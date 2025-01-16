import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def export_dataset(dataset, flag_value):
    np.save(f"{flag_value}_RPM_raw.npy", dataset) # Name accordingly
    print(f"Dataset shape: {dataset.shape}")

def session_2d_histogram(ts_mask, sizes_mask):
    data_values = sizes_mask
    hist, bin_edges = np.histogram(data_values, bins=256, range=(0, 255))
    return hist

def traffic_csv_converter(file_path):
    print("Running on " + file_path)
    session_data = {'R': [], 'T': []}
    counter = 0

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            can_id = row[1]
            length = int(row[2])
            data_values = [int(x, 16) for x in row[3:3+length]]
            flag_value = row[-1]

            if flag_value not in session_data:
                continue

            ts = float(row[0])
            h = session_2d_histogram(ts, data_values)

            session_data[flag_value].append(h)
            
            counter += 1
            if counter % 100 == 0:
                print(f"Processed {counter} rows")

    for flag_value, dataset in session_data.items():
        if dataset:
            session_array = np.asarray(dataset)
            export_dataset(session_array, flag_value)

def plot_histogram(data, bins=10):
    plt.hist(data, bins=bins, range=(0, 255), alpha=0.75)
    plt.title('Histogram of Data Values')
    plt.xlabel('Data Value')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == '__main__':
    input_file_path = r"RPM_dataset.csv"  # Check accordingly
    traffic_csv_converter(input_file_path)