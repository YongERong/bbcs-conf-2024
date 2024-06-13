import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
import getpass
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
print(dotenv_path)
load_dotenv(dotenv_path)

# accessing and printing value
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_words_path(age):
    if age <= 3:
        return "data/words_1_3.json"
    elif age <= 6:
        return "data/words_4_6.json"
    elif age <= 9:
        return "data/words_7_9.json"
    return None

def get_words(words_path, key="word"):
    with open(words_path) as f:
        data = json.load(f)
        return [item[key] for item in data]

def generate_story(age, topic, words, api_key):
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a children book author and you write books for children. Return a story of 5 paragraphs, with a maximum of 3 sentences per paragraph."
                )
            ),
            HumanMessagePromptTemplate.from_template("Create a story for kids ages {age} on {topic} and include 3 words from the {list} list. when returning the story, bold the words you used and place the words used into a python array."),
        ]
    )
    
    chat_message = chat_template.format_messages(age=age, topic=topic, list=words)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True, google_api_key=api_key)

    results = llm.invoke(chat_message)
    return results.content

def main():
    topic = input("Enter the topic: ")
    print(topic)
    
    age = int(input("Enter the age: "))
    print(age)

    words_path = get_words_path(age)
    words = get_words(words_path)
    print(words)
    
    # GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"  # Replace with your actual API key
    story = generate_story(age, topic, words, GOOGLE_API_KEY)
    print(story)

if __name__ == "__main__":
    main()
