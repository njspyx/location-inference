import os
import pandas as pd
from inspect_ai.dataset import Sample, MemoryDataset
from inspect_ai.model import ChatMessageUser, ContentText, ContentImage

def load_geolocation_dataset(csv_path: str, images_dir: str, sample_limit: int=None) -> MemoryDataset:
    """
    Load the geolocation dataset for Inspect.
    
    Args:
        csv_path: Path to dataset csv file
        images_dir: Directory containing the benchmark images
        sample_limit: [Optional] Number of samples to evaluate, default is entire dataset
        
    Returns:
        Dataset object containing samples
    """
    df = pd.read_csv(csv_path)
    if sample_limit:
        df = df.head(sample_limit)
    
    # Create samples
    samples = []
    for _, row in df.iterrows():
        # Get image path
        image_path = os.path.join(images_dir, row['filename'])
        if not os.path.exists(image_path):
            continue
        
        # Create init chat message
        input_message = ChatMessageUser(content=[
            ContentImage(image=image_path),
            ContentText(text="Determine the location of this image based on visual clues.")
        ])
        
        # Create target
        target = {
            'lat': row['lat'],
            'long': row['lng'],
            'city': row['city_name'],
            'country': row['country']
        }
        
        # Create the sample
        sample = Sample(
            input=[input_message],
            target=str(target),
            metadata={      # Add any addl metadata if needed
                'filename': row['filename'],
                'population_class': row.get('population_class', None)
            }
        )
        
        samples.append(sample)
    
    return MemoryDataset(samples)