import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import plotly.express as px
import requests
import pandas as pd

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Nutritionix API configuration
NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")


def generate_diet_plan(diseases):
    prompt = f"""
    Create a concise, visually-friendly diet plan for someone with: {diseases}

    Provide:
    1. Top 5 foods to eat (as a list)
    2. Top 5 foods to avoid (as a list)
    3. 3 key supplements (if any)
    4. 3 lifestyle tips
    5. Recommended daily calorie intake

    Format in Markdown, keep it brief and easy to read.
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text


def generate_roadmap(diseases):
    prompt = f"""
    Create a health improvement roadmap for: {diseases}

    Provide 3 goals each for:
    1. Short-term (1-3 months)
    2. Medium-term (3-6 months)
    3. Long-term (6-12 months)

    For each goal, also provide:
    - A metric to measure progress (e.g., weight, blood pressure, energy level)
    - A target value for that metric

    Format as a list of 9 items, each containing: time frame, goal, metric, target value.
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return [item.strip() for item in response.text.split('\n') if item.strip()]


def create_nutrient_chart(foods):
    nutrients = []
    for food in foods:
        response = requests.post(
            "https://trackapi.nutritionix.com/v2/natural/nutrients",
            headers={
                "x-app-id": NUTRITIONIX_APP_ID,
                "x-app-key": NUTRITIONIX_API_KEY,
                "Content-Type": "application/json"
            },
            json={"query": food}
        )
        if response.status_code == 200:
            data = response.json()
            if data['foods']:
                nutrients.append({
                    'Food': food,
                    'Calories': data['foods'][0]['nf_calories'],
                    'Protein': data['foods'][0]['nf_protein'],
                    'Carbs': data['foods'][0]['nf_total_carbohydrate'],
                    'Fat': data['foods'][0]['nf_total_fat']
                })

    df = pd.DataFrame(nutrients)
    fig = px.bar(df, x='Food', y=['Protein', 'Carbs', 'Fat'], title="Nutrient Composition of Recommended Foods")
    return fig


def main():
    st.set_page_config(page_title="AI Diet Planner", layout="wide")

    st.title("🥗 AI-Powered Diet Planner")
    st.markdown("---")

    diseases = st.text_input("Enter your health condition(s):")

    if st.button("Generate Plan", key="generate"):
        if diseases:
            with st.spinner("Creating your personalized health plan..."):
                diet_plan = generate_diet_plan(diseases)
                roadmap_items = generate_roadmap(diseases)

            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📋 Your Personalized Diet Plan")
                st.markdown(diet_plan)

                # Extract recommended foods from diet plan
                recommended_foods = [line.split('. ', 1)[1] for line in diet_plan.split('\n') if
                                     line.startswith('1.') and ': ' in line]
                if recommended_foods:
                    st.subheader("📊 Nutrient Composition of Recommended Foods")
                    nutrient_chart = create_nutrient_chart(recommended_foods)
                    st.plotly_chart(nutrient_chart, use_container_width=True)

            with col2:
                st.subheader("📋 Health Tips")
                # Static health tips table
                health_tips_data = {
                    "Tip": [
                        "Stay hydrated by drinking at least 8 glasses of water daily.",
                        "Incorporate regular physical activity into your routine.",
                        "Prioritize whole, unprocessed foods over packaged options.",
                        "Get adequate sleep (7-9 hours) for better health.",
                        "Monitor portion sizes to avoid overeating."
                    ],
                    "Description": [
                        "Hydration aids digestion and nutrient absorption.",
                        "Exercise helps maintain a healthy weight and reduces stress.",
                        "Whole foods provide more nutrients and fewer empty calories.",
                        "Proper rest supports overall health and recovery.",
                        "Being mindful of portions can help manage calorie intake."
                    ]
                }
                health_tips_df = pd.DataFrame(health_tips_data)
                st.table(health_tips_df)

        else:
            st.warning("Please enter at least one health condition to generate a plan.")


if __name__ == "__main__":
    main()
