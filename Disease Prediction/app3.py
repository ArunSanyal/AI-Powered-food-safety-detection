import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from textblob import TextBlob
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def predict_health_risks(food_item, ingredients, consumption_frequency):
    prompt = f"""
    As a food safety and health expert, analyze the following food item and its ingredients:

    Food Item: {food_item}
    Ingredients: {', '.join(ingredients)}
    Consumption Frequency: {consumption_frequency}

    Based on this information, please provide:
    1. Potential health risks associated with consuming this food item, especially if consumed in unhealthy amounts.
    2. A list of specific diseases (e.g., diabetes, heart disease) that could arise from regular consumption of this food, particularly if it contains unsafe ingredients or is consumed excessively.
    3. Any concerning ingredients and their specific health impacts.
    4. How the consumption frequency might affect the likelihood or severity of these health risks.
    5. Rate the impact (0-10 scale) of this food on the following health aspects:
       - Cardiovascular health
       - Blood sugar levels
       - Weight management
       - Digestive health
       - Nutrient balance

    Please list the diseases in a format such as "Most likely diseases: [disease1, disease2, ...]" for easy extraction.
    Present your analysis in a structured, easy-to-read format with bullet points or numbered lists where appropriate.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def create_risk_gauge(risk_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Health Risk"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred"},
            'steps' : [
                {'range': [0, 33], 'color': "lightgreen"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def extract_risk_score(text):
    blob = TextBlob(text)
    return min(max((blob.sentiment.polarity + 1) / 2 * 100, 0), 100)

def extract_diseases(text):
    match = re.search(r'Most Likely Diseases.*?:\s*(.*)', text, re.IGNORECASE)
    if match:
        diseases_raw = match.group(1)
        diseases = re.split(r',|\band\b|\n', diseases_raw)
        return [disease.strip() for disease in diseases if disease.strip()]
    return []

def extract_health_impacts(text):
    impact_pattern = r'(\w+(?:\s+\w+)*)\s*:\s*(\d+)'
    impacts = re.findall(impact_pattern, text)
    return {aspect: int(score) for aspect, score in impacts if int(score) <= 10}

def create_health_impact_radar(impacts):
    categories = list(impacts.keys())
    values = list(impacts.values())
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Health Impacts'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        title="Health Impact Assessment"
    )
    
    return fig

def main():
    st.set_page_config(page_title="Food Safety Analyzer", page_icon="🍽️", layout="wide")

    st.title("🍽️ AI-Powered Food Safety and Health Risk Predictor")

    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Analyze your food for potential health risks and impacts.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        food_item = st.text_input("Enter the food item:", value="Pizza")

        ingredients_input = st.text_area("Enter the ingredients (one per line):", 
                                         value="Wheat flour\nTomato sauce\nCheese\nPepperoni\nOlive oil")
        ingredients = [ing.strip() for ing in ingredients_input.split('\n') if ing.strip()]

    with col2:
        consumption_frequency = st.selectbox(
            "How often is this food consumed?",
            ("Rarely", "Occasionally", "Regularly", "Frequently", "Daily")
        )

        st.write("") # Add some space
        st.write("") # Add some space
        analyze_button = st.button("Analyze Food Safety")

    if analyze_button:
        if food_item and ingredients:
            st.write("---")
            
            with st.spinner("Analyzing food safety and health risks..."):
                prediction = predict_health_risks(food_item, ingredients, consumption_frequency)
            
            # Extract and display the health risk score at the top
            risk_score = 100 - extract_risk_score(prediction)  # Adjusted for higher sentiment being lower risk
            st.plotly_chart(create_risk_gauge(risk_score), use_container_width=True)

            col_text, col_table = st.columns([3, 1])
            
            with col_text:
                st.subheader("📊 Analysis Results")
                st.markdown("### 🚨 Health Risk and Disease Prediction:")
                st.markdown(prediction)

            with col_table:
                st.subheader("Most Prominent Diseases")
                diseases = extract_diseases(prediction)
                if diseases:
                    df = pd.DataFrame({"Disease": diseases})
                    st.table(df)
                else:
                    st.write("No specific diseases were mentioned in the analysis.")

            # Extract health impacts and create radar chart
            health_impacts = extract_health_impacts(prediction)
            if health_impacts:
                st.plotly_chart(create_health_impact_radar(health_impacts), use_container_width=True)
            else:
                st.write("No specific health impact ratings were found in the analysis.")

        else:
            st.warning("⚠️ Please enter both a food item and at least one ingredient.")

    st.sidebar.header("About this App")
    st.sidebar.info(
        "This AI-powered application analyzes food items and their ingredients "
        "to predict potential health risks and impacts. It considers the frequency "
        "of consumption to provide a more accurate assessment. Always consult with "
        "a healthcare professional for personalized medical advice."
    )
    st.sidebar.header("How to Use")
    st.sidebar.markdown(
        "1. Enter a food item\n"
        "2. List the ingredients\n"
        "3. Select consumption frequency\n"
        "4. Click 'Analyze Food Safety'\n"
        "5. Review the AI-generated health risk analysis and visualizations"
    )

if __name__ == "__main__":
    main()