import requests
from io import BytesIO

def get_story_image(paragraphs):
    pics = []
    for paragraph in paragraphs:
        # send paragraph to model to generate image
        # TODO: make this async so we can send multiple image requests at a time
        response = requests.get("https://picsum.photos/200/300")
        pic = BytesIO(response.content)
        pics.append(pic)
    
    return pics



if __name__ == "__main__":
    print(get_story_image(["Once upon a time, in a land full of sunshine and laughter, lived a little girl named Lily. Lily had a smile that could light up the whole world. She loved to play with her friends, skip through fields of wildflowers, and sing silly songs to the birds."]))
