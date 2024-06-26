import json
import os
import re
import requests
from io import BytesIO
from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from gtts import gTTS

#load environment variables
dotenv_path = find_dotenv()
print(dotenv_path)
load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
JIGSAW_API_KEY = os.getenv("JIGSAW_API_KEY")


def get_words_path(age):
    if age <= 3:
        return "../data/words_1_3.json"
    elif age <= 6:
        return "../data/words_4_6.json"
    elif age <= 9:
        return "../data/words_7_9.json"
    return None

def get_words(words_path, key="word"):
    with open(words_path) as f:
        data = json.load(f)
        return [item[key] for item in data]

def generate_story(age, topic, words):
    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    """You are a children book author and you write books for children. 
                    Return a story of 5 paragraphs, with a maximum of 3 sentences per paragraph."""
                )
            ),
            HumanMessagePromptTemplate.from_template("""Create a story for kids ages {age} on {topic} and include only 3 words from the {list} list. 
                                                    When returning the story, italics the words you used.
                                                    After each paragraph, include a prompt to generate an image that shows the story of each paragraph.
                                                    When displaying the story, prompt and words, use the following format:
                                                    story: story
                                                    prompt: prompt
                                                    At the end of all the paragraphs, include all the words used using the format below.
                                                    words_used: word1, word2, word3
                                                    """),
        ]
    )
    chat_message = chat_template.format_messages(age=age, topic=topic, list=words)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True, google_api_key=GOOGLE_API_KEY)
    results = llm.invoke(chat_message)
    return results.content

def extract_text(gemini_output):
    stories = re.findall(r"story:\s*(.*?)(?=\n|$)", gemini_output, re.DOTALL)
    prompts = re.findall(r"prompt:\s*(.*?)(?=\n|$)", gemini_output)
    words_used = re.findall(r"words_used:\s*(.*?)(?=\n|$)", gemini_output)

    stories = [story.strip() for story in stories]
    prompts = [prompt.strip() for prompt in prompts]
    words_used = words_used[0].split(', ') if words_used else []

    return stories, prompts, [word.strip() for word in words_used]

def generate_image(prompt, size="small", model="sd1.5"):
    endpoint = "https://api.jigsawstack.com/v1/ai/image_generation"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": JIGSAW_API_KEY
    }
    body = {
        "prompt": "comic style" + prompt,
        "size": size,
        "model": model
    }

    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code == 200:
        print(f"Image generated for prompt: {prompt}")
        return BytesIO(response.content)
    else:
        print(f"Failed to generate image for prompt: {prompt}. Status code: {response.status_code}")
        print(response.text)
        return None

def generate_and_save_images(prompts):
    images = []
    for counter, prompt in enumerate(prompts):
        try:
            image_data = generate_image(prompt)
            if image_data:
                images.append(image_data)
                # #save image
                # with open(f'img_{counter}.png', 'wb') as f:
                #     f.write(image_data.getbuffer())
        except Exception as e:
            print(f"Error generating or saving image for prompt {counter}: {e}")
    print(f"Generated {len(images)} images.")
    return images

def generate_audio(text):
    story_audio = gTTS(text=text.replace("*", ""), lang="en", tld="co.uk", slow=False)
    return story_audio

def generate_and_save_story_audio(stories):
    for counter, story in enumerate(stories):
        try:
            story_audio = generate_audio(story)
            story_audio.save(f'data/para_audio/para{counter+1}.mp3')
        except Exception as e:
            print(f"Error generating or saving audio for story {counter}: {e}")

def generate_and_save_word_audio(words):
    for word in words:
        try:
            file_path = f'data/word_audio/{word}.mp3'
            if os.path.exists(file_path):
                continue
            word_audio = generate_audio(word)
            word_audio.save(file_path)
        except Exception as e:
            print(f"Error generating or saving audio for word '{word}': {e}")

def main(topic:str, age:int):

    words_path = get_words_path(age)
    words = get_words(words_path)
    
    gemini_output = generate_story(age, topic, words)

    stories, prompts, words_used = extract_text(gemini_output)
    print(f'Stories list: {stories}')
    print(f'Image Prompts list: {prompts}')
    print(f'Words Used list: {words_used}')

    images = generate_and_save_images(prompts)
    generate_and_save_story_audio(stories)
    generate_and_save_word_audio(words_used)

    return {"paragraphs":stories, "images":images, "words_used":words_used}


if __name__ == "__main__":
    main()
