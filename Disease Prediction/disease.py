import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("AIzaSyBqjWUIbvOOMErYs_o5V3T4Z0f4Od6jeyY"))

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

def main():
    print("Welcome to the AI-Powered Food Safety and Health Risk Predictor!")
    
    while True:
        food_item = input("\nEnter the food item (or 'quit' to exit): ")
        if food_item.lower() == 'quit':
            break
        
        ingredients = input("Enter the ingredients (comma-separated): ").split(',')
        ingredients = [ing.strip() for ing in ingredients]

        print("\nAnalyzing food safety and health risks...")
        prediction = predict_health_risks(food_item, ingredients)
        
        print("\nHealth Risk and Disease Prediction:")
        print(prediction)

    print("\nThank you for using the Food Safety and Health Risk Predictor!")

if __name__ == "__main__":
    main()