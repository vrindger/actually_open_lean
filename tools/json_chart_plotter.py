import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime 

# Use this file to plot the json that gets generated when you create a chart in your Lean algorithm. 
# You will see the plot in the same dir as Lean inside the Docker container
# You will need to login to your Lean Docker container with a bash shell. So the command is `docker exec -it your_container_id /bin/bash`

def plot_stock_data(filepath):
    """
    Reads stock data from a JSON file and plots the specified series.

    Args:
        filepath: Path to the JSON file containing the stock data.
    """

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return

    series_data = data["charts"]["Combined Chart"]["series"]

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)  # sharex makes zooming synchronized

        # --- Plot price data (top subplot) ---
    for series_name in ["Low", "Close", "High", "Open", "VWAP"]:  # Plot all specified series
        if series_name in series_data:
            series = series_data[series_name]
            times, values = zip(*series["values"])
            # Convert epoch milliseconds to datetime objects, then to matplotlib dates
            times = [datetime.datetime.fromtimestamp(t / 1000) for t in times]
            times = mdates.date2num(times)
            ax1.plot(times, values, label=series["name"])

    ax1.set_ylabel(f"Price ({series_data.get('Low', {}).get('unit', '')})")  # Use unit from 'Low' series, if available
    ax1.set_title("Stock Price and Volume Over Time")
    ax1.legend()
    ax1.grid(True)

    # Format x-axis as dates
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()  # Rotate date labels for better readability


    # --- Plot volume data (bottom subplot) ---
    if "Volume" in series_data:
        volume_series = series_data["Volume"]
        times, volumes = zip(*volume_series["values"])
        # Convert epoch milliseconds to datetime objects, then to matplotlib dates
        times = [datetime.datetime.fromtimestamp(t / 1000) for t in times]
        times = mdates.date2num(times)
        ax2.bar(times, volumes, width=0.0005, label=volume_series["name"], color='skyblue') #Use bar chart, adjust width as needed
        ax2.set_ylabel(f"Volume ({volume_series.get('unit', '')})") # Use unit from "Volume", if available
        ax2.legend()
        ax2.grid(True)
        
        #Format the x axis the same way we format it for the price
        ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))


    plt.tight_layout()  # Adjust subplot parameters for a tight layout.
    plt.show()

# Example usage (replace with your file path):
filepath = "1357871701.json"  #put your filepath here
plot_stock_data(filepath)