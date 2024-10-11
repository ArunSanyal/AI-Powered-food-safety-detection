import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

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
    2. Specific diseases (e.g., diabetes, heart disease) that could arise from regular consumption of this food, particularly if it contains unsafe ingredients or is consumed excessively.
    3. Any concerning ingredients and their specific health impacts.
    4. How the consumption frequency might affect the likelihood or severity of these health risks.

    Present your analysis in a structured, easy-to-read format with bullet points or numbered lists where appropriate.
    """

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    return response.text

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
        "5. Review the AI-generated health risk analysis"
    )

if __name__ == "__main__":
    main()