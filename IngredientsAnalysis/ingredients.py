import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("AIzaSyCBVcuyRfVBlAzjUn95-GMV-bltokScM3g"))

def assess_ingredient_safety(ingredient, quantity):
    """
    Function to evaluate the safety of an ingredient based on the quantity provided.
    """
    prompt = f"""
    As a food safety and health expert, analyze the following ingredient and its quantity:

    Ingredient: {ingredient}
    Quantity: {quantity}

    Based on this information, please provide:
    1. Whether the quantity is safe for consumption.
    2. Potential health risks if this quantity is regularly consumed.
    3. Safe limits for this ingredient and recommended adjustments if needed.
    """

    # Generate a response using the Gemini model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text

def predict_health_risks(ingredients_with_quantities):
    """
    Function to assess multiple ingredients and their quantities.
    """
    analysis = []

    for ingredient, quantity in ingredients_with_quantities:
        # Evaluate each ingredient's safety and health impacts
        safety_analysis = assess_ingredient_safety(ingredient, quantity)
        analysis.append(f"Ingredient: {ingredient}\nQuantity: {quantity}\nAnalysis: {safety_analysis}\n")
    
    return "\n".join(analysis)

def main():
    print("Welcome to the AI-Powered Food Safety and Ingredient Quantity Checker!")

    while True:
        food_item = input("\nEnter the food item (or 'quit' to exit): ")
        if food_item.lower() == 'quit':
            break

        # Get the ingredients with quantities
        ingredients_input = input("Enter the ingredients with quantities (e.g., sugar:50g, salt:10g): ")
        
        # Parse the input into a list of tuples (ingredient, quantity)
        ingredients_with_quantities = [tuple(ing.strip().split(':')) for ing in ingredients_input.split(',')]
        
        # Trim spaces and format properly
        ingredients_with_quantities = [(ing[0].strip(), ing[1].strip()) for ing in ingredients_with_quantities]

        print("\nAnalyzing ingredient quantities and health impacts...")
        prediction = predict_health_risks(ingredients_with_quantities)

        print("\nHealth and Safety Assessment:")
        print(prediction)

    print("\nThank you for using the Food Safety and Ingredient Quantity Checker!")

if __name__ == "__main__":
    main()
