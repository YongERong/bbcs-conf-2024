def get_story_text(prompt, challenge_words):

    # generate text here, prompt to signal challenge words using **word**
    text = """Once upon a time, in a land full of sunshine and laughter, lived a little girl named Lily. Lily had a smile that could light up the whole world. She loved to play with her friends, skip through fields of wildflowers, and sing silly songs to the birds.
One sunny morning, Lily was playing in the park when she saw a tiny, fluffy bunny hiding behind a tree. The bunny looked scared and lost, its little nose twitching. Lily gently approached the bunny, offering it a piece of her apple. The bunny, surprised by Lily's kindness, nibbled on the apple and seemed to relax a bit.
Lily decided to name the bunny "Sunshine" because its fur was as bright as the sun. She took Sunshine home with her, and her parents were thrilled to have a new furry friend. They built a cozy little house for Sunshine in the garden, filled with soft hay and fresh vegetables.
Lily and Sunshine became the best of friends. They spent their days playing together, Sunshine **hopping** around the garden while Lily giggled with joy. Lily even learned to teach Sunshine tricks, like rolling over and fetching a ball.
Every day, Lily's smile grew even brighter, knowing that she had brought Sunshine into her life and made a new friend who brought happiness to her heart. Lily and Sunshine lived happily ever after, sharing their love and laughter with everyone they met."""

    return [text.split("\n")]


if __name__ == "__main__":
    print(get_story_text(""))
