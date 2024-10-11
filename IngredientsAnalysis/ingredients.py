import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Pexels API configuration
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_API_URL = "https://api.pexels.com/v1/search"

def get_image_url(query):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    response = requests.get(PEXELS_API_URL, headers=headers, params=params)
    data = response.json()
    if data["photos"]:
        return data["photos"][0]["src"]["medium"]
    return None

def assess_ingredient_safety(ingredient, quantity):
    prompt = f"""
    As a food safety and health expert, analyze the following ingredient and its quantity:

    Ingredient: {ingredient}
    Quantity: {quantity}

    Based on this information, please provide:
    1. Whether the quantity is safe for consumption.
    2. Potential health risks if this quantity is regularly consumed.
    3. Safe limits for this ingredient and recommended adjustments if needed.
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def predict_health_risks(ingredients_with_quantities):
    analysis = []
    for ingredient, quantity in ingredients_with_quantities:
        safety_analysis = assess_ingredient_safety(ingredient, quantity)
        analysis.append({"ingredient": ingredient, "quantity": quantity, "analysis": safety_analysis})
    return analysis

def create_safety_chart(analysis):
    ingredients = [item['ingredient'] for item in analysis]
    safety_scores = [len(item['analysis'].split()) for item in analysis]  # Using word count as a proxy for safety score

    fig = go.Figure(data=[go.Bar(x=ingredients, y=safety_scores, marker_color='skyblue')])
    fig.update_layout(
        title="Ingredient Safety Analysis",
        xaxis_title="Ingredients",
        yaxis_title="Safety Score (word count)",
        height=400
    )
    return fig

def main():
    st.set_page_config(page_title="AI-Powered Food Safety Checker", layout="wide")

    st.title("AI-Powered Food Safety and Ingredient Quantity Checker")

    col1, col2 = st.columns([2, 1])

    with col1:
        food_item = st.text_input("Enter the food item:")
        ingredients_input = st.text_area("Enter the ingredients with quantities (e.g., sugar:50g, salt:10g):")

        if st.button("Analyze"):
            if food_item and ingredients_input:
                ingredients_with_quantities = [tuple(ing.strip().split(':')) for ing in ingredients_input.split(',')]
                ingredients_with_quantities = [(ing[0].strip(), ing[1].strip()) for ing in ingredients_with_quantities]

                st.info("Analyzing ingredient quantities and health impacts...")
                analysis = predict_health_risks(ingredients_with_quantities)

                st.subheader("Health and Safety Assessment:")
                for item in analysis:
                    with st.expander(f"{item['ingredient']} ({item['quantity']})"):
                        st.write(item['analysis'])

                st.subheader("Safety Analysis Chart")
                safety_chart = create_safety_chart(analysis)
                st.plotly_chart(safety_chart, use_container_width=True)

    with col2:
        if food_item:
            image_url = get_image_url(food_item)
            if image_url:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=f"Image of {food_item}", use_column_width=True)
            else:
                st.warning("No image found for the food item.")

if __name__ == "__main__":
    main()