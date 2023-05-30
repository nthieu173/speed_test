"""
Open a CSV file with the following columns:
Server ID,Sponsor,Server Name,Timestamp,Distance,Ping,Download,Upload,Share,IP Address

Plot both the Download, Upload on the Y axis and the Timestamp on the X axis with pyplot
"""

import csv
import sys
from datetime import datetime

import matplotlib.pyplot as plt


def main():
    """
    Main function
    """
    args = sys.argv[1:]

    if not args:
        print("usage: file_name")
        sys.exit(1)

    file_name = args[0]

    download = []
    upload = []
    seconds_timestamps = []

    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            download.append(float(row["Download"]) / 1000000)
            upload.append(float(row["Upload"]) / 1000000)
            seconds_timestamps.append(
                datetime.fromisoformat(row["Timestamp"]).timestamp()
            )

    plt.plot(seconds_timestamps, download, label="Download")
    plt.plot(seconds_timestamps, upload, label="Upload")

    # plot median
    plt.plot(
        seconds_timestamps,
        [sum(download) / len(download)] * len(download),
        label="Download median",
    )
    plt.plot(
        seconds_timestamps,
        [sum(upload) / len(upload)] * len(upload),
        label="Upload median",
    )

    first_time_to_date = datetime.fromtimestamp(seconds_timestamps[0])
    last_time_to_date = datetime.fromtimestamp(seconds_timestamps[-1])

    # Ticks every day to ISO format
    daily_ticks = [
        datetime.fromtimestamp(t).isoformat()
        for t in range(
            int(first_time_to_date.timestamp()),
            int(last_time_to_date.timestamp()),
            24 * 60 * 60,
        )
    ]

    plt.xticks(
        range(
            int(first_time_to_date.timestamp()),
            int(last_time_to_date.timestamp()),
            24 * 60 * 60,
        ),
        daily_ticks,
        rotation=45,
    )

    plt.xlabel("Time")
    plt.ylabel("Speed (Mbps)")
    plt.legend()

    # Save the plot to a file
    plt.savefig("plot.png")


if __name__ == "__main__":
    main()
