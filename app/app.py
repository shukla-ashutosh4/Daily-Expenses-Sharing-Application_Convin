import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from users import create_user, get_user
from expenses import add_expense, split_equal, split_exact, split_percentage, get_user_expenses
from utils import validate_percentage, validate_exact

# Custom CSS for animations
st.markdown("""
    <style>
    .animated-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        transition-duration: 0.4s;
        cursor: pointer;
    }

    .animated-button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }

    .fade-in {
        animation: fadeInAnimation ease 2s;
        animation-iteration-count: 1;
        animation-fill-mode: forwards;
    }

    @keyframes fadeInAnimation {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("Daily Expenses Sharing Application")

# Reset functionality
def reset_fields():
    for key in st.session_state.keys():
        del st.session_state[key]

# Initialize session state values to track inputs
if 'name' not in st.session_state:
    st.session_state['name'] = ""
if 'email' not in st.session_state:
    st.session_state['email'] = ""
if 'mobile_number' not in st.session_state:
    st.session_state['mobile_number'] = ""
if 'expense_description' not in st.session_state:
    st.session_state['expense_description'] = ""
if 'total_amount' not in st.session_state:
    st.session_state['total_amount'] = 0.0
if 'split_type' not in st.session_state:
    st.session_state['split_type'] = "equal"
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

# Animated header with fade-in effect
st.markdown('<h2 class="fade-in">Welcome to the Expense Tracker!</h2>', unsafe_allow_html=True)

# User Management Section
st.subheader("Create User")
st.session_state['name'] = st.text_input("Name", value=st.session_state['name'])
st.session_state['email'] = st.text_input("Email", value=st.session_state['email'])
st.session_state['mobile_number'] = st.text_input("Mobile Number", value=st.session_state['mobile_number'])

# Button for creating a user
if st.button("Create User", key="create_user"):
    user = create_user(st.session_state['name'], st.session_state['email'], st.session_state['mobile_number'])
    st.success(f"User {user.name} created successfully", icon="✅")

# Expense Management Section
st.subheader("Add Expense")
st.session_state['expense_description'] = st.text_input("Expense Description", value=st.session_state['expense_description'])
st.session_state['total_amount'] = st.number_input("Total Amount", min_value=0.0, value=st.session_state['total_amount'])
st.session_state['split_type'] = st.selectbox("Split Type", ["equal", "exact", "percentage"], index=["equal", "exact", "percentage"].index(st.session_state['split_type']))

# Participants
participants = []
number_of_participants = st.number_input("Number of Participants", min_value=1, step=1)
for i in range(number_of_participants):
    email = st.text_input(f"Participant {i+1} Email")
    if st.session_state['split_type'] == "exact":
        amount = st.number_input(f"Participant {i+1} Amount", min_value=0.0)
        participants.append({"email": email, "amount": amount})
    elif st.session_state['split_type'] == "percentage":
        percentage = st.number_input(f"Participant {i+1} Percentage", min_value=0.0, max_value=100.0)
        participants.append({"email": email, "percentage": percentage})
    else:
        participants.append({"email": email})

# Add Expense Logic
if st.button("Add Expense", key="add_expense"):
    if st.session_state['split_type'] == "exact" and not validate_exact(st.session_state['total_amount'], participants):
        st.error("Exact amounts must add up to the total amount!")
    elif st.session_state['split_type'] == "percentage" and not validate_percentage(participants):
        st.error("Percentages must add up to 100%!")
    else:
        expense = add_expense(st.session_state['expense_description'], st.session_state['total_amount'], st.session_state['split_type'], participants)
        st.success(f"Expense '{expense.description}' added successfully", icon="💸")

# Show User Expenses
st.subheader("View User Expenses")
st.session_state['user_email'] = st.text_input("User Email for Expense Check", value=st.session_state['user_email'])
if st.button("Check Expenses", key="check_expense"):
    user_expenses = get_user_expenses(st.session_state['user_email'])
    if user_expenses:
        exp_list = [{"Expense": exp.description, "Total": exp.total_amount, "Split Type": exp.split_type} for exp in user_expenses]
        df_expenses = pd.DataFrame(exp_list)
        st.write(df_expenses)
        
        # Bar Chart for Individual Expenses
        st.subheader("Individual Expenses Breakdown")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=df_expenses['Expense'], y=df_expenses['Total'], name='Total Amount', marker_color='blue'))
        fig_bar.update_layout(title="Total Expenses Breakdown", xaxis_title="Expense", yaxis_title="Amount")
        st.plotly_chart(fig_bar)
        
        # Pie Chart for Expense Distribution
        st.subheader("Expense Distribution")
        split_data = {"Participant": [p['email'] for p in participants], "Amount": [p.get('amount', st.session_state['total_amount'] / len(participants)) for p in participants]}
        df_split = pd.DataFrame(split_data)
        fig_pie = go.Figure(data=[go.Pie(labels=df_split['Participant'], values=df_split['Amount'], hole=.3)])
        fig_pie.update_layout(title="Expense Split Distribution")
        st.plotly_chart(fig_pie)
    else:
        st.warning(f"No expenses found for {st.session_state['user_email']}")

# Reset button functionality
if st.button("Reset", key="reset_form"):
    reset_fields()
    st.experimental_rerun()  # Refresh the entire app to clear inputs
