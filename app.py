import pandas as pd
from datetime import datetime
import streamlit as st

# Initialize the DataFrame in session_state if not already present
if 'df' not in st.session_state:
    columns = ['Date', 'Production Qty', 'Rejection Qty', 'Accumulated Production Qty', 
               'Accumulated Rejection Qty', 'Percentage of Daily Rejection', 
               'Percentage of Accumulated Rejection']
    st.session_state.df = pd.DataFrame(columns=columns)

# Streamlit app
st.title("Daily Production and Rejection Tracker")

# User inputs
date = st.text_input("Date (dd/mm/yyyy):")
production_qty = st.number_input("Production Qty:", min_value=0, step=1)
rejection_qty = st.number_input("Rejection Qty:", min_value=0, step=1)

# Add entry button
if st.button("Add Entry"):
    try:
        # Validate date format
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            st.error("Invalid date format. Please use dd/mm/yyyy.")
            st.stop()

        # Calculate accumulated values
        if st.session_state.df.empty:
            accumulated_production_qty = production_qty
            accumulated_rejection_qty = rejection_qty
        else:
            accumulated_production_qty = st.session_state.df['Accumulated Production Qty'].iloc[-1] + production_qty
            accumulated_rejection_qty = st.session_state.df['Accumulated Rejection Qty'].iloc[-1] + rejection_qty

        # Calculate percentages
        percentage_daily_rejection = (rejection_qty / production_qty) * 100 if production_qty > 0 else 0
        percentage_accumulated_rejection = (accumulated_rejection_qty / accumulated_production_qty) * 100 if accumulated_production_qty > 0 else 0

        # Append the new entry to the DataFrame in session_state
        new_entry = pd.DataFrame([[date, production_qty, rejection_qty, accumulated_production_qty, 
                                   accumulated_rejection_qty, percentage_daily_rejection, 
                                   percentage_accumulated_rejection]], columns=st.session_state.df.columns)
        st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)

        st.success("Entry added successfully!")
    except ValueError as e:
        st.error(f"Error: {str(e)}")

# Display the current DataFrame
st.write(st.session_state.df)

# Print report button
if st.button("Print Report"):
    st.session_state.df.to_csv('daily_production_report.csv', index=False)
    st.success("Report saved as 'daily_production_report.csv'")
