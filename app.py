import dotenv
import openai
import os
import sqlite3
import datetime
import argparse
from openai import OpenAI
import pandas as pd

# Load the .env file
dotenv.load_dotenv()

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the prompt
prompt = ''

#  query chatgpt
def query(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an expert assistant and teacher, skilled in explaining how to further learn, develop and grow to someone attempting to build new skills. The user is attempting to learn Japanese"},
        {"role": "user", "content": prompt}
    ]
    )

    print(completion.choices[0].message)

def save_data(today, activity, duration, positive_aspects, challenges):
    # connect to database
    conn = sqlite3.connect('journal.db')
    c = conn.cursor()

    # create table
    c.execute('''CREATE TABLE IF NOT EXISTS journal
                 (today date, activity text, duration text, positive_aspects text, challenges text)''')

    # insert data
    c.execute("INSERT INTO journal VALUES (?, ?, ?, ?, ?)", (today, activity, duration, positive_aspects, challenges))

    # commit and close
    conn.commit()
    conn.close()

    # print out the data
    print("Activity: ", activity)
    print("Duration: ", duration)
    print("Positive Aspects: ", positive_aspects)
    print("Challenges: ", challenges)

    # generate a summary
    prompt = f"I did {activity} today. It took {duration}. What went well was {positive_aspects}. What went badly was {challenges}."
    # summary = query(prompt)
    # print("Summary: ", summary)

def summarise_month():
    """Query the db for what happened in the month and create a gpt prompt to summarize what happened"""
    conn = sqlite3.connect('journal.db')
    query = "SELECT * FROM journal"
    df = pd.read_sql_query(query, conn)
    print(df)
    return df
    # summary = query(prompt)
    # print("Summary: ", summary)



def main():
    # today = datetime.date.today()
    # code block to save 10 days of data into the db
    dt = datetime.date(2024,7, 1)
    for _ in range(10):
        today = dt + datetime.timedelta(days=1)

        # ask user what they did today
        activity = input("What did you do today? ")

        # ask user how long for?
        duration = input("How long did it take? ")

        # ask user what went well
        positive_aspects = input("What went well? ")

        # ask user what went badly
        challenges = input("What went badly? ")

        # save data to database
        save_data(today, activity, duration, positive_aspects, challenges)

    # code block to summarise the month
    df = summarise_month()

    # query chatgpt
    prompt = f'Given the following tabular data, summarise what I did this month, what went well and what could be improved for the future. \n{df}'
    query(prompt)


if __name__ == "__main__":
    main()
