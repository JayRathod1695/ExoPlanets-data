import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the cleaned dataset (replace this with your actual cleaned CSV path)
csv_file_path = r"C:\Users\Dell\Documents\hackathon\ExoPlanets-data.csv"
df = pd.read_csv(csv_file_path)

# Define a function to create a 3D model of a planet
def create_3d_planet(radius, name="Exoplanet"):
    """Create a 3D model of a planet using its radius."""
    # Create a mesh for the sphere (planet)
    phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0*np.pi:100j]
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    # Plotting the sphere
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Surface plot
    ax.plot_surface(x, y, z, color='b', rstride=5, cstride=5, alpha=0.7)

    # Labels and title
    ax.set_title(f"3D Model of {name}")
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Set equal aspect ratio for all axes
    ax.set_box_aspect([1, 1, 1])

    # Show the plot
    plt.show()

# Function to generate 3D models for all planets in the dataset
def generate_planet_models(df):
    """Generate 3D models for all exoplanets based on their radius."""
    for index, row in df.iterrows():
        pl_name = row['pl_name'] if 'pl_name' in row else f'Exoplanet_{index}'
        pl_radius = row['pl_rade']  # Planetary radius in Earth radii

        if pd.isna(pl_radius):
            continue  # Skip if radius is missing

        # Call the 3D model function with the planet's name and radius
        create_3d_planet(radius=pl_radius, name=pl_name)

# Main execution
if __name__ == "__main__":
    # Generate 3D models for exoplanets
    generate_planet_models(df)
