import streamlit as st
import healthy
import ingredients
import disease

def main():
    st.set_page_config(page_title="Food Safety & Health Analyzer", page_icon="🍽️", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Healthy Food Analysis", "Ingredient Analysis", "Disease Prediction"])

    if page == "Healthy Food Analysis":
        st.title("🥗 Healthy Food Analysis")
        healthy.main()
    elif page == "Ingredient Analysis":
        st.title("🧪 Ingredient Analysis")
        ingredients.main()
    else:
        st.title("🩺 Disease Prediction")
        disease.main()

if __name__ == "__main__":
    main()