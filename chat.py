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


folder = "mai-shen-yun-main"
months = ["May","June","July","August","September","October"]

all_data = []
for month in months:
    month_file = f"{folder}/{month}/{month}_Data_Items.csv"
    if os.path.exists(month_file):
        df = pd.read_csv(month_file)
        df['Month'] = month
        all_data.append(df)
historical_data = pd.concat(all_data, ignore_index=True)

# # Read each month's CSV manually
# may_data = pd.read_csv(f"{folder}/May/May_Data_Items.csv")
# june_data = pd.read_csv(f"{folder}/June/June_Data_Items.csv")
# july_data = pd.read_csv(f"{folder}/July/July_Data_Items.csv")
# august_data = pd.read_csv(f"{folder}/August/August.csv")
# september_data = pd.read_csv(f"{folder}/September/September_Data_Items.csv")
# october_data = pd.read_csv(f"{folder}/October/October_Data_Items.csv")

# # Add a month column to each
# may_data['Month'] = 'May'
# june_data['Month'] = 'June'
# july_data['Month'] = 'July'
# august_data['Month'] = 'August'
# september_data['Month'] = 'September'
# october_data['Month'] = 'October'

# Combine into one DataFrame
historical_data = pd.concat([may_data, june_data, july_data, august_data, september_data, october_data], ignore_index=True)



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
            {"role": "user", "content": context_text + "\n\nQuestion: " +user_input}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"

    data = response.json()
    # Extract the assistant's message
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "Error parsing response from OpenRouter."
