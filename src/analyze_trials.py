"""Fixed-budget analysis of preregistered single-use trial records.

This software validates record accounting and computes a conditional test. It
cannot validate calibration assumptions, optical isolation, or source tails.
No result is experimental when the plan is marked synthetic.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from theory import certify_counts, certify_reverse_counts


def analyze(plan:dict,rows:list[dict],allow_synthetic:bool=False)->dict:
    synthetic=bool(plan.get('synthetic',False))
    if synthetic and not allow_synthetic:raise ValueError('Synthetic plan. Use --allow-synthetic for a demonstration only.')
    if not synthetic and plan.get('approval_status')!='LAB_CALIBRATED_AND_PREREGISTERED':
        raise ValueError('Calibration/preregistration have not been declared complete.')
    if plan.get('decoder')!='one_click_port_else_inconclusive':raise ValueError('Unsupported or unspecified decoder')
    if plan.get('label_law')!='independent_uniform_per_interrogation':raise ValueError('Unsupported label law')
    N=plan['fixed_N']
    if len(rows)!=N:raise ValueError(f'Expected exactly {N} attempted trials, received {len(rows)}')
    ids=set();counts={'correct':0,'wrong':0,'inconclusive':0};labels=[0]*4;mask_counts=[0]*16
    for row in rows:
        rid=row['trial_id']
        if not rid or rid in ids:raise ValueError('Missing/duplicate trial id')
        ids.add(rid)
        if row['condition_id']!=plan['condition_id'] or row['calibration_id']!=plan['calibration_id']:
            raise ValueError('Unapproved condition/calibration change')
        if row['phase_code_id']!=plan['phase_code_id'] or row['receiver_id']!=plan['receiver_id']:
            raise ValueError('Unapproved phase code or receiver change')
        j=int(row['hidden_label']);mask=int(row['click_mask'])
        if j not in range(4) or mask not in range(16):raise ValueError('Invalid label or mask')
        labels[j]+=1;mask_counts[mask]+=1
        if mask not in (1,2,4,8):counts['inconclusive']+=1
        elif mask==(1<<j):counts['correct']+=1
        else:counts['wrong']+=1
    test=plan.get('test','classical_probe_exclusion')
    if test=='classical_probe_exclusion':
        result=certify_counts(counts,float(plan['penalty']),float(plan['kappa_upper']),float(plan['mean_energy_upper']),
                              float(plan['alpha_stat']),float(plan['alpha_calibration']))
        tail=float(plan.get('multiphoton_probability_upper',0))
        if not 0<=tail<=1:raise ValueError('Invalid tail bound')
        result['tail_score_subtraction']=tail
        result['certified_gap']-=tail
        result['rejects_classical_null']=result['certified_gap']>0
    elif test=='four_path_one_photon_exclusion':
        if not 0<=float(plan['mean_energy_upper'])<=1:
            raise ValueError('Reverse comparison requires coherent signal mean <= one photon')
        if len(plan['transmission_upper'])!=4:
            raise ValueError('This analyzer expects four paths')
        result=certify_reverse_counts(counts,float(plan['penalty']),plan['transmission_upper'],
                float(plan['operator_radius']),float(plan['alpha_stat']),float(plan['alpha_calibration']))
    else:raise ValueError('Unsupported test')
    result['test']=test
    result['counts']=counts;result['label_counts']=labels;result['all_16_mask_counts']=mask_counts
    result['not_verified_by_software']=['conditional energy guarantee including high-number tails',
         'common phase reference across hidden settings','single-use and label isolation',
         'uniformity/independence of label generator','optical channel interval on held-out trials',
         'no output-dependent exclusion or optional stopping']
    result['status']='SYNTHETIC_NOT_AN_EXPERIMENT' if synthetic else 'CONDITIONAL_TEST_WITH_DECLARED_EXTERNAL_CALIBRATION'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,required=True);parser.add_argument('--trials',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--allow-synthetic',action='store_true')
    args=parser.parse_args()
    plan=json.loads(args.plan.read_text())
    with args.trials.open(newline='') as f:rows=list(csv.DictReader(f))
    result=analyze(plan,rows,args.allow_synthetic)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
