import pandas as pd

# Path to your downloaded CSV file
csv_file_path = r"C:\Users\Priyansh Madhu\OneDrive\Documents\Hackathon\ExoPlanets-data.csv"
df = pd.read_csv(csv_file_path)

# Clean up column names
df.columns = df.columns.str.strip()

# Define the thresholds for habitability and observability
INSOLATION_THRESHOLD_LOW = 0.8  # Lower threshold for insolation (in Earth units)
INSOLATION_THRESHOLD_HIGH = 1.5  # Upper threshold for insolation (in Earth units)
RADIUS_THRESHOLD = 1.6  # Upper threshold for planet radius (in Earth radii)
EQUILIBRIUM_TEMPERATURE_MIN = 273  # Minimum temperature for habitability (in Kelvin)
EQUILIBRIUM_TEMPERATURE_MAX = 323  # Maximum temperature for habitability (in Kelvin)
DISTANCE_THRESHOLD = 100  # Distance in parsecs for observability
SNR_THRESHOLD = 5  # Threshold for signal-to-noise ratio

def calculate_snr(R_star, R_planet, D, E_S, P_S, SNR0=100):
    """Calculate the signal-to-noise ratio based on the given parameters."""
    return SNR0 * ((R_star * R_planet * (D / 6)) / ((E_S / 10) * P_S)) ** 2

def is_observable_and_habitable(row):
    insolation = row['pl_insol']
    radius = row['pl_rade']
    eq_temp = row['pl_eqt']
    distance = row['sy_dist']
    eccentricity = row['pl_orbeccen']
    R_star = row['st_rad']  # Star radius
    R_planet = row['pl_rade']  # Planet radius
    D = 6.0  # Telescope diameter in meters (example value)
    E_S = row['sy_dist']  # Star distance in parsecs
    P_S = row['pl_orbsmax']  # Semi-major axis in AU (assuming this is the correct column)

    # Calculate the SNR
    snr = calculate_snr(R_star, R_planet, D, E_S, P_S)

    # Check for observability and habitability
    is_observable = distance < DISTANCE_THRESHOLD and snr > SNR_THRESHOLD
    is_habitable = (INSOLATION_THRESHOLD_LOW <= insolation <= INSOLATION_THRESHOLD_HIGH and
                    radius <= RADIUS_THRESHOLD and
                    EQUILIBRIUM_TEMPERATURE_MIN <= eq_temp <= EQUILIBRIUM_TEMPERATURE_MAX and
                    eccentricity < 0.1)  # Assume low eccentricity for habitability

    return is_observable and is_habitable

# Filter the DataFrame for observable and habitable exoplanets
df['observable_habitable'] = df.apply(is_observable_and_habitable, axis=1)
filtered_exoplanets = df[df['observable_habitable']]

# Display the filtered results
print("Observable and potentially habitable exoplanets:")
print(filtered_exoplanets[['pl_name', 'hostname', 'sy_dist', 'pl_rade', 'pl_insol', 'pl_eqt', 'st_rad', 'pl_orbsmax']])

