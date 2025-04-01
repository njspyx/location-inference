import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two sets of coordinates using the Haversine formula.
    
    Args:
        lat1 (float): Latitude of the first set of coordinates.
        lon1 (float): Longitude of the first set of coordinates.
        lat2 (float): Latitude of the second set of coordinates.
        lon2 (float): Longitude of the second set of coordinates.
        
    Returns:
        float: The distance between the two sets of coordinates in kilometers.
    """
    R = 6371  # Earth's radius in kilometers
    
    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Calculate the Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance