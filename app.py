import os
import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Personalized Diet Planner",
    page_icon="🥗",
    layout="centered"
)

st.title("🥗 AI Personalized Diet Planner")
st.write("Generate a calorie target and meal plan using Generative AI")

# -----------------------------
# API Key Setup 
# -----------------------------
load_dotenv()



# -----------------------------
# Initialize LLM
# -----------------------------
try:
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",  #  Free tier model
        temperature=0.4
    )
except Exception as e:
    st.error(f"Failed to initialize AI model: {e}")
    st.stop()

# -----------------------------
# Prompt Template
# -----------------------------
diet_prompt = PromptTemplate(
    input_variables=[
        "age",
        "gender",
        "height",
        "weight",
        "activity_level",
        "goal",
        "diet_type",
        "meals_per_day",
        "constraints"
    ],
    template="""
You are a certified nutrition assistant.

User Profile:
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- Activity Level: {activity_level}
- Goal: {goal}
- Diet Preference: {diet_type}
- Meals per Day: {meals_per_day}
- Allergies or Dislikes: {constraints}

Tasks:
1. Estimate a suitable daily calorie target (mention the number in kcal).
2. Create a simple Indian daily meal plan based on the diet preference.
3. Briefly explain why this plan supports the user's goal.

Keep the response clear and structured.
"""
)

# -----------------------------
# User Input Form
# -----------------------------
with st.form("diet_form"):
    st.subheader("👤 User Details")

    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])

    height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)

    activity_level = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Lightly active",
            "Moderately active",
            "Very active"
        ]
    )

    goal = st.selectbox(
        "Goal",
        [
            "Weight loss",
            "Weight maintenance",
            "Muscle gain"
        ]
    )

    diet_type = st.selectbox(
        "Diet Preference",
        [
            "Vegetarian",
            "Non-Vegetarian",
            "Vegan"
        ]
    )

    meals_per_day = st.selectbox("Meals per Day", [2, 3, 4])

    constraints = st.text_input(
        "Allergies / Dislikes (optional)",
        placeholder="e.g., no peanuts, lactose intolerant"
    )

    submit = st.form_submit_button("Generate Diet Plan")

# -----------------------------
# Run LLM 
# -----------------------------
if submit:
    with st.spinner("Generating your personalized diet plan..."):
        try:
            formatted_prompt = diet_prompt.format(
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                activity_level=activity_level,
                goal=goal,
                diet_type=diet_type,
                meals_per_day=meals_per_day,
                constraints=constraints if constraints else "None"
            )

            response = llm.invoke(formatted_prompt)

            st.success("✅ Diet Plan Generated")
            st.markdown(response.content)

        except Exception as e:
            st.error("Something went wrong while generating the plan.")
            st.exception(e)
