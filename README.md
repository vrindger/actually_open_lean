# Actually open source quantconnect lean engine

24-7 in my 911

This project aims to create a true, actual, non-commercial, community edition or free and open source version of QuantConnect lean. It does not require any subscriptions. It simply makes the beautiful QuantConnect Lean engine available with all the brokers in a local manner for you. Trading is a private affair and I know how important a local platform is for you. It was for me. Jared Broad, who is part Austin Powers, part Dr. Evil and part 'Bhairo becomes Byron because their minds are very narrow' Mini-me is a confused individual. He makes sure all his code is open source, however, the source code is unusable for the majority of the world as it is. Therefore, there are projects like this that need to crop up. I know if I searched for 'actually open source lean' or 'truly open source lean' or 'madly open source lean' or 'deeply open source lean', others must have also. This project aims to help those people, because there isn't such a project currently and this has worked so far for me in my personal trading algorithms. You can fork this, privatize it, use it to make money, whatever. 

Some caveats though:
1. if you make money from this, please please please do share some with me as I'm still in a 9 to 5 x 50 year rut
1. It's a very rudimentary setup with shell scripts and plain docker. Should toally be pythonized
2. It doesn't have plotting
3. No warranties absolutely not
4. If u have pull requests for nice features, I will integrate them in for the world. 

## I'm a broke guy. Please pay me if you made money from this, which I know some of you will, given that 40% of IB accounts are profitable...!!:

My receiving wallets:
Ethereum 0xd576227aCc7d74259F66a8AFd379C7f36eCee41A (includes Ethereum compatible networks like Polygon, Arbitrum, OP Mainnet, Base, Blast, Linea and Avalanche)
Solana ArTNKfq3MWF3JfZXAquE5dhAQQGWiUVNw1ufkuV8WwAU
Bitcoin bc1q3guagg7zrh3ssw3vgw88jsrj8lulqfzf508u0x
Dogecoin DSRYJhMLzyiQajrSpZQgc2hfPwpc2gEqae

I'm a simple musician (robinhood?) and this trading stuff is just annoying to me https://www.youtube.com/shorts/pHl_lISFGJ0

## Documentation

### Supported Operating Systems
this uses bash scripts and docker
  *   Linux
  *   macOS bash shell? 
  *   Windows subsystem for Linux
  *   Windows not supported unfortunately unless you can get it to work with the Windows bash shell. Yucghk

### `lean_algos` Your main script directory = lean_algos/MyLeanAlgorithmTemplate

`lean_algos` is the directory where you can place your algo `directory(s)`. Each directory will contain a set of artifacts and be for one algorithm that will be built from scripts within the `MyLeanAlgorithmTemplate` directory

Check the template dir `MyLeanAlgorithmTemplate` for a 'non-functional' python Lean example with some goodies I left in. At a minimum you will always need:
* A `QCAlgorithm` class written in either .cs or .py - `MyLeanAlgorithm.py` - this is your actual trading algorithm file which can be written in either `python` or `C#`. `C#` for ultimate speed I suppose
* `config.json` file (this will specify import config items, mostly leave unchanged). Change it to add:
    1. your brokerage API keys (yes, KEEP YOUR FORKEDREPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE KEEP YOUR REPOS PRIVATE!!)

        ```
        "alpaca-api-key": "redacted",
        "alpaca-api-secret": "redacted",
        ```
    * `algorithm-location`: "../../../Algorithm.Python/MyLeanAlgorithm.py" Yes you need the 3 dots because this will be executed from a dll inside Lean/Launcher/Debug 
    * `algorithm-language` - Algorithm language selector - options CSharp, Python
    * `algorithm-type-name` - this is the name of the QCAlgorithm class you wrote in either C# or python as explained above.
    * `environment` - The config for the environment that will get run. Search for `live-alpaca` environment later in the example file. It'll mostly just be what I have for live trading. You can set paper for paper i think. Please research live source code to understand this fully?
    * `config.sh` - This is my config file for building the Docker container. It simply adds the variables for this Algo to a shell variable. Open to pull requests!
    * `Dockerfile_MyLeanAlgorithm` - This builds the docker file. Please add whatever stuff you need in here. For brokerages, you will need to copy and paste my line to comment out `ValidateSubscription()` from the Brokerage code and other stuff I have in there. Other than that I know I've added AWS, my own projects, several brokerages etc. This example shows you one brokerage, but it should at least get you up to  executing the algorithm script you put in `MyLeanAlgorithm.py`. Bitcoin and other wallet addresses above :')
    * `MyLeanAlgorithm.sh` - This is the final file that you will run using `bash MyLeanAlgorithm.sh` in a Linux shell to run the docker container that will run the lean algo. It contains cleanup code that cleans old containers with Lean executions that you canceled with Ctrl-C keyboard interrupts..If history is important, you will want to remove those. Crap this is only for Linux right now because it's a shell script. Open to pull requests lol 

That's it! Run your algorithm by going into it's directory and executing `bash MyLeanAlgorithm.sh`! You will see the magical Lean get instantiated locally if you did everything right and pay me at all my crypto wallets above.


# Step 0.0 - motivation


* money is a problem that can be solved - forest gump after pwning apple stock
* right approach for trading:
  * idea-> Backtest->live paper trade->live trade small->live trade big.
* `Probability of profit*avg profit - probability of loss*avg loss`=`your average trade profit or loss (pnl)`. If this is greater than all the commissions and fees, u become a money printing casino. Most important equation in trading. 
* Never trade with what you are not willing to lose completely.
* Limit the risk of unlimited loss potential and stick with limited loss potential trades(option spreads, crypto futures, buying margin rather than naked shorting)
* pigs get fat, hogs get ...
* ...

# Step 0.0.1 - STOP AND READ THIS
* instead of doing all this, u can pay like USD `$`1080/mo on quantconnect.com for an institution seat to run locally or $10/mo to run on their cloud servers which might cost more - 60/mo or something not sure. idc because i like my free on-premise live trading institution grade version below
* definitely review their pricing page: https://www.quantconnect.com/pricing u will have to click choose tier to see the options.
* u'll still need to write ur own algo. The config stuff, they take care of for you with their 'open source' lean-CLI
* also like install docker, set up vs code
* but U won't need my dockerfile stuff or brokerage stuff I have. They have backtesting in their lean-cli which is also open source but I have not cracked it yet - too much subscription code in it as opposed to one line in Brokerage code lol. 

# Step 0: Train and learn lean engine algo-writing
There's a [bootcamp](https://www.quantconnect.com/learning/course/1/Boot-Camp-101-US-Equities)
And tons of beautiful, [documentation](https://www.quantconnect.com/docs/v2) on the engine online with youtube videos, a [discord group](https://discord.gg/WrWdCewf) where Jared and his AI Mia Khalisi personally help you, [a class reference](https://www.lean.io/docs/v2/lean-engine/class-reference/classQuantConnect_1_1Algorithm_1_1QCAlgorithm.html), slack group?, etc.....Too much stuff to help you become experts at writing Lean algorithms but not at executing them :') - just remember my wallet addresses please

# Detailed Documentation
## Step 0.1: Install stuff

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
    * `pip install quantconnect-stubs`
  * in vs code press ctrl-shift-p or cmd-shift-p and select python interpreter: `.conda/envs/lean/python`

* Install docker desktop
  * look at docker desktop installation instructions for ubuntu or ur linux

* Install git
  * `apt install git`

* git clone my project: 
  * `git clone https://github.com/vrindger/actually_open_lean`

## Step 0.2: Decide what u want to trade and pick brokerages

* Think of a trading strategy u think will work. 
* Which instruments does it trade? stocks, options, futures, future options, spot crypto, derivative crypto
* Which brokerage do u want to use? https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages
* Identify lean brokerage github open source project: https://github.com/QuantConnect/ e.g. https://github.com/QuantConnect/Lean.Brokerages.Alpaca

## Step 1 - Create your own Dockerfile for running your engine
## - some things like which brokerage are set here. i added common ones i like

Look at the Dockerfile being used in my project such as: https://github.com/vrindger/lean/blob/main/Dockerfile_dev_debug
* u might want to use a different brokerage than the ones I've used, e.g:
```
 RUN git clone https://github.com/QuantConnect/Lean.Brokerages.Binance $BINANCE_DIR && \
    cp -rf $BINANCE_DIR/QuantConnect.BinanceBrokerage $LEAN_DIR && \
    cp -rf $BINANCE_DIR/QuantConnect.BinanceBrokerage.ToolBox $LEAN_DIR
```

This is the secret sauce to this project hahaha - commenting out one line in the brokerage code. Hope you don't change the name to that function @jaredbroad lol:
```
# Disable QuantConnect license check
RUN sed -i 's/^\s*ValidateSubscription();/\/\/&/' $LEAN_DIR/QuantConnect.AlpacaBrokerage/AlpacaBrokerage.cs 
```

## Step 2 - Create your own trading algo! U can copy mine but use your own brokerage keys etc

* Create a new dir in the lean_algos dir with your own config file and .py or .cs file for C#. 
* To create algo, look at the template dir under `lean_algos`

* `MyLeanAlgorithm` is my example algorithm using my config file(a `config.json`) which used to have my secret keys for my brokerage's paper account. The algorithm file is a .py file.

* Yes, u will need every single file - the json file, an algo file, Dockerfile AND the .sh bash files. this stuff is WIP


## Step 3 - Run bash script

`bash MyLeanAlgorithm.sh` 

# Random important notes:
* there's a `string` ticker for instruments like 'BTCUSDT' or 'GOOGL'. 
* then there's a Lean Symbol object created from that ticker if u specify US stock like so:  `Market Symbol.create('SPY', SecurityType.EQUITY, Market.USA)`. symbols don't contain very much info.
* then there's a `Security` that is added to the algorithm which contains the symbol and even more information like exchange and hours etc. It's the active `Security` that gets traded

* [In Lean, methods only (?not classes?, ManualUniverseSelectionModel) are automatically converted from camel case(C#) to snake case:](https://www.quantconnect.com/announcements/16830/pep8-python-api-migration/p1)
  * Snake case methods, and CamelCase classes:
    ```
    self.AddUniverseSelection(ManualUniverseSelectionModel(symbols)) 
    self.add_universe_selection(ManualUniverseSelectionModel(symbols))
     ```

# SEO

Cru-cru-cruisin'

I got my top down
And I'm ready to roll
Watch me go now (go now)
I'm leaving this town
To the Costa Del Sol
Come on, let's go now (go now)

The stars are out tonight
The moon is shining down on me
With rays of pure delight
And I'll be spendin'

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life

Cruisin', cruisin' down the street
Cruisin' up and down the street

You're my lover, you're my Romeo
Watch me glow now
Rockin' to the rhythm
On Venga Radio (Venga Radio)
Don't let go now (go now)

The stars are out tonight
The moon is shining down on me
With rays of pure delight
And I'll be spendin'

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life

Cruisin', cruisin' down the street
Cruisin' up and down the street
Cruisin', cruisin' down the street
Cruisin' up and down the street

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life

24-7 in my 911
And I ain't gonna work a 9 to 5
24-7 in my 911
On a highway to heaven
It's the time of my life
Source: Musixmatch

give me great search engine terms 100 for "actually open source quantconnect lean" someone might search for my new project's readme in github so they will find it

Alright, let's craft 100 search engine terms designed to maximize the visibility of your "actually open source QuantConnect LEAN" project on GitHub. We'll target a range of search intents, from general to highly specific.

General Open Source & QuantConnect:

    open source QuantConnect LEAN
    QuantConnect LEAN open source fork
    LEAN trading engine open source
    open source algorithmic trading platform LEAN
    free open source QuantConnect alternative
    QuantConnect LEAN community edition
    open source backtesting engine LEAN
    LEAN open source trading framework
    open source quant trading LEAN
    LEAN engine github open source

Specific LEAN & Project Features:

    fully open source QuantConnect LEAN
    truly open source LEAN engine
    unrestricted open source LEAN
    no limitations open source LEAN
    complete open source LEAN
    LEAN engine source code access
    LEAN open source contributions
    modified QuantConnect LEAN open source
    enhanced LEAN trading engine open source
    extended LEAN framework open source

GitHub & Repository Focused:

    LEAN engine github repository
    open source QuantConnect LEAN github
    github LEAN trading platform
    LEAN engine open source code github
    search github LEAN open source
    LEAN open source project github
    LEAN engine fork github
    github open source trading algorithm LEAN
    LEAN engine open source examples github
    github LEAN open source documentation

Problem Solving & Alternatives:

    QuantConnect LEAN limitations open source
    bypass QuantConnect restrictions open source
    alternative to QuantConnect LEAN open source
    free LEAN backtesting open source
    open source LEAN without cloud
    local LEAN engine open source
    self-hosted LEAN open source
    run LEAN locally open source
    QuantConnect LEAN cost open source
    solve LEAN limitations open source

Technical & Development:

    LEAN engine source code download
    compile LEAN engine open source
    modify LEAN engine source
    build LEAN engine from source
    LEAN engine development open source
    contribute to LEAN engine
    LEAN engine open source API
    LEAN engine open source plugins
    extend LEAN engine functionality
    LEAN engine open source libraries

Keywords + Specific Terms:

    "actually open source" LEAN
    "fully unlocked" LEAN engine
    "community maintained" LEAN
    "completely free" LEAN trading
    "no cloud required" LEAN
    LEAN engine "local execution"
    open source "algorithmic trading" LEAN
    LEAN "backtesting" open source
    "quant trading" LEAN github
    LEAN engine "source code" access

Long-Tail & Specific Queries:

    how to run QuantConnect LEAN locally open source
    where to find open source QuantConnect LEAN on github
    best open source alternative to QuantConnect LEAN
    LEAN engine open source with no API restrictions
    detailed documentation for open source LEAN engine
    community support for open source LEAN trading
    how to contribute to open source LEAN engine development
    LEAN engine open source with full source code access
    open source LEAN engine for advanced trading strategies
    step-by-step guide to compiling open source LEAN engine

Targeting Specific User Needs:

    open source LEAN for professional traders
    LEAN engine open source for researchers
    open source LEAN for students
    LEAN engine open source for hobbyists
    open source LEAN for quantitative analysts
    LEAN engine open source for developers
    LEAN open source for automated trading
    open source LEAN for backtesting strategies
    LEAN open source for custom indicators
    LEAN open source for market data analysis

Variations & Misspellings:

    quant connect open source
    lean engine open source code
    open source lean platform
    quant connect free
    lean trading engine free
    quant connect community
    opensource lean trading
    lean source code
    quantconnect github
    lean github

Adding Descriptive Terms:

    robust open source LEAN engine
    scalable open source LEAN trading
    customizable open source LEAN platform
    powerful open source LEAN framework
    flexible open source LEAN engine
    reliable open source LEAN backtesting
    efficient open source LEAN trading
    modern open source LEAN engine
    comprehensive open source LEAN documentation 100.active open source LEAN community

I'll be your dream, I'll be your wish, I'll be your fantasy
I'll be your hope, I'll be your love, be everything that you need
I love you more with every breath truly, madly, deeply do
I will be strong, I will be faithful 'cause I'm counting on

A new beginnin'
A reason for livin'
A deeper meaning, yeah

Well, I wanna stand with you on a mountain
I wanna bathe with you in the sea
I wanna lay like this forever
Until the sky falls down on me

And when the stars are shining brightly in the velvet sky
I'll make a wish, send it to heaven, then make you want to cry
The tears of joy for all the pleasure and the certainty
That we're surrounded by the comfort and protection

Of the highest powers
In lonely hours (lonely hours, girl)
The tears devour you

Well, I wanna stand with you on a mountain
I wanna bathe with you in the sea
I wanna lay like this forever
Until the sky falls down on me

Oh, can you see it, baby?
You don't have to close your eyes
It's standin' right before you
All that you need will surely come
Ooh-ooh-ooh, yeah

I'll be your dream, I'll be your wish, I'll be your fantasy
I'll be your hope, I'll be your love, be everything that you need
I'll love you more with every breath, truly, madly, deeply do
Mm

I wanna stand with you on a mountain
I wanna bathe with you in the sea
I wanna lay like this forever
Until the sky falls down on me
Well, I wanna stand with you on a mountain
I wanna bathe with you in the sea
I want to live like this forever
Until the sky falls down on me

Ooh-ooh-ooh, ooh-ooh-ooh-yeah
Ooh-ooh-ooh
La-la-di-da-yeah, da-yeah, la
La-la-di-da-yeah, da-yeah, la
Source: Musixmatch