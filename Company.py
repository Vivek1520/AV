import streamlit as st
import pandas as pd
import datetime

# Initialize the CSV file if it does not exist
def init_data():
    try:
        df = pd.read_csv("feedback.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Employee", "Feedback", "Rating", "Department"])
        df.to_csv("feedback.csv", index=False)
    return df

# Save a new feedback entry to the CSV file
def save_feedback(date, employee, feedback, rating, department):
    df = pd.read_csv("feedback.csv")
    new_feedback = pd.DataFrame({
        "Date": [date],
        "Employee": [employee],
        "Feedback": [feedback],
        "Rating": [rating],
        "Department": [department]
    })
    df = pd.concat([df, new_feedback], ignore_index=True)
    df.to_csv("feedback.csv", index=False)

# Main function to run the Streamlit app
def main():
    st.title("Employee Feedback and Engagement Platform")

    # Initialize data
    feedback_df = init_data()

    # Section for submitting feedback
    st.header("Submit Your Feedback")
    employee_name = st.text_input("Your Name:")
    department = st.selectbox("Department:", ["HR", "Sales", "Engineering", "Marketing", "Other"])
    feedback_text = st.text_area("Your Feedback:")
    rating = st.slider("Rate Your Experience (1-5):", 1, 5)

    if st.button("Submit Feedback"):
        if employee_name and feedback_text:
            date_submitted = datetime.datetime.now().strftime("%Y-%m-%d")
            save_feedback(date_submitted, employee_name, feedback_text, rating, department)
            st.success("Feedback submitted successfully!")
        else:
            st.error("Please fill in all fields.")

    # Section to view feedback
    st.header("Feedback Overview")
    if feedback_df.empty:
        st.write("No feedback submitted yet.")
    else:
        st.write("### Submitted Feedback")
        for index, row in feedback_df.iterrows():
            st.subheader(f"Feedback #{index + 1}")
            st.write(f"**Date Submitted:** {row['Date']}")
            st.write(f"**Employee:** {row['Employee']}")
            st.write(f"**Department:** {row['Department']}")
            st.write(f"**Feedback:** {row['Feedback']}")
            st.write(f"**Rating:** {row['Rating']}/5")
            st.write("---")

if __name__ == "__main__":
    main()
