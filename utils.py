import re

def clean_text(text):
    t = re.sub("[\t\n\r]", " ", text)
    return re.sub(" +", " ", t).strip()
