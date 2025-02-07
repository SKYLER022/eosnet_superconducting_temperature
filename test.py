import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Enable \mathrm in matplotlib LaTex mode
#mpl.rcParams['text.usetex'] = True

# Read the CSV file without headers
data = pd.read_csv('train_results.csv', header=None)

# Assign columns
struct_name = data.iloc[:, 0]  # 1st column
y_true = data.iloc[:, 1]  # 2nd column
y_predict = data.iloc[:, 2]  # 3rd column

# Define a threshold for outliers
threshold = 3 * np.std(y_true - y_predict)  # Example: 3 standard deviations

# Filter out outliers
mask = np.abs(y_true - y_predict) <= threshold
struct_name_filtered = struct_name[mask]
y_true_filtered = y_true[mask]
y_predict_filtered = y_predict[mask]

# Calculate new Mean Absolute Error (MAE)
mae_filtered = np.mean(np.abs(y_true_filtered - y_predict_filtered))

# Calculate the point density
x = y_true_filtered.values
y = y_predict_filtered.values
xy = np.vstack([x, y])
z = gaussian_kde(xy)(xy)

# Scale z to represent actual number of data points
z = z * len(x)

# Create custom colormap
colors = ['black', 'red', 'yellow']
n_bins = 100
cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]

# Determine the range for the axes
min_val = min(x.min(), y.min()) - 1
max_val = max(x.max(), y.max()) + 1

# Create the scatter plot with density-based coloring
fig, ax = plt.subplots(figsize=(8, 8))  # Square figure
scatter = ax.scatter(x, y, c=z, cmap=cmap, norm=mpl.colors.LogNorm(), s=20, marker='s')
ax.plot([min_val, max_val], [min_val, max_val], color='black', linestyle='dashed', linewidth=1)

# Set the same range for x and y axes
ax.set_xlim(min_val, max_val)
ax.set_ylim(min_val, max_val)

# Ensure aspect ratio is 1 (square plot)
ax.set_aspect('equal', adjustable='box')

# Set major ticks to integers with a difference of 2
xticks = np.arange(np.floor(min_val)+1, np.ceil(max_val), 2)
yticks = np.arange(np.floor(min_val)+1, np.ceil(max_val), 2)

ax.set_xticks(xticks)
ax.set_yticks(yticks)

# Set font size for tick labels
ax.tick_params(axis='both', which='major', labelsize=18)

# Remove grid lines
ax.grid(False)

# Show ticks without labels on top x-axis and right y-axis
ax.tick_params(axis='x', top=True, labeltop=False, direction='in')
ax.tick_params(axis='y', right=True, labelright=False, direction='in')

# Create a divider for existing axes instance
divider = make_axes_locatable(ax)

# Add an axes to the right of the main axes
cax = divider.append_axes("right", size="5%", pad=0.1)

# Add colorbar
cbar = fig.colorbar(scatter, cax=cax)
# cbar.set_label('Counts', rotation=90, labelpad=20, fontsize=18)
cbar.ax.tick_params(labelsize=18)

# Ensure bottom and top ticks are included
cbar.ax.tick_params(which='both', direction='out')  # Ensure ticks point outward

# Add labels and title
ax.set_xlabel('Calculated' + ' Tc ' + 'K', fontsize=20)
ax.set_ylabel('Predicted' + ' Tc ' +  'K', fontsize=20)
ax.set_title(f'MAE: {mae_filtered:.3f}', fontsize=20)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Save the plot as a PDF
plt.savefig('test_plot.pdf', format='pdf')

# Save the plot as a PNG with 600 dpi
plt.savefig('test_plot.png', format='png', dpi=600)

# Show the plot
plt.show()

# Create a new DataFrame with filtered data
filtered_data = pd.DataFrame({
    'Structure': struct_name_filtered,
    'True_Value': y_true_filtered,
    'Predicted_Value': y_predict_filtered
})

# Save the filtered data to a new CSV file
filtered_data.to_csv('filtered_test_results.csv', index=False, header=False,
                     float_format=lambda x: f'{x:.15f}')
