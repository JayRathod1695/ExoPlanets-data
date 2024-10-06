import pandas as pd

# Load the cleaned dataset (replace this with your actual cleaned CSV path)
csv_file_path = r"C:\Users\Dell\Documents\hackathon\ExoPlanets-data.csv"
df = pd.read_csv(csv_file_path)
df=df.dropna()
print(df)
print(df.shape)

# Define a function to calculate the SNR
def calculate_snr(R_star, R_planet, D, E_S, P_S, SNR0=100):
    """Calculate the Signal-to-Noise Ratio (SNR)."""
    try:
        return SNR0 * ((R_star * R_planet * (D / 6)) / ((E_S / 10) * P_S)) ** 2
    except ZeroDivisionError:
        return None  # Handle division by zero if any parameters are zero

# Define a function to filter exoplanets based on user-defined telescope diameter
def filter_exoplanets(df, telescope_diameter):
    """Filter exoplanets that can be characterized based on SNR and distance."""
    filtered_exoplanets = []

    for index, row in df.iterrows():
        # Retrieve necessary parameters, handling missing values
        R_star = row.get('st_rad', None)         # Host star radius (in solar radii)
        R_planet = row.get('pl_rade', None)      # Planetary radius (in Earth radii)
        E_S = row.get('sy_dist', None)           # Distance to the exoplanet (in parsecs)
        P_S = row.get('pl_orbsmax', None)        # Planet-star distance (in AU)
        
        # Ensure all required values are present and valid
        if None in [R_star, R_planet, E_S, P_S] or 0 in [R_star, R_planet, E_S, P_S]:
            continue  # Skip rows with missing or invalid data
        
        D = telescope_diameter  # Telescope diameter (in meters)

        # Calculate SNR
        snr = calculate_snr(R_star, R_planet, D, E_S, P_S)

        # Append to the list if SNR > 5
        if snr is not None and snr > 5:
            filtered_exoplanets.append(row)

    # Convert the list of filtered rows to a DataFrame with all columns
    return pd.DataFrame(filtered_exoplanets, columns=df.columns)

# Main execution
if __name__ == "__main__":
    # User input for telescope diameter
    telescope_diameter = float(input("Enter the telescope diameter (in meters, e.g., 6): "))

    # Filter exoplanets based on the given telescope diameter
    filtered_exoplanets = filter_exoplanets(df, telescope_diameter)

    # Display the results
    print("\nFiltered Exoplanets with SNR > 5:")
    print(filtered_exoplanets)  # Modify as needed

    # Optionally, save the filtered results to a new CSV
    filtered_csv_path = r"C:\Users\Dell\Documents\hackathon\Filtered_ExoPlanets-data.csv"
    filtered_exoplanets.to_csv(filtered_csv_path, index=False)
    print(f"\nFiltered exoplanets saved to {filtered_csv_path}")
