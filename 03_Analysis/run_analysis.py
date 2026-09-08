"""Run from any directory: python path/to/03_Analysis/run_analysis.py"""
from analysis_helpers import checks, run_analysis

if __name__=='__main__':
    print(checks())
    results=run_analysis()
    v=results['validation']
    print(f"Verified Kilifi records: {v['qc_cohort_records']:,}; mixed K/T: {v['mixed_KT']}; unambiguous: {v['unambiguous_records']:,}")
    print('Years without samples:',v['missing_years'])
    print('Example outputs:',results['output_dir'])
    print('These are reproducible exploratory outputs for group review, not a completed report.')
