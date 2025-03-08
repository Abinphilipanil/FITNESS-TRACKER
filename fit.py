import streamlit as st
import pandas as pd
import os
import datetime
import openai

# OpenAI API key (replace with your own API key)
openai.api_key = 'AIzaSyCVEXIacEelDDRspWGHwsT34NFLl7vqn5E'

# File to store user data
data_file = 'user_data.csv'
forum_file = 'forum_data.csv'

# Check if data file exists, if not create it
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=['Name', 'Sex', 'Age', 'Height', 'Weight', 'BMI', 'Goal', 'Date', 'Workout'])
    df.to_csv(data_file, index=False)

# Check if forum file exists, if not create it
if not os.path.exists(forum_file):
    forum_df = pd.DataFrame(columns=['Timestamp', 'User', 'Question', 'Answer'])
    forum_df.to_csv(forum_file, index=False)

def calculate_bmi(weight, height):
    if height > 0:
        bmi = weight / (height/100)**2
        return round(bmi, 2)
    else:
        return 0

def ai_suggestions(bmi, goal):
    suggestions = ["Based on your BMI and goal, here are some personalized suggestions:"]
    if bmi < 18.5:
        suggestions.append("1. Your BMI indicates that you are underweight. Consider a balanced diet to gain weight.")
        suggestions.append("2. Include calorie-dense foods like nuts, seeds, avocados, and lean meats.")
        suggestions.append("3. Strength training exercises can help build muscle mass.")
    elif 18.5 <= bmi < 24.9:
        suggestions.append("1. Your BMI is normal. Maintain a balanced diet and regular exercise.")
        suggestions.append("2. Include a mix of cardio and strength training exercises.")
        suggestions.append("3. Stay hydrated and get enough sleep.")
    elif 25 <= bmi < 29.9:
        suggestions.append("1. Your BMI indicates that you are overweight. Consider a diet plan and regular exercise.")
        suggestions.append("2. Focus on cardio exercises like running, cycling, or swimming.")
        suggestions.append("3. Incorporate strength training to build muscle and boost metabolism.")
    else:
        suggestions.append("1. Your BMI indicates that you are obese. Consult a healthcare provider for a suitable plan.")
        suggestions.append("2. Start with low-impact cardio exercises and gradually increase intensity.")
        suggestions.append("3. Monitor your diet and avoid high-calorie, low-nutrient foods.")
    
    if goal == "Lose Weight":
        suggestions.append("4. Create a calorie deficit by consuming fewer calories than you burn.")
        suggestions.append("5. Include high-intensity interval training (HIIT) in your workout routine.")
    elif goal == "Gain Muscle":
        suggestions.append("4. Increase your protein intake to support muscle growth.")
        suggestions.append("5. Focus on compound exercises like squats, deadlifts, and bench presses.")
    elif goal == "Maintain Fitness":
        suggestions.append("4. Maintain a balanced routine with both cardio and strength training.")
        suggestions.append("5. Stay consistent with your workouts and diet plan.")

    return suggestions

def save_user_data(data):
    df = pd.read_csv(data_file)
    new_data = pd.DataFrame([data])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(data_file, index=False)

def save_forum_data(data):
    forum_df = pd.read_csv(forum_file)
    new_data = pd.DataFrame([data])
    forum_df = pd.concat([forum_df, new_data], ignore_index=True)
    forum_df.to_csv(forum_file, index=False)

def get_ai_answer(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer the following question about exercise and fitness:\n\n{question}\n\nAnswer:",
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    return answer

def main():
    st.title("Fitness Tracker App")

    st.sidebar.title("Enter Your Details")
    name = st.sidebar.text_input("Name")
    sex = st.sidebar.selectbox("Sex", ["Male", "Female", "Other"])
    age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=25)
    height = st.sidebar.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.sidebar.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    goal = st.sidebar.selectbox("Goal", ["Lose Weight", "Gain Muscle", "Maintain Fitness"])
    
    if st.sidebar.button("Calculate BMI"):
        bmi = calculate_bmi(weight, height)
        st.sidebar.write(f"Your BMI: {bmi}")
        st.sidebar.write(f"Height: {height} cm")
        st.sidebar.write(f"Weight: {weight} kg")

        suggestions = ai_suggestions(bmi, goal)
        st.sidebar.write("AI Suggestions:")
        for suggestion in suggestions:
            st.sidebar.write("- " + suggestion)
        
        user_data = {
            "Name": name,
            "Sex": sex,
            "Age": age,
            "Height": height,
            "Weight": weight,
            "BMI": bmi,
            "Goal": goal,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Workout": ""
        }
        save_user_data(user_data)

    st.header("Workout Tracker")
    st.subheader("Select Your Workout")

    workout_options = ["Running", "Cycling", "Swimming", "Weightlifting", "Yoga", "HIIT", "Walking", "Dancing"]
    workout = st.selectbox("Workout Type", workout_options)
    workout_details = st.text_area("Enter your workout details for today")

    if st.button("Save Workout"):
        df = pd.read_csv(data_file)
        workout_entry = f"{workout}: {workout_details}"
        df.loc[df['Name'] == name, 'Workout'] = workout_entry
        df.to_csv(data_file, index=False)
        st.success("Workout details saved successfully!")

    st.header("User Data")
    df = pd.read_csv(data_file)
    st.dataframe(df)

    st.header("Question Forum")
    st.subheader("Ask a Question")
    question = st.text_area("Enter your question about exercise or fitness")
    
    if st.button("Submit Question"):
        answer = get_ai_answer(question)
        forum_data = {
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User": name,
            "Question": question,
            "Answer": answer
        }
        save_forum_data(forum_data)
        st.success("Question submitted successfully!")
        st.write("AI Answer:")
        st.write(answer)

    st.subheader("Forum Q&A")
    forum_df = pd.read_csv(forum_file)
    st.dataframe(forum_df)

if __name__ == "__main__":
    main()
