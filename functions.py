import random, string, requests
from wtforms import ValidationError


def get_url_name():
    # Gets some random numbers and letters
    numbers = random.randint(10000,99999)
    letters = ''.join(random.choice(string.ascii_letters) for letter in range(8))

    # What the URL can contain
    url_contains = str(numbers) + letters
    # Adds all characters to a list, then shuffles them and turns it into a string
    url_contains = [character for character in url_contains] 
    random.shuffle(url_contains)
    url_name = ''.join(url_contains)

    return url_name

def is_youtube_video(form, field):
    not_youtube_video = True
    r = requests.get(field.data) 
    if "Video unavailable" in r.text:
        not_youtube_video = True
    if "watch?v=" in field.data:
        return
    if "embed" in field.data:
        return
    if not_youtube_video:
        raise ValidationError("This is not a valid YouTube video, please try again!")