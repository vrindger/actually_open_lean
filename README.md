# Actually open source quantconnect lean engine

# Step 0.0 - motivation
```
The quantconnect lean engine is too commercialized and hard to use as an open source project. This project aims to create an actual open source version of lean. 

money is a problem that can be solved - forest gump after pwning apple stock

right approach for trading:
idea-> Backtest->live paper trade->live trade small->live trade big.

Probability of profit*avg profit - probability of loss*avg loss=your average trade profit or loss (pnl). If this is greater than all the commissions and fees, u become a money printing casino. Most important equation in trading. 

Never trade with what you are not willing to lose completely.

Limit the risk of unlimited loss potential and stick with limited loss potential trades(option spreads, crypto futures, buying margin rather than naked shorting)
```
# Step 0.0.1 - STOP AND READ THIS
* instead of doing all this, u can pay like $1,080$/mo on quantconnect.com for an institution seat to run locally or $10/mo to run on their cloud servers which might cost more - 60/mo or something not sure. idc because i like my free on-premise live trading institution grade version below

* definitely review their pricing page: https://www.quantconnect.com/pricing u will have to click choose tier to see the options.

* u'll still need to write ur own algo (not easy with their platform, but pythonic = huge plus)

* also like install docker, set up vs code
* but U won't need my dockerfile stuff or brokerage stuff. They have backtesting in their lean-cli which is also open source but I have not cracked it yet. 

# Step 0: Train and learn lean engine algo-writing
There's a bootcamp: https://www.quantconnect.com/learning/course/1/Boot-Camp-101-US-Equities
And tons of documentation on the engine online and videos

# Step 0.1: Install stuff

* Install vs code
i'm using vs code in windows subsystem on linux. Ubuntu linux works great for this. You could use an ubuntu VM or other linux.
Install python, pylance vscode extensions

* Set up code autocomplete for vs code
  * Create python environment somewhere on your machine and install these packages:
    * install miniconda. google search for downloading the ubuntu installer shell script and run it using `bash Miniconda.sh`
  * start new terminal after conda installed
  * Create conda env: `conda create --name lean python==3.11`
  * `conda activate lean`
  * install stubs autocomplete package using pip:
    * pip install quantconnect-stubs
  * in vs code press ctrl-shift-p or cmd-shift-p and select python interpreter: .conda/envs/lean/python

* Install docker desktop
  * look at docker desktop installation instructions for ubuntu or ur linux

* Install git
  * `apt install git`

* git clone my project: 
  * `git clone https://github.com/vrindger/lean`

# Step 0.2: Decide what u want to trade and pick brokerages

* Think of a trading strategy u think will work. 
* Which instruments does it trade? stocks, options, futures, future options, spot crypto, derivative crypto
* Which brokerage do u want to use? https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages
* Identify lean brokerage github open source project: https://github.com/QuantConnect/ e.g. https://github.com/QuantConnect/Lean.Brokerages.Alpaca

# Step 1 - Create your own Dockerfile for running your engine
## - some things like which brokerage are set here. i added common ones i like

Look at the Dockerfile being used in my project such as: https://github.com/vrindger/lean/blob/main/Dockerfile_dev_debug
* u might want to use a different brokerage than the ones I've used, e.g:
```
 RUN git clone https://github.com/QuantConnect/Lean.Brokerages.Binance $BINANCE_DIR && \
    cp -rf $BINANCE_DIR/QuantConnect.BinanceBrokerage $LEAN_DIR && \
    cp -rf $BINANCE_DIR/QuantConnect.BinanceBrokerage.ToolBox $LEAN_DIR
```
* u might want to download the zip from that Lean project into a Lean-master dir to use the local COPY command because git cloning the entire Lean prject takes forever.  the COPY command uses the local unzipped source code to copy the large Lean repo locally instead of cloning each time the dockerfile runs, to save time. 

* to clone everytime  u can uncomment the git clone line shown below and comment the COPY local Lean-master line.
```
# Clone Lean repository
COPY ./Lean-master $LEAN_DIR
# RUN git clone https://github.com/QuantConnect/Lean $LEAN_DIR
```


# Step 2 - Create your own trading algo! U can copy mine but use your own brokerage keys etc

* Create a new dir in the base/lean_configs dir with your own config file and .py or .cs file for C#. 
* To create algo, look at this dir:
  * https://github.com/vrindger/lean/tree/main/base/lean_configs

* MyLeanAlgorithm is my example algorithm using my config file(a config.json) with my secret keys for my brokerage's paper account. The algorithm file is a .py file.

* Yes, u will need a json file, an algo file AND the .sh bash file. this stuff is WIP

# Step 3 - Create or edit bash script 
* Edit docker_build_n_run_debug.sh 
  * https://github.com/vrindger/lean/blob/main/docker_build_n_run_debug.sh to contain your dir name (algo name) created in step 1. 

* Remove or add keys that your Dockerfile might need.

# Step 4 - Run bash script

`bash docker_build_n_run_debug.sh` 

# Random important notes:
* there's a string ticker for instruments like 'BTCUSDT' or 'GOOGL'. 
* then there's a symbol created from that ticker if u specify US stock like so:  `Market Symbol.create('SPY', SecurityType.EQUITY, Market.USA)`. symbols don't contain very much info.
* then there's a security that is added to the algorithm which contains the symbol and even more information like exchange and hours etc. It's the active security that gets traded

* [In Lean, methods only (not classes) are automatically converted from camel case(C#) to snake case:](https://www.quantconnect.com/announcements/16830/pep8-python-api-migration/p1)
  * Snake case methods, and CamelCase classes:
    ```
    self.AddUniverseSelection(ManualUniverseSelectionModel(symbols)) 
    self.add_universe_selection(ManualUniverseSelectionModel(symbols))
     ```
