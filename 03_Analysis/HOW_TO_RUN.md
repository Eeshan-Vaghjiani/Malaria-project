# Run the Kilifi starter analysis

The main analysis uses only the data already in this folder. The supplied output files show what a successful run produces. You do not need a GPU or the full genome-wide Pf8 downloads.

## Option A: run Python locally

Install Python 3.12 if it is not already available. Open a terminal **inside the extracted `Kilifi_Malaria_Project` folder**. The tested analysis package versions are recorded in `requirements.txt`; installing them requires internet access.

On Windows, use Command Prompt:

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r 03_Analysis\requirements.txt
.venv\Scripts\python.exe 03_Analysis\run_analysis.py
```

On macOS/Linux with Python 3.12 installed:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r 03_Analysis/requirements.txt
.venv/bin/python 03_Analysis/run_analysis.py
```

These commands call the environment's interpreter directly, so activation is optional. See the [official Python environment documentation](https://docs.python.org/3/library/venv.html).

A successful run prints 1,872 retained records, 169 mixed K/T calls and 1,703 unambiguous records. It identifies 2001 and 2002 as years without samples. It regenerates the prepared CSVs and example outputs at their existing paths. Save copies under new filenames before making experimental changes that you want to keep.

## Option B: learn through the notebook

Open `Kilifi_Starter_Analysis.ipynb` in Jupyter or upload it to [Google Colab](https://colab.research.google.com/). Run the code cells in order and read the explanations between them.

For local Jupyter, install JupyterLab in the same environment using that environment's Python with `-m pip install jupyterlab`, then launch it with `-m jupyterlab`. Open the supplied notebook. The folder remains accessible to its code even if Jupyter starts in `03_Analysis`.

For Colab:

1. Upload the notebook using Colab's **Upload notebook** option.
2. Run the first code cell. If the project folder is absent, it asks you to upload the complete `Kilifi_Malaria_Project.zip`.
3. Select the downloaded ZIP. The cell extracts it into the Colab working directory and locates the analysis files.
4. Continue through the remaining cells. Standard scientific packages are normally available in Colab; their versions may differ from the recorded local environment.
5. If a required package is missing or incompatible, use a separate Colab code cell: `%pip install -r /content/Kilifi_Malaria_Project/03_Analysis/requirements.txt`, then restart the session if Colab requests it and run the notebook again.
6. Download files you want to keep from Colab's Files pane and save the notebook. Colab sessions are temporary; see its [official FAQ](https://research.google.com/colaboratory/faq.html).

The notebook code was checked by executing its ordinary Python cells sequentially in the recorded local environment. Its interactive Colab upload step requires your browser and has not been exercised in your Google account.

## What the notebook does

1. Finds the complete extracted project folder and imports the helpers.
2. Checks the original data hashes and rebuilds the Kilifi dataset.
3. Checks sample counts, coding and missing-year handling.
4. Produces annual and period summaries with Wilson 95% confidence intervals.
5. Compares primary and secondary marker definitions, pooled versus equally weighted annual summaries, and all studies versus the largest study.
6. Exports three example figures and an exploratory period association test.
7. Prompts the group to interpret the results and record decisions.

## Files you may edit

The notebook is intended for group notes and extensions. Core preparation and calculations are in `analysis_helpers.py`; `run_analysis.py` calls those functions. The source files in `02_Datasets/Original_Pf8` are preserved snapshots. A changed source hash intentionally stops execution so that a new download cannot silently alter the analysis.

The proposed periods are fixed teaching choices, not fitted change points or official policy periods. Changing the question, period definitions, inclusion rules or outcomes should follow lecturer feedback and be recorded in `06_Group_Work/MEETING_AND_DECISIONS.md`.

## Troubleshooting

| Message / problem | Action |
|---|---|
| `No module named pandas`, `numpy`, `scipy` or `matplotlib` | Install `requirements.txt` with the same Python interpreter used to run the script. |
| Cannot find `analysis_helpers` or `Pf8_samples.txt` | Extract the whole ZIP, preserve folder names and run from the project folder. |
| Original file differs from verified snapshot | Restore the bundled original. If intentionally changing data releases, review and update validation rules explicitly. |
| CSV shows many values in one column | Import CSV with a comma delimiter; import original TXT/TSV with a tab delimiter. |
| 2001/2002 proportions appear blank | Expected: those years have no retained samples. |
| Existing output figures changed after running | The script regenerates example outputs. Preserve earlier versions under different names if comparing changes. |

Official software references: [JupyterLab installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html), [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html), [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html), [SciPy contingency-table test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html).
