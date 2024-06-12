from . import get_story_image, get_story_text, wordbank

# TODO: Deal with janky imports
get_story_text = get_story_text.get_story_text
get_story_image = get_story_image.get_story_image


def get_story(prompt, challenge_word_count):
    challenge_words = wordbank.Wordbank("/Users/e-rongyong/Python/bbcs-conf-2024/mock/wordbank.json")
    
    challenge_dict = dict(challenge_words.get_challenge_words(challenge_word_count))
    words = challenge_dict.keys()

    paragraphs = get_story_text(prompt, words)
    images = get_story_image(paragraphs)
    

    return {"paragraphs": paragraphs, "images":images, "challenge_dict":challenge_dict}

if __name__ == "__main__":
    print(get_story("Prompt", 5))
