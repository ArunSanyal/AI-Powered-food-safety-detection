import streamlit as st
import requests
import google.generativeai as genai
from PIL import Image
import io
import matplotlib.pyplot as plt

# Set up API keys (replace with your actual keys)
OCR_API_KEY = "YOUR_OCR_SPACE_API_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def ocr_space_file(image_file, api_key=OCR_API_KEY, language='eng'):
    """
    Function to call the OCR.space API and get text from an image.
    """
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': api_key,
        'language': language,
        'isOverlayRequired': False
    }
    files = {'file': image_file}
    response = requests.post(url, files=files, data=payload)
    result = response.json()
    
    if result.get('IsErroredOnProcessing'):
        st.error(f"OCR Error: {result['ErrorMessage']}")
        return None
    
    return result.get('ParsedResults')[0].get('ParsedText')

def analyze_ingredients(ingredients):
    """
    Function to analyze ingredients using Gemini API.
    """
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following list of ingredients:
    {ingredients}
    
    Provide information on:
    1. Safety for consumption
    2. Health benefits or concerns
    3. Potential allergens
    4. Nutritional value
    5. Any other relevant details
    
    Also, suggest a simple pie chart showing the proportion of healthy vs. potentially concerning ingredients.
    """
    response = model.generate_content(prompt)
    return response.text

def create_pie_chart(healthy_count, concerning_count):
    """
    Create a pie chart showing the proportion of healthy vs. potentially concerning ingredients.
    """
    labels = 'Healthy', 'Potentially Concerning'
    sizes = [healthy_count, concerning_count]
    colors = ['#66b3ff', '#ff9999']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    return fig

def main():
    st.title("Ingredient Analyzer")
    
    uploaded_file = st.file_uploader("Choose an image of ingredients", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Ingredients"):
            # Perform OCR
            ingredients_text = ocr_space_file(uploaded_file)
            
            if ingredients_text:
                st.subheader("Extracted Ingredients:")
                st.write(ingredients_text)
                
                # Analyze ingredients
                analysis = analyze_ingredients(ingredients_text)
                st.subheader("Ingredient Analysis:")
                st.write(analysis)
                
                # Create and display pie chart
                # Note: You'll need to implement logic to determine healthy vs. concerning ingredients
                # This is a simplified example
                healthy_count = 3  # Replace with actual count
                concerning_count = 2  # Replace with actual count
                pie_chart = create_pie_chart(healthy_count, concerning_count)
                st.pyplot(pie_chart)
            else:
                st.error("Failed to extract text from the image. Please try again with a clearer image.")

if __name__ == "__main__":
    main()