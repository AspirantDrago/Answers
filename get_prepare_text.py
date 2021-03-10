import re


def get_prepare_text(text):
    p = re.compile(r'<.*?>')
    text = p.sub('', text)
    text = text.replace('\n\r', ' ').replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip().lower()
    text = ''.join(filter(str.isprintable, text))
    return text
