import pandas as pd
from flask import Flask, render_template
import os
import logging

from project_root import PROJECT_ROOT

# Initialize the Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the CSV file
CSV_FILE_PATH = PROJECT_ROOT / 'out' / 'listings.csv'

@app.route('/')
def display_table():
    try:
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(CSV_FILE_PATH)
        # Convert DataFrame to a list of dictionaries for easier rendering in template
        headers = data.columns.tolist()
        rows = data.values.tolist()
        return render_template('index.html', headers=headers, rows=rows)
    except FileNotFoundError:
        logging.error(f"CSV file not found at {CSV_FILE_PATH}")
        return "Error: The CSV file was not found. Please check the CSV_FILE_PATH.", 404
    except pd.errors.EmptyDataError:
        logging.error(f"CSV file at {CSV_FILE_PATH} is empty.")
        return "Error: The CSV file is empty. Please provide valid data.", 400
    except Exception as e:
        logging.exception("An unexpected error occurred while processing the CSV file.")
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    # Ensure required directories exist
    templates_dir = os.path.join(PROJECT_ROOT, 'templates')
    out_dir = os.path.join(PROJECT_ROOT, 'out')

    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(CSV_FILE_PATH):
        logging.warning(f"'{CSV_FILE_PATH}' not found.")
        logging.info("Please create the CSV file or update CSV_FILE_PATH in app.py.")
        # Optionally create a dummy CSV for demonstration
        # dummy_df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
        # dummy_df.to_csv(CSV_FILE_PATH, index=False)
        # logging.info(f"Created a dummy CSV at '{CSV_FILE_PATH}' for demonstration.")

    logging.info("Starting Flask application...")
    app.run(debug=True)
