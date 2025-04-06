import math
from typing import Dict, Any, List, Union


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

def get_cardinal_direction(heading):
    """Convert heading degrees to cardinal direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(heading / 45) % 8
    return directions[index]

def extract_coordinates(text: str) -> Union[Dict[str, Any], None]:
    """
    Extract coordinates from model output. Looks for JSON structure.
    
    Args:
        text: Model output text to extract from
        
    Returns:
        Dictionary with lat, long, city, country if found, None otherwise
    """
    try:
        # Try to find JSON structure in the text
        match = re.search(r'({.*?})', text, re.DOTALL)
        if match:
            json_str = match.group(1)
            data = json.loads(json_str)
            
            # Validate structure
            if 'lat' in data and 'long' in data:
                return {
                    'lat': float(data['lat']),
                    'long': float(data['long']),
                    'city': data.get('city', ''),
                    'country': data.get('country', '')
                }
    
    except (json.JSONDecodeError, ValueError, TypeError):
        try:
            lat_match = re.search(r'lat(?:itude)?[\s:]+(-?\d+\.?\d*)', text, re.IGNORECASE)
            long_match = re.search(r'long(?:itude)?[\s:]+(-?\d+\.?\d*)', text, re.IGNORECASE)
            
            if lat_match and long_match:
                country_match = re.search(r'country[\s:]+([A-Za-z\s]+)', text, re.IGNORECASE)
                city_match = re.search(r'city[\s:]+([A-Za-z\s]+)', text, re.IGNORECASE)
                
                return {
                    'lat': float(lat_match.group(1)),
                    'long': float(long_match.group(1)),
                    'city': city_match.group(1).strip() if city_match else '',
                    'country': country_match.group(1).strip() if country_match else ''
                }
        except Exception:
            pass
    
    return None