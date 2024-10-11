import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def predict_health_risks(food_item, ingredients):
    # Construct the prompt for the Gemini model
    prompt = f"""
    As a food safety and health expert, analyze the following food item and its ingredients:

    Food Item: {food_item}
    Ingredients: {', '.join(ingredients)}

    Based on this information, please provide:
    1. Potential health risks associated with consuming this food item
    2. Possible diseases that could arise from regular consumption
    3. Any concerning ingredients and their specific health impacts

    Present your analysis in a structured format.
    """

    # Generate a response using the Gemini model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text

# Simulated function to get food item and ingredients from another source
def get_food_data_from_external_source():
    # This function could be replaced with actual data retrieval logic
    # For example, it could read from a database, API, or file
    return "Pizza", ["Wheat flour", "Tomato sauce", "Cheese", "Pepperoni", "Olive oil"]

def analyze_food_safety(food_item, ingredients):
    print(f"\nAnalyzing food safety and health risks for: {food_item}")
    print(f"Ingredients: {', '.join(ingredients)}")
    
    prediction = predict_health_risks(food_item, ingredients)
    
    print("\nHealth Risk and Disease Prediction:")
    print(prediction)
    
    return prediction

def main():
    print("AI-Powered Food Safety and Health Risk Predictor")
    
    # Get food data from external source
    food_item, ingredients = get_food_data_from_external_source()
    
    # Analyze the food data
    analysis = analyze_food_safety(food_item, ingredients)
    
    # Here you could do further processing with the analysis result
    # For example, storing it in a database, sending alerts, etc.

if __name__ == "__main__":
    main()