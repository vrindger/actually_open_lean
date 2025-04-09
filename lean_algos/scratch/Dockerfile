#
#   LEAN Docker Container 20200522
#   Cross platform deployment for multiple brokerages
#

# Use base system
FROM quantconnect/lean:foundation
LABEL name="lean"

RUN apt-get install -y git

ENV BASE_DIR=/base
ENV CICD_DIR=$BASE_DIR/cicd
ENV CODE_DIR=$BASE_DIR/src
ENV LEAN_DIR=$CODE_DIR/Lean
ENV LEAN_RELEASE_DIR=$CODE_DIR/Lean/Launcher/bin/Release
ENV LEAN_DEBUG_DIR=$CODE_DIR/Lean/Launcher/bin/Debug
ENV ALPACA_DIR=$CODE_DIR/Lean.Brokerages.Alpaca


COPY ./base /base/
# Set GitHub username and PAT as build arguments
ARG GITHUB_USERNAME
ARG GITHUB_PAT

# Run the Git configuration script
RUN chmod +x $CICD_DIR/configure_git.sh && $CICD_DIR/configure_git.sh $GITHUB_USERNAME $GITHUB_PAT


# Set working directory to CODE_DIR
WORKDIR $CODE_DIR 

# Clone Lean repository
COPY ./base/Lean $LEAN_DIR
# RUN git clone https://github.com/QuantConnect/Lean $LEAN_DIR

# Clone and copy brokerage addons
RUN git clone https://github.com/QuantConnect/Lean.Brokerages.Alpaca $ALPACA_DIR && \
    cp -rf $ALPACA_DIR/QuantConnect.AlpacaBrokerage $LEAN_DIR

# Disable QuantConnect license check
RUN sed -i 's/^\s*ValidateSubscription();/\/\/&/' $LEAN_DIR/QuantConnect.AlpacaBrokerage/AlpacaBrokerage.cs 

# Lean customizations
RUN echo log.txt >> $LEAN_DIR/.gitignore

# Add projects
WORKDIR $LEAN_DIR/Launcher
RUN dotnet add reference ../QuantConnect.AlpacaBrokerage/QuantConnect.AlpacaBrokerage.csproj 

WORKDIR $LEAN_DIR
RUN dotnet sln add QuantConnect.AlpacaBrokerage/*csproj && \
    dotnet sln remove Tests/*csproj


# Build the Launcher Lean project which builds everything it needs to build
RUN dotnet build -c Debug Launcher

# Copy the algo and config files 
COPY algo.py $BASE_DIR
COPY config.json $BASE_DIR

# Set the entrypoint
WORKDIR $LEAN_DEBUG_DIR
ENTRYPOINT ["dotnet", "QuantConnect.Lean.Launcher.dll"]