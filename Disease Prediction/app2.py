import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from textblob import TextBlob
import plotly.graph_objs as go
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

    Please list the diseases in a format such as "Most likely diseases: [disease1, disease2, ...]" for easy extraction.
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
    return fig

def create_disease_bar_chart(diseases):
    if diseases:
        # Create a DataFrame to count occurrences of each disease
        df = pd.DataFrame(diseases, columns=['Disease'])
        disease_counts = df['Disease'].value_counts()

        # Create a horizontal bar chart with disease counts
        fig = go.Figure(go.Bar(
            x=disease_counts.values,
            y=disease_counts.index,
            orientation='h',
            marker=dict(color='teal'),
        ))

        # Customize the layout for better readability
        fig.update_layout(
            title="Frequency of Potential Diseases Mentioned",
            xaxis_title="Frequency",
            yaxis_title="Disease",
            bargap=0.2,  # Space between bars
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=100, r=20, t=50, b=50)
        )
        return fig
    else:
        return None


def extract_risk_score(text):
    # Simple sentiment analysis to gauge overall risk
    blob = TextBlob(text)
    # Normalize sentiment to a 0-100 scale
    return min(max((blob.sentiment.polarity + 1) / 2 * 100, 0), 100)

def extract_diseases(text):
    # Use regex to capture the "Most Likely Diseases" section
    match = re.search(r'Most Likely Diseases.*?:\s*(.*)', text, re.IGNORECASE)
    if match:
        # Extract diseases by splitting on common delimiters
        diseases_raw = match.group(1)
        # Split by commas, "and", and new lines
        diseases = re.split(r',|\band\b|\n', diseases_raw)
        # Clean up whitespace and filter out any empty strings
        diseases = [disease.strip() for disease in diseases if disease.strip()]
        return diseases
    return []


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

    st.markdown('<p class="big-font">Analyze your food for potential health risks and diseases.</p>', unsafe_allow_html=True)

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
            st.subheader("📊 Analysis Results")
            
            with st.spinner("Analyzing food safety and health risks..."):
                prediction = predict_health_risks(food_item, ingredients, consumption_frequency)
            
            st.markdown("### 🚨 Health Risk and Disease Prediction:")
            st.markdown(prediction)

            # Extract and display the health risk score
            risk_score = 100 - extract_risk_score(prediction)  # Adjusted for higher sentiment being lower risk
            st.plotly_chart(create_risk_gauge(risk_score))

            # Extract diseases and create bar chart
            diseases = extract_diseases(prediction)
            disease_chart = create_disease_bar_chart(diseases)

            if disease_chart:
                st.plotly_chart(disease_chart)
            else:
                st.write("No specific diseases were mentioned in the analysis.")

        else:
            st.warning("⚠️ Please enter both a food item and at least one ingredient.")


    st.sidebar.header("About this App")
    st.sidebar.info(
        "This AI-powered application analyzes food items and their ingredients "
        "to predict potential health risks and diseases. It considers the frequency "
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