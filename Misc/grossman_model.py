import numpy as np
import matplotlib.pyplot as plt

def draw_grossman_ppf():
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Generate points for the PPF curve
    # Using a quadratic curve instead of circular arc for better shape
    x = np.linspace(1, 5, 100)
    y = 5 * np.sqrt(1 - ((x-1)/4)**2)  # Modified equation for better curve shape
    
    # Plot the PPF curve
    ax.plot(x, y, 'b-', linewidth=2)
    
    # Add Hmin point
    ax.plot([1], [0], 'ko', label='Hmin')
    
    # Add points A through E along the curve
    points = [(1, 0), (1.8, 2), (2.5, 3), (3.5, 2), (5, 0)]
    labels = ['A', 'B', 'C', 'D', 'E']
    for (x, y), label in zip(points, labels):
        ax.plot(x, y, 'k.', markersize=8)
        ax.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points')
    
    # Add labels
    ax.set_xlabel('H', fontsize=12)
    ax.set_ylabel('Z', fontsize=12)
    
    # Set axis ranges
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    
    # Add Hmin label
    ax.annotate('Hmin', xy=(1, -0.2), ha='center')
    
    # Keep aspect ratio equal
    ax.set_aspect('equal')
    
    # Show grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    plt.show()

# Call the function to create the plot
draw_grossman_ppf()