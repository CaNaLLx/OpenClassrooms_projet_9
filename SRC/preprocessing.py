import string
import preprocessor as p

p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG, p.OPT.EMOJI)


def clean_tweet(text):
    text = p.clean(text).lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())
