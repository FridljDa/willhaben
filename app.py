import pandas as pd
from flask import Flask, render_template
import os

from project_root import PROJECT_ROOT

# Initialize the Flask application
app = Flask(__name__)

# Define the path to the CSV file
# Assuming PROJECT_ROOT is the directory where app.py is located

CSV_FILE_PATH = PROJECT_ROOT / 'out' / 'listings.csv'

@app.route('/')
def display_table():
  try:
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(CSV_FILE_PATH)
    # Convert DataFrame to a list of dictionaries for easier rendering in template
    # or use data.to_html(classes='display', table_id='myTable') for direct HTML table

    # For DataTables.net, it's often easier to pass column headers and row data separately
    headers = data.columns.tolist()
    rows = data.values.tolist()

    return render_template('index.html', headers=headers, rows=rows)
  except FileNotFoundError:
    return "Error: The CSV file was not found. Please check the CSV_FILE_PATH.", 404
  except Exception as e:
    return f"An error occurred: {e}", 500


if __name__ == '__main__':
  # Create the 'templates' and 'out' directories if they don't exist
  if not os.path.exists(os.path.join(PROJECT_ROOT, 'templates')):
    os.makedirs(os.path.join(PROJECT_ROOT, 'templates'))
  if not os.path.exists(os.path.join(PROJECT_ROOT, 'out')):
    os.makedirs(os.path.join(PROJECT_ROOT, 'out'))
    print("Created 'out' directory. Please place your listings.csv file there.")

  # Reminder to create a dummy CSV if it doesn't exist, for testing
  if not os.path.exists(CSV_FILE_PATH):
    print(f"Warning: '{CSV_FILE_PATH}' not found.")
    print("Please create the CSV file or update CSV_FILE_PATH in app.py.")
    # You might want to create a dummy CSV for initial setup if it's missing
    # For example:
    # dummy_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    # dummy_df.to_csv(CSV_FILE_PATH, index=False)
    # print(f"Created a dummy CSV at '{CSV_FILE_PATH}' for demonstration.")

  app.run(debug=True)