# Ray
# Created By: 2023-05-08
# Description: This is a python program to calculate standard deviation on a 10 second basis from an input file
import gzip
import json
import numpy as np
import csv
import time

def calculate_std(prices):
    return np.std(prices)

def process_file(input_filename, output_filename):
    """method to process the data: including reading from input, calculate for every 10 second, and write it into output file

    Args:
        input_filename (string): input file's path
        output_filename (string): output file's path
    """
    #provided code to read gzip file
    with gzip.open(input_filename, mode="rt") as f, open(output_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["timestamp", "std"])

        current_timestamp = None
        next_timestamp = None
        prices = []

        for row in f:
            parsed = json.loads(row.rstrip("\n"))
            timestamp_ms_received, price = parsed[0], parsed[2]
            
            #First current_timestamp is None
            if current_timestamp is None:
                # here I rounded the second to the ten-second decimal, which means 1658361610180 become 1658361610000, if this is undesirable, comment the next line and uncomment the line after that.
                current_timestamp = (timestamp_ms_received // 10000) * 10000
                # current_timestamp = timestamp_ms_received
                next_timestamp = current_timestamp + 10000
                
            #Between each 10 second gap
            if timestamp_ms_received < next_timestamp:
                prices.append(price)
            #Next 10 second
            else:
                std = calculate_std(prices)
                csv_writer.writerow([current_timestamp, std])
                
                current_timestamp = next_timestamp
                next_timestamp = current_timestamp + 10000
                prices = [price]

if __name__ == "__main__":
    input_filename = "tf-binance-BTC_ETH-2022-07-21.gz"
    output_filename = "output.csv"
    
    start_time = time.time()
    process_file(input_filename, output_filename)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    # 0.87 seconds, time complexity: O(n), n is the number of lines of input file
