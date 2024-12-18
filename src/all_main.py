"""
Rolling main script to run the rolling strategy
"""

import os
import pickle
from typing import Union

from argparse import ArgumentParser, Namespace
import numpy as np

from .strategy import Strategy, RunStrategy
from .utils.general_utils import load_config, get_class
from .utils.data_utils import transfer_colnames
from .get_data import DataAPI
from .base.base_indicator import GlobalDataManager
from .indicators import BB, EMA, RSI, SMA


def get_args() -> Namespace:
    """
    parsing arguments
    """
    parser = ArgumentParser()
    parser.add_argument("--data_source", type=str, default="self")
    parser.add_argument("--plot", "-p", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    cfg = load_config("config/gen_strat.yaml")
    RANDOM_PARAM = False if cfg.task == "syn_spsl" else True
    fetcher = DataAPI(args.data_source)
    api_map = {
        "yahoo": cfg.DataAPIYahoo,
        "self": cfg.DataLocal,
        "taifex": cfg.DataAPITAIFEX,
    }
    data = fetcher.fetch(api_map[args.data_source])
    df = transfer_colnames(data)
    GlobalDataManager.set_data(df)
    full_log, full_trajectory, full_return_log, full_date, full_param, full_transac_cumret = (
        [],
        [],
        [],
        [],
        [],
        []
    )
    ModelClass = get_class(cfg.Class.strat)
    ind = ModelClass(*cfg.Class.params)
    last_idx, half_ids = None, []
    ind: Union[BB, EMA, RSI, SMA]

    if not RANDOM_PARAM:
        cfg.trials = 1

    val_df = ind.build()
    strat_val = Strategy(val_df, ind)
    valid_runner = RunStrategy(val_df, strat_val, **cfg.Settings)
    ret = valid_runner.run(0, val_df.shape[0] - 1)
    period_param = {ind.tag: ind.get_init_args()}
    full_log.append(valid_runner.trade_log)
    full_trajectory.extend(valid_runner.trajectory)
    full_return_log.extend(valid_runner.return_log["return"])
    full_date.extend(valid_runner.return_log["date"])
    full_param.extend(period_param)
    full_transac_cumret.extend(valid_runner.return_log["transac_cumret"])

    GlobalDataManager.reset()

    dic = {
        "date": full_date,
        "return": full_return_log,
        "for_stoploss": full_transac_cumret,
        "trade_log": full_log,
        "trajectory": full_trajectory,
        "param": full_param,
    }
    print(f"Cum ret: {np.cumsum(dic['return'])[-1]}")

    if cfg.task == "syn_spsl":
        pkl_filename = f"{str(ind)}_{cfg.Settings.sl_thres}_{cfg.Settings.sp_thres}.pkl"
        folder_name = f"synthetic_{str(ind)}"

        if folder_name not in os.listdir("trade_log"):
            os.mkdir(f"trade_log/{folder_name}")

        with open(f"trade_log/{folder_name}/{pkl_filename}", "wb") as pkl_file:
            pickle.dump(dic, pkl_file)

    else:
        pkl_filename = (
            f"{ind.tag}_new_{cfg.Settings.sl_thres}_{cfg.Setting.sp_thres}.pkl"
        )

        if pkl_filename in os.listdir("trade_log"):
            pkl_filename = f"{ind.tag}_new_{np.random.randint(1000)}.pkl"

        with open(f"trade_log/{pkl_filename}", "wb") as pkl_file:
            pickle.dump(dic, pkl_file)
