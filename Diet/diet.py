import streamlit as st
import pandas as pd

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def generate_diet_recommendation(tdee, goal):
    if goal == "Lose Weight":
        calorie_target = tdee - 500
    elif goal == "Gain Weight":
        calorie_target = tdee + 500
    else:
        calorie_target = tdee
    
    protein = (calorie_target * 0.3) / 4
    carbs = (calorie_target * 0.4) / 4
    fats = (calorie_target * 0.3) / 9
    
    return calorie_target, protein, carbs, fats

def main():
    st.set_page_config(page_title="Personalized Diet Recommender", page_icon="🥗", layout="wide")
    st.title("🥗 Personalized Diet Recommender")
    
    st.write("Enter your details below to get a personalized diet recommendation.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0)
        height = st.number_input("Height (cm)", min_value=140.0, max_value=220.0, value=170.0)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity_level = st.selectbox("Activity Level", [
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"
        ])
        goal = st.selectbox("Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
    
    if st.button("Generate Diet Recommendation"):
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)
        calorie_target, protein, carbs, fats = generate_diet_recommendation(tdee, goal)
        
        st.subheader("Your Personalized Diet Recommendation")
        st.write(f"Daily Calorie Target: {calorie_target:.0f} calories")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Protein", f"{protein:.1f}g", "30% of calories")
        col2.metric("Carbohydrates", f"{carbs:.1f}g", "40% of calories")
        col3.metric("Fats", f"{fats:.1f}g", "30% of calories")
        
        st.subheader("Sample Meal Plan")
        meal_plan = pd.DataFrame({
            "Meal": ["Breakfast", "Snack", "Lunch", "Snack", "Dinner"],
            "Calories": [
                calorie_target * 0.25,
                calorie_target * 0.1,
                calorie_target * 0.3,
                calorie_target * 0.1,
                calorie_target * 0.25
            ]
        })
        meal_plan["Calories"] = meal_plan["Calories"].round().astype(int)
        st.table(meal_plan)
        
        st.info("Note: This is a basic recommendation. Please consult with a registered dietitian or nutritionist for a more comprehensive and personalized meal plan.")

if __name__ == "__main__":
    main()