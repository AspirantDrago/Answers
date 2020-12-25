import re


def get_prepare_text(text):
    p = re.compile(r'<.*?>')
    text = p.sub('', text)
    text = text.strip().lower()
    text = ''.join(filter(str.isprintable, text))
    return text
