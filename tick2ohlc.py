import pandas as pd
import sys

# NOTE: Each list below must be divisible by last entry of prev list
# (15 by 5, 30 by 15, 1D by 6H, etc.)
_UNITS = [
    ["1min"],
    ["5min"],
    ["15min"],
    ["30min"],
    ["1H"],
    ["4H", "6H"],
    ["1D"],
    ["3D", "1W", "1M"],
]


def resample(df: pd.DataFrame, unit: str) -> pd.DataFrame:
    tick = "last" in df.columns
    col_actions = (
        {"last": "ohlc", "volume": "sum"}
        if tick
        else {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )
    new_df = df.resample(unit).agg(col_actions).dropna()
    if tick:
        # Collapse multindex and make it flat
        new_df.columns = new_df.columns.get_level_values(1)
    # Convert index into separate date/time columns
    new_df["date"] = new_df.index.strftime("%m/%d/%Y")
    new_df["time"] = new_df.index.strftime("%H:%M")
    # Make DT index a regular column
    return new_df


def write_data(filename: str, df: pd.DataFrame, unit: str):
    new_df = df.reset_index()
    new_df.to_csv(
        f"{filename}_{unit.lower()}.csv",
        index=False,
        columns=["date", "time", "open", "high", "low", "close", "volume"],
    )


def read_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(
        filename,
        names=["datetime", "last", "volume"],
        parse_dates=["datetime"],
        date_parser=lambda epoch: pd.to_datetime(epoch, unit="s"),
        index_col="datetime",
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tick2ohlc <base_filename>\n")
        print("<base_filename> = filename without the .csv extension")
        sys.exit(1)

    filename = sys.argv[1]
    # Start by reading tick data
    print("Reading tick data...", end="", flush=True)
    df = read_data(filename + ".csv")
    print("done")

    for units in _UNITS:
        for unit in units:
            print(f"Resampling and writing CSV for: {unit}...", end="", flush=True)
            new_df = resample(df, unit)
            write_data(filename, new_df, unit)
            print("done")

        # Last new_df of list becomes new df for next cycle
        df = new_df
