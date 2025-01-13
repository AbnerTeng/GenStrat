from argparse import ArgumentParser, Namespace

import yfinance as yf
from rich.progress import track

from ..utils.general_utils import load_config


def save_data(stock_id: str, args: Namespace) -> None:
    """
    Save the stock data to the data folder

    Args:
        stock_id (str): Stock ID

    Returns:
        None
    """
    data = yf.download(stock_id, start=args.start, end=args.end)
    data.to_csv(f"env_data/{stock_id}.csv")


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--stock_id_conf", type=str, default="config/stock_id.yaml")
    parser.add_argument("--section", type=str, default="misc")
    parser.add_argument("--start", type=str, default="2010-01-01")
    parser.add_argument("--end", type=str, default="2024-08-01")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    config = load_config(args.stock_id_conf)
    stock_id_list = config[args.section]

    for stock_id in track(stock_id_list):
        save_data(stock_id, args)