from inspect_ai.solver import solver, Solver, TaskState, Generate
from inspect_ai.model import ChatMessageSystem

@solver
def geolocation_prompt() -> Solver:
    """
    Custom solver to add system prompt and task instructions.
    """
    
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        # Add a system prompt
        system_message = ChatMessageSystem(content="""
        You are a top-ranked, professional, competitive world-class GeoGuessr player, renowned for your ability 
        to accurately pinpoint the location of images based solely on the visual clues they provide. 
        You have a keen eye for detail and an extensive knowledge of geography that allows you to make insightful deductions.
        """)
        state.messages.insert(0, system_message)
        
        # Add task instructions
        if state.user_prompt:
            state.user_prompt.text = """
            You have been presented with a new image, and your task is to use your exceptional skills to determine 
            the precise coordinates of the location depicted. Carefully examine the image, taking note of any 
            distinctive features, landmarks, vegetation, or other elements that could serve as clues. 
            Piece together a chain of thought, step by step, to infer the most likely location.

            Once you have gathered sufficient evidence, provide your best guess for the coordinates in the following JSON format:
            {"lat": latitude, "long": longitude, "city": city, "country": country}

            If you cannot narrow it down, then provide your best guess.
            Be as specific as possible, narrowing down the location to a particular region, city, or even a 
            specific landmark or intersection. Your goal is to demonstrate your expertise as a GeoGuessr master 
            by providing a highly accurate and well-reasoned response.
            """
        
        return state
    
    return solve