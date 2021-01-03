# tick2ohlc
Convert basic tick data (using 'last' not 'bid/ask') in CSV files to OHLC bar CSV files. For example, the tool works with the cryptocurrency tick data stored here: http://api.bitcoincharts.com/v1/csv/. By default, it generates multiple minute, hour, day, week, and monthly bar files. This is easily changed by modifying the top of the source file.

## Requirements

* Python 3.7 or higher
* Optional: Poetry (https://python-poetry.org/)

## Install

NOTE: Replace `python` in first line below with the correct name for your Python 3.7 or higher executable

### Using Poetry

```shell
python -m venv .env         # Create venv (optional)
source .env/bin/activate    # Activate venv (if created venv)
poetry install --no-dev     # Install dependencies
```

### Using Regular PIP

```shell
python -m venv .env             # Create venv (optional)
source .env/bin/activate        # Activate venv (if created venv)
pip install -r requirements.txt # Install dependencies
```

## Run

```shell
python ./tick2ohlc.py <base_filename>  # <base_filename> = filename minus .csv ext.
```