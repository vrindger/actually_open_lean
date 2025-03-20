export LEAN_CONFIG_FILE="config.json"
export ALGO_FILE="scratch.py"

# Print the variables to /etc/environment with proper quotes
echo "ALGO_FILE=\"$ALGO_FILE\"" >> /etc/environment
echo "LEAN_CONFIG_FILE=\"$LEAN_CONFIG_FILE\"" >> /etc/environment