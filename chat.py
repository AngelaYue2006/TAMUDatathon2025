# chat.py
import os
import requests
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"  # OpenRouter chat endpoint

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found. Make sure it's in your .env file.")

folder = "data"
months = ["May","June","July","August","September","October"]

all_data = []
for month in months:
    month_file = f"{folder}/{month}/{month}_Data_Items.csv"
    if os.path.exists(month_file):
        df = pd.read_csv(month_file)
        df['Month'] = month
        all_data.append(df)
historical_data = pd.concat(all_data, ignore_index=True)

# Calculate ingredient summary per month
ingredient_summary = historical_data.groupby(['Month', 'Item Name']).agg(
    total_count=('Count','sum'),
    total_revenue=('Amount','sum')
).reset_index()

# Define thresholds for understocking and overstocking
UNDERSTOCK_THRESHOLD = 100  # example units
OVERSTOCK_THRESHOLD = 1000  # example units

understocked = ingredient_summary[ingredient_summary['total_count'] < UNDERSTOCK_THRESHOLD]
overstocked = ingredient_summary[ingredient_summary['total_count'] > OVERSTOCK_THRESHOLD]

# Generate context text for the chatbot
context_lines = ["Ingredient usage summary by month:"]
for month in months:
    context_lines.append(f"\n{month}:")
    month_data = ingredient_summary[ingredient_summary['Month'] == month]
    for _, row in month_data.iterrows():
        context_lines.append(f"- {row['Item Name']}: {row['total_count']} units sold")

context_lines.append("\nUnderstocked items (low sales):")
for _, row in understocked.iterrows():
    context_lines.append(f"- {row['Month']}: {row['Item Name']} ({row['total_count']} units)")

context_lines.append("\nOverstocked items (high sales):")
for _, row in overstocked.iterrows():
    context_lines.append(f"- {row['Month']}: {row['Item Name']} ({row['total_count']} units)")

context_text = "\n".join(context_lines)

# to use gemini: "google/gemini-2.5-flash"
# to use gpt: "gpt-4o-mini"
def get_chat_response(user_input: str, model: str = "gpt-4o-mini") -> str:
    """
    Sends user input to OpenRouter and returns the chatbot response.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a data analyst who explains insights clearly and precisely."},
            {"role": "user", "content": context_text + "\n\nQuestion: " + user_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "Error parsing response from OpenRouter."