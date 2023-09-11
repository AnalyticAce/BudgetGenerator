# Budget Generator

This is a Budget Generator project that allows you to manage and track expenses for various events or sessions. You can upload old events, add new sessions, add expenses, view registered expenses, export data to Excel, and delete expenses. The project uses Streamlit for the user interface, Pandas for data management, and Plotly Express for data visualization.

## Project Structure

The project is structured as follows:

- `src/`: This directory contains the main Streamlit application.
  - `config.json`: A configuration file used to store budget data, including event information and expenses.
  - `main.py`: The main Python script that implements the Streamlit app and its functionalities.
- `requirements.txt`: A file listing Python packages required for the project. You can install these dependencies using the command `pip install -r requirements.txt`.
- `README.md`: The documentation you are currently reading, explaining the project structure and functionalities.

## Functionalities

### Upload Old Event

- Select "Log Old Event" from the main menu.
- Choose an existing event from the dropdown list to edit its details.

### Add New Session

- Select "Add New Session" from the main menu.
- Enter the event name and date for the new session.
- Choose an expense category from the predefined list.
- Provide a particular description of the expense.
- Input the quantity, description, and price for the expense.
- Click "Add Expense" to register the expense for the current session.

### Manage Expenses

- After selecting an event (either a logged old event or a new session), you can manage expenses for that event.
- Enter the expense details (category, particular, quantity, description, and price) and click "Add Expense" to register the expense.
- Registered expenses are displayed in a table below the input section.
- You can also visualize the expenses with a histogram of prices and a pie chart of expense categories.

### Export Data to Excel

- You can export the registered expenses to an Excel file for further analysis or record-keeping.
- Click "Export to Excel" to generate an Excel file containing the expense data for the selected event.

### Delete Expenses

- Registered expenses can be deleted by clicking the "Delete" button next to each expense in the table.
- Clicking the "Delete" button will remove the selected expense from the event's records.

## How to Run

To run the Budget Generator project, follow these steps:

1. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

2. Start the Streamlit application by running:

```bash
streamlit run src/main.py
```

This will launch the Budget Generator app in your web browser, allowing you to use all the features and functionalities mentioned above.

Enjoy managing your event expenses with the Budget Generator!