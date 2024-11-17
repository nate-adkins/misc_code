import numpy as np
import matplotlib.pyplot as plt

grid_size = 100
cell_size = 1

grid_width_in_cells = int(grid_size / cell_size)  # Cast to integer

def pdf_function(x, y):
    return np.exp(-0.5 * (x**2 + y**2))

x_values = np.linspace(-grid_size/2, grid_size/2, grid_width_in_cells)
y_values = np.linspace(-5, 5, grid_width_in_cells)

pdf_values = np.zeros((len(y_values), len(x_values)))

for i, y in enumerate(y_values):
    for j, x in enumerate(x_values):
        pdf_values[i, j] = pdf_function(x, y)

plt.figure(figsize=(8, 6))
plt.imshow(pdf_values, cmap='viridis', extent=[x_values.min(), x_values.max(), y_values.min(), y_values.max()])
plt.colorbar(label='PDF Value')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('2D PDF Function')
plt.show()