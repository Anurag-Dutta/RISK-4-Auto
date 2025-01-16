import numpy as np
import matplotlib.pyplot as plt
import os

file_path = r"R_RPM_raw.npy" # Check accordingly
data = np.load(file_path)

output_folder = r"R_RPM_histograms" # Check accordingly
os.makedirs(output_folder, exist_ok=True)

rows_per_image = 256
num_rows = data.shape[0]

for start_idx in range(0, num_rows, rows_per_image):
    end_idx = min(start_idx + rows_per_image, num_rows)
    combined_data = data[start_idx:end_idx]

    print(f"Creating 2D histogram image for rows {start_idx} to {end_idx - 1}")
    
    combined_data_normalized = combined_data.astype(np.float32)
    combined_data_max = combined_data_normalized.max(axis=0)
    combined_data_max[combined_data_max == 0] = 1
    combined_data_normalized /= combined_data_max

    combined_data_normalized *= 255
    combined_data_normalized = combined_data_normalized.astype(np.uint8)

    plt.figure(figsize=(25, 25))
    plt.imshow(combined_data_normalized, cmap='binary', aspect='auto', interpolation='nearest')

    output_file = os.path.join(output_folder, f"2d_histogram_{start_idx}_{end_idx - 1}.png")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()