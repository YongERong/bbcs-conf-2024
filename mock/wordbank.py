import json
import random

class Wordbank:
    def __init__(self, wordbank_path) -> None:
        with open(wordbank_path, "r") as f:
            self.wordbank = json.load(f)

    def get_challenge_words(self, count):
        return random.sample(self.wordbank, count)
    

if __name__ == "__main__":
    test = Wordbank("/Users/e-rongyong/Python/bbcs-conf-2024/mock/wordbank.json")
    print(test.get_challenge_words(3))

        

    