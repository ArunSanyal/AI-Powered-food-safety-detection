import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API with your API key
genai.configure(api_key=os.getenv("YOUR_API_KEY"))  # Replace with your actual Google API key

def analyze_food(food_name):
    # Crafting the prompt to get the list of ingredients and classifications
    prompt = f"""
    Food: {food_name}
    - List the main ingredients in this food item.
    - For each ingredient, indicate if it's healthy or unhealthy.
    - Finally, provide an overall assessment of whether the food is considered safe or unsafe based on the ingredients.

    Please structure the response as follows:
    Ingredients: <ingredient list>
    Health Classification: <healthy/unhealthy for each ingredient>
    Overall Food Health: <safe/unsafe>
    """

    # Sending the prompt to the Google Generative AI model
    model = genai.GenerativeModel('gemini-pro')  # Adjust the model name if necessary
    response = model.generate_content(prompt)

    # Extracting and displaying the response
    output = response.text.strip()
    return output

def main():
    print("Welcome to the AI-Powered Food Safety and Health Risk Predictor!")

    while True:
        food_name = input("\nEnter the food item (or 'quit' to exit): ")
        if food_name.lower() == 'quit':
            break

        print("\nAnalyzing food safety and health risks...")
        analysis = analyze_food(food_name)

        # Print the structured output
        print("\nHealth Classification and Assessment:")
        print(analysis)

    print("\nThank you for using the Food Safety and Health Risk Predictor!")

if __name__ == "__main__":
    main()
