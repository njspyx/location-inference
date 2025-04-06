import json
import re
import math
import ast
from typing import Dict, Any, List, Union
from inspect_ai.scorer import scorer, Scorer, Score, SampleScore, Target, metric, Metric
from inspect_ai.scorer import CORRECT, INCORRECT
from inspect_ai.solver import TaskState

from utils import extract_coordinates

from utils import calculate_distance

@metric
def mean_distance() -> Metric:
    """
    Compute the mean distance error across all samples.
    """
    def compute_metric(scores: List[SampleScore]) -> float:
        distances = []
        for score in scores:
            if score.score.metadata and 'distance' in score.score.metadata:
                distance = score.score.metadata['distance']
                if isinstance(distance, (int, float)) and not math.isinf(distance):
                    distances.append(distance)
        
        if not distances:
            return float('inf')
        return sum(distances) / len(distances)
    
    return compute_metric


@metric
def median_distance() -> Metric:
    """
    Compute the median distance error across all samples.
    """
    def compute_metric(scores: List[SampleScore]) -> float:
        distances = []
        for score in scores:
            if score.score.metadata and 'distance' in score.score.metadata:
                distance = score.score.metadata['distance']
                if isinstance(distance, (int, float)) and not math.isinf(distance):
                    distances.append(distance)
        
        if not distances:
            return float('inf')
        
        sorted_distances = sorted(distances)
        n = len(sorted_distances)
        if n % 2 == 0:
            return (sorted_distances[n//2-1] + sorted_distances[n//2]) / 2
        else:
            return sorted_distances[n//2]
    
    return compute_metric


@metric
def country_accuracy() -> Metric:
    """
    Compute the country prediction accuracy across all samples.
    """
    def compute_metric(scores: List[SampleScore]) -> float:
        country_correct_count = 0
        total = 0
        
        for score in scores:
            if score.score.metadata and 'country_correct' in score.score.metadata:
                country_correct_count += 1 if score.score.metadata['country_correct'] else 0
                total += 1
        
        if total == 0:
            return 0.0
        return country_correct_count / total
    
    return compute_metric


@metric
def city_accuracy() -> Metric:
    """
    Compute the city prediction accuracy across all samples.
    """
    def compute_metric(scores: List[SampleScore]) -> float:
        city_correct_count = 0
        total = 0
        
        for score in scores:
            if score.score.metadata and 'city_correct' in score.score.metadata:
                city_correct_count += 1 if score.score.metadata['city_correct'] else 0
                total += 1
        
        if total == 0:
            return 0.0
        return city_correct_count / total
    
    return compute_metric


@scorer(metrics=[mean_distance(), median_distance(), country_accuracy(), city_accuracy()])
def geolocation_distance() -> Scorer:
    """
    Custom scorer that calculates Haversine distance error between predicted and actual coordinates.
    Also evaluates country and city accuracy.
    """
    
    async def score(state: TaskState, target: Target) -> Score:
        """
        Score a single sample.
                
        Returns:
            Score object with score and metadata
        """
        # get vars
        answer = state.output.completion
        try:
            target_data = ast.literal_eval(target.text)
        except:
            return Score(
                value=INCORRECT,
                explanation=f"Failed to parse target: {target.text}"
            )

        
        # Extract predicted coordinates from model output using regex
        predicted = extract_coordinates(answer)
        
        if predicted is None or 'lat' not in predicted or 'long' not in predicted:
            return Score(
                value=INCORRECT,
                explanation=f"Failed to extract valid coordinates from model output: {answer}"
            )
        
        try:
            # Calculate distance error
            distance = calculate_distance(
                float(target_data['lat']), float(target_data['long']),
                float(predicted['lat']), float(predicted['long'])
            )
            
            # Calculate accuracies
            country_correct = False
            city_correct = False
            
            if 'country' in predicted and 'country' in target_data:
                country_correct = predicted['country'].lower() == target_data['country'].lower()
            
            if 'city' in predicted and 'city' in target_data:
                city_correct = predicted['city'].lower() == target_data['city'].lower()
            
            # Create score
            return Score(
                value=distance, 
                answer=f"lat: {predicted['lat']}, long: {predicted['long']}, {predicted.get('city', 'Unknown')}, {predicted.get('country', 'Unknown')}",
                explanation=answer,
                metadata={ # used for metrics calculation
                    'distance': distance,
                    'country_correct': country_correct,
                    'city_correct': city_correct,
                    'predicted': predicted,
                    'target': target_data
                }
            )
        
        except Exception as e:
            return Score(
                value=INCORRECT,
                explanation=f"Error calculating score: {str(e)}\nModel output: {answer}"
            )
    
    return score

