import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.ndimage import gaussian_filter
import random

# Constants
SPEED_OF_LIGHT = 3e8  # m/s

# Generate mountainous terrain using Gaussian smoothing
def generate_mountainous_terrain(size=(100, 100), num_islands=10, island_radius=15, smoothing=5, high_value=255, low_value=0):
    # Create a 2D array filled with low values (0)
    terrain = np.full(size, low_value)
    
    # Randomly place islands in the terrain
    for _ in range(num_islands):
        x_center = random.randint(0, size[0] - 1)
        y_center = random.randint(0, size[1] - 1)
        
        for x in range(size[0]):
            for y in range(size[1]):
                # Calculate distance from island center
                distance = np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
                # If within the island radius, set a high value
                if distance <= island_radius:
                    terrain[x, y] += high_value

    # Apply Gaussian filter to smooth the edges
    terrain = gaussian_filter(terrain, sigma=smoothing)
    
    # Normalize terrain values to be between low_value and high_value
    terrain = np.clip(terrain, low_value, high_value)

    return terrain.astype(np.uint8)  # Ensure values are in the range of 0-255


# Calculate free-space path loss (FSPL)
def free_space_path_loss(d, frequency):
    return 20 * np.log10(d) + 20 * np.log10(frequency) - 147.55

# Simple dipole antenna gain function (vertical pattern)
def dipole_gain(elevation_angle):
    return np.sin(elevation_angle)

# Calculate the azimuth and elevation angle between the transmitter and receiver
def calculate_azimuth_elevation(tx_coords, rx_coords):
    dx = rx_coords[0] - tx_coords[0]
    dy = rx_coords[1] - tx_coords[1]
    dz = rx_coords[2] - tx_coords[2]
    
    azimuth = np.arctan2(dy, dx)  # Horizontal angle
    distance = np.sqrt(dx**2 + dy**2)
    elevation = np.arctan2(dz, distance)  # Vertical angle (elevation)
    
    return azimuth, elevation

# Compute signal strength with antenna pattern and terrain elevation
def signal_strength(tx_coords, rx_coords, frequency, terrain_map, antenna_gain_function):
    tx_x, tx_y = tx_coords[:2]
    rx_x, rx_y = rx_coords[:2]
    
    # Distance between transmitter and receiver
    d = euclidean(tx_coords[:2], rx_coords[:2])
    
    # Calculate FSPL (Free-Space Path Loss)
    fspl = free_space_path_loss(d, frequency)
    
    # Get the elevation at the receiver (z-coordinates for tx and rx)
    tx_elev = terrain_map[int(tx_y), int(tx_x)]
    rx_elev = terrain_map[int(rx_y), int(rx_x)]
    
    # Calculate azimuth and elevation angles
    azimuth, elevation_angle = calculate_azimuth_elevation(
        (tx_x, tx_y, tx_elev), (rx_x, rx_y, rx_elev)
    )
    
    # Apply antenna gain based on the elevation angle
    gain = antenna_gain_function(elevation_angle)
    
    # Final signal strength after accounting for gain
    signal = fspl - gain
    return signal

# Generate signal strength map over the terrain
def generate_signal_map(tx_coords, frequency, terrain_map, antenna_gain_function):
    height, width = terrain_map.shape
    signal_map = np.zeros((height, width))
    
    for i in range(height):
        for j in range(width):
            # Compute the real-world coordinates for each pixel
            rx_coords = (j, i, terrain_map[i, j])
            
            # Calculate signal strength at each point
            signal_map[i, j] = signal_strength(tx_coords, rx_coords, frequency, terrain_map, antenna_gain_function)
    
    return signal_map

# Visualize the signal strength map
def plot_signal_map(signal_map, terrain_map):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot the terrain map
    ax[0].imshow(terrain_map, cmap='gray')
    ax[0].set_title('Terrain Map (Height values 0-255)')
    
    # Plot the signal strength map
    signal_plot = ax[1].imshow(signal_map, cmap='inferno')
    ax[1].set_title('Signal Strength Map (dB)')
    
    # Add colorbars
    fig.colorbar(ax[0].imshow(terrain_map, cmap='gray'), ax=ax[0])
    fig.colorbar(signal_plot, ax=ax[1])
    
    plt.show()

# Main function to run the simulation
def main():
    # Generate a mountainous terrain map (height values from 0 to 255)
    height, width = 100, 100  # Define the size of the terrain
    terrain_map = generate_mountainous_terrain((height, width))
    
    # Transmitter coordinates (x, y, elevation)
    tx_coords = (50, 50, terrain_map[50, 50])  # Example transmitter position
    
    # Set the frequency (in MHz)
    frequency = 900e6  # Example: 900 MHz
    
    # Generate the signal map
    signal_map = generate_signal_map(tx_coords, frequency, terrain_map, dipole_gain)
    
    # Plot the result
    plot_signal_map(signal_map, terrain_map)

# Run the script
if __name__ == '__main__':
    main() 