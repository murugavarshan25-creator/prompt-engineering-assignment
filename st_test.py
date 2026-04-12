import streamlit as st
from datetime import date

# Title
st.title("Age Calculator")

# User input
st.subheader("Enter your Date of Birth")
dob = st.date_input("Select your birth date")

# Button
if st.button("Calculate Age"):
    today = date.today()

    # Calculate age
    age = today.year - dob.year

    # Adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    st.success(f"Your age is {age} years")

    # Optional: show detailed breakdown
    days_lived = (today - dob).days
    st.info(f"You have lived approximately {days_lived} days 🎉")