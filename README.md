# proj-properties-data
Ingestion and analysis of a small mock database of real estate properties.

## Process
A data pipeline is built with [DVC](https://dvc.org/) which first cleans and transforms the .csv files in `data` with the scripts in `scripts`, then produces some charts for analysis in `plots`.

Note that the repo does not contain the data and the pipeline structure follows dbt best practices. The scripts are very verbose and somewhat messy to allow the reader to follow the process for understanding and cleaning the data.

The `data` folder contains another README with thoughts on the data and a summary of the actions taken, while the `plots` folder contains a README with some of the gained insights and the business recommendations following from those insights.

## Requirements
It's assumed that you have python 3 installed on your machine. After cloning the repo follow these steps:

1. Create a virtual environment

```bash
python3 -m venv venv
```

2. Activate the environment

```bash
source venv/bin/activate (Unix)
venv\Scripts\activate (Windows)
```

3. Upgrade pip and install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Finally, you need unzip to the raw data onto your machine and point the pipeline to it. There's a `.env` file that's pointing to the Downloads folder on my unix machine. If you're on unix yourself, simply change the user name, and also change the path should your local database folder be located elsewhere:

```
DB_PATH=<absolute path to the folder containing the csv files>
```

## Usage

All processing is done through python scripts located in `scripts` and orchestrated with DVC. To see the DAG of the pipeline, use the command:

```bash
dvc dag
```

The dependencies between the scripts are controlled by the `dvc.yaml` file which contains the description of the steps and what dependencies (both scripts and data) each step has.

To actually run everything, simply type:

```bash
dvc repro
```

This command runs everything in the project that you have not already run. If something fails in the run, just go to the script that failed, fix it, and then run `dvc repro` again. It will not run the steps that were already successful again.


## Special case: Getting new data

If you have already run `dvc repro` on your local repository and would like to run the pipeline again with new data, you have to force DVC to rerun the fetching stages, as they are not rerun normally unless the SQL or python scripts used change. To force DVC to rerun everything, type:

```bash
dvc repro --force
```

This forces all stages to be rerun even if nothing has changed.