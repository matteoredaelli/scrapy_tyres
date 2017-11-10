import re

def clean_text(text):
    if text is None or text=="":
        return text
    t = re.sub("[\t\n\r]", " ", text)
    return re.sub(" +", " ", t).strip()

def clean_dict(d):
    for i in d:
        d[i] = clean_text(d[i])
    return d
