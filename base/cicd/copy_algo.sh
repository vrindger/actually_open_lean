#!/bin/bash
source /etc/environment

# Debugging information
echo "Algorithm file: $ALGO_FILE"
echo "LEAN_DIR: $LEAN_DIR"

conf_dir=$LEAN_CONFIG_BASE/

if [[ $ALGO_FILE == *.py ]]; then
    echo "Copying Python algorithm to $LEAN_DIR/Algorithm.Python"
    cp $conf_dir/$ALGO_FILE $LEAN_DIR/Algorithm.Python
elif [[ $ALGO_FILE == *.cs ]]; then
    echo "Copying C# algorithm to $LEAN_DIR/Algorithm.CSharp"
    cp $conf_dir/$ALGO_FILE $LEAN_DIR/Algorithm.CSharp
else
    echo "Unsupported algorithm file type: $ALGO_FILE"
    exit 1
fi

cp $conf_dir/$LEAN_CONFIG_FILE $LEAN_DIR/Launcher/config.json