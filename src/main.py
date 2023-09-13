import streamlit as st
import json
import pandas as pd
import os
from secrets import *
import xlsxwriter
import plotly.express as px

st.set_page_config(
    page_title="Budget Generator",
    page_icon="💰",
)

predefined_categories = ["Food", "Transportation", "Accommodation", "Entertainment", "Miscellaneous"]

def load_budget_data():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as config_file:
            try:
                data = json.load(config_file)
            except json.JSONDecodeError:
                data = {"budgets": []}
    else:
        data = {"budgets": []}
    
    return data


def add_budget_item(event_name, event_date, category, particular, quantity, description, price):
    data = load_budget_data()

    budget_item = next((item for item in data["budgets"] if item["event_name"] == event_name), None)

    if budget_item is None:
        budget_item = {
            "event_name": event_name,
            "event_date": str(event_date),
            "expenses": []
        }
    rounded_price = round(price, 2)
    total_cost = round(quantity * rounded_price, 2)

    unique_id = token_hex(3)
    new_expense = {
        "id": unique_id,
        "category": category,
        "particular": particular,
        "quantity": quantity,
        "description": description,
        "price": rounded_price,
        "total_cost": total_cost
    }

    budget_item["expenses"].append(new_expense)

    if budget_item not in data["budgets"]:
        data["budgets"].append(budget_item)

    with open('config.json', 'w') as config_file:
        json.dump(data, config_file, indent=4)

    st.success("Expense added successfully!")


def delete_budget_item(event_name, expense_id):

    data = load_budget_data()

    budget_item = next((item for item in data["budgets"] if item["event_name"] == event_name), None)

    if budget_item:

        budget_item["expenses"] = [expense for expense in budget_item["expenses"] if expense["id"] != expense_id]

        with open('config.json', 'w') as config_file:
            json.dump(data, config_file, indent=4)

        st.sidebar.success(f"Expense with ID {expense_id} deleted successfully!")

def export_to_excel(dataframe, event_name):

    excel_writer = pd.ExcelWriter(f'{event_name}_expenses.xlsx', engine='xlsxwriter')

    dataframe.to_excel(excel_writer, sheet_name='Expenses', index=False)

    workbook = excel_writer.book
    worksheet = excel_writer.sheets['Expenses']

    chart = workbook.add_chart({'type': 'column'})

    for i in range(1, dataframe.shape[1]):
        chart.add_series({
            'name': ['Expenses', 0, i],
            'categories': ['Expenses', 1, 0, dataframe.shape[0], 0],
            'values': ['Expenses', 1, i, dataframe.shape[0], i],
        })

    worksheet.insert_chart('H2', chart)

    header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white', 'bg_color': 'blue'})
    cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    total_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_color': 'white', 'bg_color': 'blue'})

    for col_num, value in enumerate(dataframe.columns.values):
        worksheet.write(0, col_num, value, header_format)
    for row_num, values in enumerate(dataframe.values):
        for col_num, value in enumerate(values):
            worksheet.write(row_num + 1, col_num, value, cell_format)

    for i, column in enumerate(dataframe.columns):
        max_len = max(dataframe[column].astype(str).apply(len).max(), len(column) + 5)
        worksheet.set_column(i, i, max_len)

    total_cost_col = dataframe['Total Cost']
    total_cost_sum = total_cost_col.sum()
    worksheet.write(dataframe.shape[0] + 1, dataframe.shape[1] - 1, total_cost_sum, total_format)

    worksheet.add_table(0, 0, dataframe.shape[0], dataframe.shape[1], {'columns': [{'header': column} for column in dataframe.columns]})

    excel_writer.close()


st.title("Budget Generator")

option = st.selectbox("Select an Option:", ["Log Old Event", "Add New Session"])

if option == "Log Old Event":
    existing_events = [item["event_name"] for item in load_budget_data()["budgets"]]
    selected_event = st.selectbox("Select an existing event:", existing_events)

    if st.button("Edit Event"):
        st.session_state.event_name = selected_event
elif option == "Add New Session":
    st.title("Add New Session")

    event_name = st.text_input("Enter Event Name")
    event_date = st.date_input("Event Date")
    
    category = st.selectbox("Select Expense Category:", predefined_categories)
    particular = st.text_input("Particular (e.g., name of the item)")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    description = st.text_input("Description")
    price = st.number_input("Price", min_value=5, step=5)

    if st.button("Add Expense"):
        add_budget_item(event_name, event_date, category, particular, quantity, description, price)

if "event_name" in st.session_state:
    st.title(f"Event: {st.session_state.event_name}")

    event_date = st.date_input("Event Date")
    category = st.selectbox("Select Expense Category:", predefined_categories)
    particular = st.text_input("Particular (e.g., name of the item)")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    description = st.text_input("Description")
    price = st.number_input("Price", min_value=0.01, step=0.01)

    if st.button("Add Expense"):
        add_budget_item(st.session_state.event_name, event_date, category, particular, quantity, description, price)

    st.subheader(f"Registered Expenses for {st.session_state.event_name}")
    data = load_budget_data()
    expense_data = []

    current_event_budget = next((item for item in data["budgets"] if item["event_name"] == st.session_state.event_name), None)

    if current_event_budget:
        for expense in current_event_budget["expenses"]:
            expense_data.append([expense["id"], expense["category"], expense["particular"], expense["quantity"], expense["description"], expense["price"], expense["total_cost"]])

        if expense_data:
            expense_df = pd.DataFrame(expense_data, columns=["ID", "Category", "Particular", "Quantity", "Description", "Price", "Total Cost"])

            st.subheader("Registered Expenses:")
            st.table(expense_df)

            if st.button("Export to Excel"):
                export_to_excel(expense_df, st.session_state.event_name)
                st.success("Data exported to Excel successfully!")

            # Display a histogram of prices
            st.subheader("Histogram of Prices")
            fig_hist = px.histogram(expense_df, x="Price", nbins=20, title="Price Distribution")
            st.plotly_chart(fig_hist)

            # Display a pie chart of expense categories
            st.subheader("Pie Chart of Expense Categories")
            category_counts = expense_df["Category"].value_counts()
            fig_pie = px.pie(names=category_counts.index, values=category_counts.values, title="Expense Categories")
            st.plotly_chart(fig_pie)

            st.sidebar.subheader("Delete Expenses:")
            for index, row in expense_df.iterrows():
                if st.sidebar.button(f"Delete ID {row['ID']}"):
                    delete_budget_item(st.session_state.event_name, row['ID'])

        else:
            st.info("No expenses registered yet for this event.")
    else:
        st.info("This event has no registered expenses.")
