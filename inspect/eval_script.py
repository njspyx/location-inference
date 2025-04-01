import os
from inspect_ai import Task, eval, task
from inspect_ai.solver import generate

from dataset import load_geolocation_dataset
from solver import geolocation_prompt
from scorer import geolocation_distance

@task
def geolocation_benchmark(csv_path: str, imgs_dir: str, sample_limit: int=None) -> Task:
    """
    Benchmark task for evaluating single-image geolocation.
    
    Args:
        csv_path: Path to dataset csv file
        images_dir: Directory containing the benchmark images
        limit: [Optional] Number of samples to evaluate, default is entire dataset
    
    Returns:
        Inspect benchmark task object
    """
    # load dataset, solver, and scorer
    dataset = load_geolocation_dataset(csv_path, imgs_dir, sample_limit)
    solver = [
        geolocation_prompt(),
        generate()
    ]
    scorer = geolocation_distance()
    
    return Task(
        dataset=dataset,
        solver=solver,
        scorer=scorer,
    )

if __name__ == "__main__":
    # Default path for dataset dir, change if needed
    DATASET_PATH = "../geolocation-inference-dataset"
    
    CSV_PATH = DATASET_PATH+"/img_coordinates_final_v1_with_country.csv"
    IMAGES_DIR = DATASET_PATH+"/imgs_final"
    
    # Set to limit number of samples evaluated
    SAMPLE_LIMIT = 5
    
    # Set environment variables here or in bash
    # os.environ["OPENAI_API_KEY"] = _
    
    # Run
    log = eval(
        geolocation_benchmark(CSV_PATH, IMAGES_DIR, SAMPLE_LIMIT),
        model="openai/gpt-4o", # CHANGE MODEL HERE
        log_dir="logs"
    )
    
    # print(f"Mean distance: {log.results.metrics.get('mean_distance')} km")
    # print(f"Median distance: {log.results.metrics.get('median_distance')} km")
    # print(f"Country accuracy: {log.results.metrics.get('accuracy') * 100:.2f}%")
    # print(f"City accuracy: {log.results.metrics.get('city_accuracy') * 100:.2f}%")
    
    # print(f"Inspect logs saved at: {log.path}")
    print(f"Run `inspect view --log-dir logs --port 7575`")