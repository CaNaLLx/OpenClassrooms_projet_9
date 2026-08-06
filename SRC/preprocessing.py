import string
import re
import preprocessor as p
import emoji

p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG, p.OPT.EMOJI)

# Regex & constantes globales
RE_URL     = re.compile(r"https?://\S+|www\.\S+")
RE_MENTION = re.compile(r"@\w+")
RE_SPACE   = re.compile(r"\s+")
RE_ELONG   = re.compile(r"(.)\1{2,}")
HTML_MAP   = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&#39;": "'"}

def segment_hashtag_text(text: str) -> str:
    # Fonction de secours au cas où vous ne l'avez pas encore définie
    return re.sub(r"#(\w+)", r"\1", text)


def clean_tweet_LSTM(text: str) -> str:
    text = p.clean(text).lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())


def clean_tweet_SETFIT(text: str, demojize: bool = True, segment_hashtags: bool = True) -> str:
    # 1. Entités HTML
    for k, v in HTML_MAP.items():
        text = text.replace(k, v)

    # 2. URLs et mentions → placeholders
    text = RE_URL.sub("http", text)
    text = RE_MENTION.sub("@user", text)

    # 3. Émojis → description textuelle
    if demojize:
        text = emoji.demojize(text, delimiters=(" :", ": "))

    # 4. Hashtags → segmentation
    if segment_hashtags:
        text = segment_hashtag_text(text)

    # 5. Élongations
    text = RE_ELONG.sub(r"\1\1", text)

    # 6. Espaces
    return RE_SPACE.sub(" ", text).strip()
