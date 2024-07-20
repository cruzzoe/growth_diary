import dotenv
import openai
import os
import sqlite3
import datetime
import argparse

# Load the .env file
dotenv.load_dotenv()

# Set the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the prompt
prompt = ''

#  query chatgpt
def query(prompt):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()    


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


def main():
    today = datetime.date.today()
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


if __name__ == "__main__":
    main()
