import os
import requests
import tempfile
from io import BytesIO
from PIL import Image
from inspect_ai.tool import tool, ToolError
from inspect_ai.util import sandbox, StoreModel, store_as
from pydantic import Field, BaseModel
from typing import Optional, Dict, List, Any, Tuple

from utils import get_cardinal_direction

class StreetViewState(StoreModel):
    """
    Store for state/history of Street View API calls.
    """
    init_heading: float = Field(default=0.0)
    init_pitch: float = Field(default=0.0)
    history: List[Dict[str, Any]] = Field(default_factory=list)
    img_paths: List[str] = Field(default_factory=list)

@tool
def street_view_api(api_key: str, instance: str=None):
    
    async def execute(lat: float, lng: float, heading: float = 0, pitch: float = 0, fov: float = 90) -> str:
        """
        Fetches image from Google Street View Static API.
        
        Returns:
            str: Image path
        """
        
        if not api_key:
            raise ToolError("Google Maps API key is not provided.")
        sv_state =store_as(StreetViewState, instance=instance)
        
        # construct url request
        url = f"https://maps.googleapis.com/maps/api/streetview?size=640x640&radius=500&location={lat},{lng}&fov=100&heading={heading}&pitch={pitch}&key={api_key}"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise ToolError(f"Failed to fetch image: {response.status_code} - {response.content}")
            
            # save image to temp file and get path to return
            img = Image.open(BytesIO(response.content))
            temp_dir = "output"
            os.makedirs(temp_dir, exist_ok=True)
            img_path = os.path.join(temp_dir, f"{lat}_{lng}_{heading}_{pitch}.jpg")
            img.save(img_path)
            
            # save view metadata to store
            sv_state.img_paths.append(img_path)
            sv_state.history.append({
                'lat': lat,
                'lng': lng,
                'heading': heading,
                'pitch': pitch,
                'cardinal_direction': get_cardinal_direction(heading)
            })
            
            return img_path
            
        except Exception as e:
            raise ToolError(f"Error fetching image: {str(e)}")
    
    return execute
    
    
    
    