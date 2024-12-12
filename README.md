# GenStrat

A quantitative strategy generation & backtesting system. With several data API provided.

## Introduction

Simple Quantitative strategies such as SMA, EWM, BBand, RSI, etc. are always the very first step for beginners to get into the Quantitative world. However, it is not easy to find a platform that can provide a simple way to backtest these ideas and stratgies. **GenStrat** is designed for

1. Someone who have ideas but unfamiliar of how to implement strategies & backtest systems.
2. Someone who want to generate lots of startegies for ML / RL.

## Project Structure

```bash

```

## Installation

git clone

```bash
git clone https://github.com/AbnerTeng/GenStrat.git

poetry install
```

through docker (tbd)

through pip (tbd)

## Usage

1. Cutomize your configuration in `config/gen_strat.yaml`

- Brief explanation of configuration

```plaintext
- DataAPIYahoo: Yahoo Finance API kwargs
- DataAPITAIFEX: Taiwan Future Exchange API kwargs
- DataLocal: If you have local data, or you don't have proxy to access any data API, the example data of SP500 ETF is in `tick_data`

- task:
    - syn_spsl (synthetic stop loss / profit experiment)
    - hpo (hyperparameter optimization among single strategy)

- trials
    - number of trials for hyperparameter optimization

- Class:
    strat: The strategy class you want to backtest
    params: The hyperparameters you want to optimize (please refer to `doc/strat_naming.md`)

Settings:
    - initial_cap: Initial capital
    - trans_cost: Transaction cost
    - stop_loss: Stop loss threshold
    - stop_profit: Stop profit threshold
```

1. Run single strategy backtesting with below command

```bash
poetry shell
poetry run python -m src.rolling_main --data_source <data_source> --plot

# Example
poetry run python -m src.rolling_main --data_source yahoo --plot
```

(Alternative) Run multiple strategies backtesting with below command

```bash
chmod +x script/syn_traj.sh

bash scirpt/syn_traj.sh
```

> Note that the whole project is still under development, everything is executable but not fully tested & optimized.