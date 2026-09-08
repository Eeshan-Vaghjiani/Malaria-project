"""Reproducible teaching analysis for the Kilifi Pf8 pfcrt K76T project.

These functions analyse public, sequence-derived marker calls. They do not
estimate clinical treatment efficacy or the within-host frequency of clones.
"""
from pathlib import Path
from statistics import NormalDist
import hashlib
import json
import math
import sys

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

PROJECT_NAME = 'Kilifi_Malaria_Project'
YEARS = list(range(1994, 2021))
PERIODS = [('1994-1999',1994,1999), ('2000-2004',2000,2004),
           ('2005-2009',2005,2009), ('2010-2014',2010,2014),
           ('2015-2020',2015,2020)]
MAIN_STUDY = '1132-PF-K1000G-DBS-KE-BEJON'
EXPECTED_HASHES = {
    'Pf8_samples.txt':'50b7dcf2d0ffea0ef429f62801a0e184ab4da4d22708f9ec685652062c8dadb0',
    'Pf8_drug_resistance_marker_genotypes.tsv':'866450e8b32a5f6433f813932565579512cc5e0424b999d6769818988840e4ed',
}


def locate_project_root():
    candidates = [Path(__file__).resolve().parent.parent, Path.cwd(), Path.cwd()/PROJECT_NAME]
    candidates.extend(Path.cwd().parents)
    for p in candidates:
        if (p/'02_Datasets/Original_Pf8/Pf8_samples.txt').exists():
            return p
    raise FileNotFoundError('Extract the complete Kilifi_Malaria_Project folder first.')


def verify_original_inputs(root):
    report = {}
    for name, expected in EXPECTED_HASHES.items():
        path = Path(root)/'02_Datasets/Original_Pf8'/name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'{name} differs from the verified snapshot. Keep the original files unchanged; review any new release explicitly.')
        report[name] = actual
    return report


def classify_call(raw):
    """Collapse ordering only; preserve the original value in raw_crt76_call."""
    value = str(raw).strip()
    if value in {'', '-', '*', '!', 'nan', 'None', '<NA>'}:
        return 'uncallable'
    tokens = {x.strip() for x in value.split(',')}
    if tokens == {'K'}: return 'K_only'
    if tokens == {'T'}: return 'T_only'
    if tokens == {'K', 'T'}: return 'mixed_KT'
    return 'uncallable'


def period_for_year(year):
    for label, first, last in PERIODS:
        if first <= int(year) <= last: return label
    raise ValueError(f'Year outside the planned scope: {year}')


def build_dataset(root, export=True):
    root = Path(root)
    hashes = verify_original_inputs(root)
    raw = root/'02_Datasets/Original_Pf8'
    meta = pd.read_csv(raw/'Pf8_samples.txt', sep='\t', dtype=str, keep_default_na=False)
    geno = pd.read_csv(raw/'Pf8_drug_resistance_marker_genotypes.tsv', sep='\t', dtype=str, keep_default_na=False)
    if not meta['Sample'].is_unique or not geno['Sample'].is_unique:
        raise ValueError('Duplicate Sample identifiers must be reviewed before joining.')
    scope = meta.loc[(meta['Country']=='Kenya') & (meta['Admin level 1']=='Kilifi')].copy()
    joined = scope.merge(geno[['Sample','crt_76[K]']],on='Sample',how='left',validate='one_to_one')
    joined['year_numeric'] = pd.to_numeric(joined['Year'], errors='coerce')
    if not set(joined['QC pass'].str.lower()) <= {'true','false'}:
        raise ValueError('Unexpected QC pass encoding.')
    joined['qc_pass_bool'] = joined['QC pass'].str.lower().eq('true')
    joined['eligible_year'] = joined['year_numeric'].between(1994,2020) & joined['year_numeric'].mod(1).eq(0)
    joined['included_qc_cohort'] = joined['qc_pass_bool'] & joined['eligible_year']
    joined['inclusion_reason'] = np.select(
        [~joined['qc_pass_bool'], ~joined['eligible_year']],
        ['excluded_QC','excluded_year'], default='included_QC_cohort')
    selected = joined.loc[joined['included_qc_cohort']].copy()
    selected['case_group'] = selected['All samples same case'].map(
        lambda x: ','.join(sorted({v.strip() for v in x.split(',') if v.strip()})))
    if selected['case_group'].eq('').any() or not selected['case_group'].is_unique:
        raise ValueError('Missing or repeated recorded case groups require review before treating samples as independent.')
    out = pd.DataFrame({
        'sample_id': selected['Sample'], 'study': selected['Study'],
        'country': selected['Country'], 'admin1': selected['Admin level 1'],
        'year': selected['year_numeric'].astype(int), 'case_group': selected['case_group'],
        'qc_pass': selected['qc_pass_bool'],
        'genome_callable_pct': pd.to_numeric(selected['% callable'],errors='coerce'),
        'sample_type': selected['Sample type'], 'ena_accessions': selected['ENA'],
        'raw_crt76_call': selected['crt_76[K]'],
    })
    out['marker_call'] = out['raw_crt76_call'].map(classify_call)
    out['marker_callable'] = out['marker_call'].ne('uncallable')
    out['has_76T'] = out['marker_call'].map({'K_only':0,'T_only':1,'mixed_KT':1}).astype('Int64')
    out['unambiguous_76T'] = out['marker_call'].map({'K_only':0,'T_only':1}).astype('Int64')
    out['time_period'] = out['year'].map(period_for_year)
    out['source_release'] = 'MalariaGEN Pf8'
    out = out.sort_values(['year','sample_id']).reset_index(drop=True)
    report = {
        'metadata_rows':len(meta), 'marker_file_rows':len(geno),
        'all_Kilifi_records':len(joined), 'excluded_QC':int((~joined['qc_pass_bool']).sum()),
        'excluded_year_after_QC':int((joined['qc_pass_bool'] & ~joined['eligible_year']).sum()),
        'qc_cohort_records':len(out), 'callable_records':int(out['marker_callable'].sum()),
        'unambiguous_records':int(out['unambiguous_76T'].notna().sum()),
        'K_only':int(out['marker_call'].eq('K_only').sum()),
        'T_only':int(out['marker_call'].eq('T_only').sum()),
        'mixed_KT':int(out['marker_call'].eq('mixed_KT').sum()),
        'uncallable':int(out['marker_call'].eq('uncallable').sum()),
        'unique_case_groups':int(out['case_group'].nunique()),
        'observed_year_count':int(out['year'].nunique()),
        'missing_years':sorted(set(YEARS)-set(out['year'])),
        'input_sha256':hashes,
    }
    validate_snapshot(out,report)
    if export:
        dest=root/'02_Datasets/Kilifi_Subsets'; dest.mkdir(exist_ok=True,parents=True)
        out.to_csv(dest/'kilifi_pfcrt_qcpass.csv',index=False)
        out.loc[out['unambiguous_76T'].notna()].to_csv(dest/'kilifi_pfcrt_unambiguous.csv',index=False)
        joined[['Sample','Study','Country','Admin level 1','Year','QC pass','Exclusion reason',
                'All samples same case','included_qc_cohort','inclusion_reason']].to_csv(dest/'kilifi_inclusion_audit.csv',index=False)
        out.groupby('study').agg(records=('sample_id','size'),first_year=('year','min'),last_year=('year','max')).reset_index().to_csv(dest/'study_inventory.csv',index=False)
        (root/'07_Reproducibility/data_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return out, report


def validate_snapshot(data, report):
    expected = {'metadata_rows':33325,'marker_file_rows':24409,'all_Kilifi_records':2078,
        'excluded_QC':206,'excluded_year_after_QC':0,'qc_cohort_records':1872,
        'callable_records':1872,'unambiguous_records':1703,'K_only':1236,'T_only':467,
        'mixed_KT':169,'uncallable':0,'unique_case_groups':1872,'observed_year_count':25}
    for k, v in expected.items():
        if report[k] != v: raise AssertionError(f'Snapshot check failed: {k}: {report[k]} != {v}')
    if report['missing_years'] != [2001,2002]: raise AssertionError('Unexpected annual coverage')
    if not data['sample_id'].is_unique: raise AssertionError('Samples duplicated')
    if not data.loc[data['marker_call']=='mixed_KT','has_76T'].eq(1).all(): raise AssertionError('Mixed carriers lost')
    if not data.loc[data['marker_call']=='mixed_KT','unambiguous_76T'].isna().all(): raise AssertionError('Mixed calls included in unambiguous denominator')


def wilson_interval(k,n,confidence=0.95):
    if not 0 <= k <= n: raise ValueError('Expected 0 <= successes <= denominator')
    if n == 0: return math.nan,math.nan
    z=NormalDist().inv_cdf(0.5+confidence/2)
    p=k/n; denom=1+z*z/n
    center=(p+z*z/(2*n))/denom
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return max(0.,center-half),min(1.,center+half)


def summarize(data, group='year'):
    groups=YEARS if group=='year' else [p[0] for p in PERIODS]
    rows=[]
    for value in groups:
        d=data.loc[data[group]==value]
        counts=d['marker_call'].value_counts()
        K=int(counts.get('K_only',0)); T=int(counts.get('T_only',0)); M=int(counts.get('mixed_KT',0))
        n=K+T+M; u=K+T
        r={group:value,'n_qc':len(d),'n_callable':n,'n_unambiguous':u,
           'n_K_only':K,'n_T_only':T,'n_mixed_KT':M,'n_uncallable':len(d)-n,
           'sampling_status':'observed' if len(d) else 'no_samples'}
        for label,k,denom in [('carrier',T+M,n),('unambiguous',T,u),('K_only',K,n),('T_only',T,n),('mixed_KT',M,n)]:
            lo,hi=wilson_interval(k,denom)
            r[label+'_proportion']=k/denom if denom else math.nan
            r[label+'_ci_low']=lo; r[label+'_ci_high']=hi
        rows.append(r)
    return pd.DataFrame(rows)


def sampling_sensitivity(data):
    main=data.loc[data['study']==MAIN_STUDY]
    a=summarize(data); b=summarize(main)
    pooled=summarize(data,'time_period').set_index('time_period')
    main_pooled=summarize(main,'time_period').set_index('time_period')
    rows=[]
    for label,first,last in PERIODS:
        aa=a.loc[a['year'].between(first,last) & a['n_callable'].gt(0)]
        bb=b.loc[b['year'].between(first,last) & b['n_callable'].gt(0)]
        rows.append({'time_period':label,'observed_years':len(aa),
            'all_studies_n':int(pooled.loc[label,'n_callable']),
            'all_studies_pooled_carrier':pooled.loc[label,'carrier_proportion'],
            'all_studies_equal_year_carrier':aa['carrier_proportion'].mean(),
            'main_study_n':int(main_pooled.loc[label,'n_callable']),
            'main_study_pooled_carrier':main_pooled.loc[label,'carrier_proportion'],
            'main_study_equal_year_carrier':bb['carrier_proportion'].mean()})
    return pd.DataFrame(rows),b


def exploratory_period_test(data):
    p=summarize(data,'time_period')
    table=np.column_stack([p['n_T_only']+p['n_mixed_KT'],p['n_K_only']])
    stat,pvalue,dof,expected=chi2_contingency(table,correction=False)
    valid=bool(np.all(expected>=5))
    return {'method':'Pearson chi-square: predefined period x detected 76T carriage',
        'status':'Approximation checks passed' if valid else 'Do not interpret: expected-count check failed',
        'statistic':float(stat) if valid else None,'p_value':float(pvalue) if valid else None,
        'degrees_of_freedom':int(dof),'minimum_expected_count':float(expected.min()),
        'periods':p['time_period'].tolist(),'columns':['76T_detected','K_only'],
        'observed_counts':table.tolist(),
        'interpretation_limit':'Exploratory association in archived samples. It is not proof of a monotonic trend, a policy effect or clinical resistance.'}


def make_figures(annual,sensitivity,output_dir):
    import matplotlib
    if 'ipykernel' not in sys.modules: matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    output_dir=Path(output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'figure.facecolor':'white','savefig.facecolor':'white'})
    created=[]
    source='Source: MalariaGEN Pf8, bundled snapshot. Example analysis for group review.'
    fig,ax=plt.subplots(figsize=(11,4.7))
    ax.bar(annual['year'],annual['n_qc'],color='#456779',width=.75)
    ax.set(title='Kilifi sample coverage, 1994–2020',xlabel='Collection year',ylabel='QC-passing records')
    ax.set_xticks(YEARS[::2]); ax.grid(axis='y',alpha=.18); ax.set_axisbelow(True)
    for year in [2001,2002]: ax.annotate('No\nsamples',(year,0),xytext=(year,28),ha='center',fontsize=8,rotation=90)
    fig.text(.08,.015,source,fontsize=8,color='#555555'); fig.tight_layout(rect=[0,.05,1,1])
    path=output_dir/'01_yearly_sample_counts.png'; fig.savefig(path,dpi=180); plt.close(fig); created.append(path)
    fig,ax=plt.subplots(figsize=(11,4.7)); bottom=np.zeros(len(annual))
    for field,label,color in [('K_only','K76-only','#91ACBA'),('T_only','76T-only','#454B53'),('mixed_KT','Mixed K/T','#C29355')]:
        values=annual[field+'_proportion'].fillna(0).to_numpy()
        ax.bar(annual['year'],values,bottom=bottom,label=label,color=color,width=.76)
        bottom+=values
    ax.set(xlabel='Collection year',ylabel='Proportion of callable records',ylim=(0,1.04))
    ax.set_title('Composition of callable pfcrt codon-76 records',pad=40)
    ax.yaxis.set_major_formatter(PercentFormatter(1));ax.set_xticks(YEARS[::2])
    ax.legend(ncol=3,loc='lower center',bbox_to_anchor=(.5,1.01),frameon=False)
    for year in [2001,2002]:ax.text(year,.05,'No samples',rotation=90,ha='center',va='bottom',fontsize=8)
    fig.text(.08,.015,source+' Gaps represent no samples, not zero prevalence.',fontsize=8,color='#555555')
    fig.tight_layout(rect=[0,.06,1,1]);path=output_dir/'02_marker_composition.png';fig.savefig(path,dpi=180);plt.close(fig);created.append(path)
    fig,ax=plt.subplots(figsize=(11,5.0))
    for field,label,color,shift,marker in [('carrier','76T detected: T-only + mixed','#275D74',-.13,'o'),('unambiguous','T-only among unambiguous calls','#AA6736',.13,'s')]:
        d=annual.loc[annual[field+'_proportion'].notna()]
        yy=d[field+'_proportion'].to_numpy(); lo=d[field+'_ci_low'].to_numpy(); hi=d[field+'_ci_high'].to_numpy()
        ax.errorbar(d['year']+shift,yy,yerr=np.maximum(0,np.vstack([yy-lo,hi-yy])),fmt=marker,markersize=3.5,
                    color=color,elinewidth=.8,capsize=2,label=label)
    ax.set(title='How the mixed-call definition affects the temporal summary',xlabel='Collection year',ylabel='Sample-level prevalence',ylim=(-.03,1.04))
    ax.set_xticks(YEARS[::2]);ax.yaxis.set_major_formatter(PercentFormatter(1));ax.grid(axis='y',alpha=.18)
    ax.legend(loc='upper right',framealpha=.95,fontsize=9)
    fig.text(.08,.035,'Points with 95% Wilson intervals. Definitions use different denominators; no values are inferred for 2001–2002.',fontsize=8,color='#555555')
    fig.text(.08,.01,source,fontsize=8,color='#555555');fig.tight_layout(rect=[0,.07,1,1])
    path=output_dir/'03_temporal_prevalence.png';fig.savefig(path,dpi=180);plt.close(fig);created.append(path)
    return created


def run_analysis(root=None,output_dir=None):
    root=Path(root or locate_project_root())
    dest=Path(output_dir) if output_dir else root/'04_Example_Outputs'
    dest.mkdir(exist_ok=True,parents=True)
    data,validation=build_dataset(root)
    annual=summarize(data);period=summarize(data,'time_period')
    sensitivity,annual_main=sampling_sensitivity(data)
    annual.to_csv(dest/'annual_summary.csv',index=False)
    annual[['year','n_qc','sampling_status']].to_csv(root/'02_Datasets/Kilifi_Subsets/year_coverage.csv',index=False)
    period.to_csv(dest/'period_summary.csv',index=False)
    sensitivity.to_csv(dest/'sampling_sensitivity.csv',index=False)
    annual_main.to_csv(dest/'annual_main_study.csv',index=False)
    (dest/'exploratory_period_test.json').write_text(json.dumps(exploratory_period_test(data),indent=2),encoding='utf-8')
    make_figures(annual,sensitivity,dest)
    return {'data':data,'validation':validation,'annual':annual,'period':period,
            'sensitivity':sensitivity,'annual_main_study':annual_main,'output_dir':dest}


def checks():
    # Concrete risks: comma order, incorrect mixed denominator, period boundaries,
    # and zero-sample years accidentally plotted as zero prevalence.
    assert classify_call('K,T')==classify_call('T,K')=='mixed_KT'
    assert classify_call('K')=='K_only' and classify_call('T')=='T_only'
    assert classify_call('-')=='uncallable'
    assert period_for_year(1999)=='1994-1999' and period_for_year(2000)=='2000-2004'
    assert period_for_year(2020)=='2015-2020'
    assert all(math.isnan(v) for v in wilson_interval(0,0))
    lo,hi=wilson_interval(0,12); assert lo==0 and 0<hi<1
    example=pd.DataFrame({'year':[2000]*4,'marker_call':['K_only','T_only','mixed_KT','uncallable']})
    s=summarize(example).set_index('year')
    assert s.loc[2000,'carrier_proportion']==2/3 and s.loc[2000,'unambiguous_proportion']==1/2
    assert math.isnan(s.loc[2001,'carrier_proportion']) and s.loc[2001,'n_callable']==0
    return 'Classification, denominator, boundary and missing-year checks passed.'
