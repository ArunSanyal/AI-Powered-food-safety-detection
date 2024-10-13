import google.generativeai as genai
import os
from google.cloud import vision
import pandas as pd

# Configure the Gemini API and Google Vision API
genai.configure(api_key="AIzaSyBqjWUIbvOOMErYs_o5V3T4Z0f4Od6jeyY")
client = vision.ImageAnnotatorClient()

# Function to analyze ingredient safety
def analyze_ingredient_safety(ingredient, quantity):
    prompt = f"""
    As a food safety and health expert, analyze the following ingredient and its quantity:

    Ingredient: {ingredient}
    Quantity: {quantity}

    Based on this information, please provide:
    1. Whether the quantity is safe for consumption.
    2. Potential health risks if this quantity is regularly consumed.
    3. Safe limits for this ingredient and recommended adjustments if needed.
    """

    # Generate response using Gemini API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text

# Function to extract text from an image using Google Vision API
def extract_text_from_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(f"Error with Google Vision API: {response.error.message}")
    
    # Extract text from the image
    text = response.text_annotations[0].description
    return text

# Parse extracted text into ingredients and quantities based on commas
def parse_ingredients(text):
    # Assuming the text is in a comma-separated format (ingredient:quantity)
    ingredients_with_quantities = [tuple(ing.strip().split(':')) for ing in text.split(',')]
    ingredients_with_quantities = [(ing[0].strip(), ing[1].strip()) for ing in ingredients_with_quantities]
    return ingredients_with_quantities

# Analyze each ingredient's safety and health impact
def analyze_ingredients(ingredients_with_quantities):
    analysis = []

    for ingredient, quantity in ingredients_with_quantities:
        safety_analysis = analyze_ingredient_safety(ingredient, quantity)
        analysis.append({
            "Ingredient": ingredient,
            "Quantity": quantity,
            "Analysis": safety_analysis
        })
    
    return pd.DataFrame(analysis)  # Return the result as a table

def main():
    print("Welcome to the AI-Powered Ingredient Health and Safety Analyzer!")

    # Step 1: Use the given image path
    image_path = r'C:\Users\DELL\OneDrive\Desktop\Bit\OCRingre\ocr.py'

    # Step 2: Extract text from the image
    print("\nExtracting ingredients from the image...")
    extracted_text = extract_text_from_image(image_path)
    
    # Step 3: Parse ingredients and quantities
    ingredients_with_quantities = parse_ingredients(extracted_text)
    
    # Step 4: Analyze health impacts and safety of each ingredient
    print("\nAnalyzing the ingredients...")
    result_df = analyze_ingredients(ingredients_with_quantities)

    # Step 5: Display the results
    print("\nHealth and Safety Analysis of Ingredients:")
    print(result_df)

    # Save results to CSV (optional)
    result_df.to_csv('ingredient_analysis.csv', index=False)

if __name__ == "__main__":
    main()
