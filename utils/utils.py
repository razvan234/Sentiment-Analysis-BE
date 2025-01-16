import re


def extract_values(url):
    # Find all matches of the pattern =...&
    matches = re.findall(r'=(.*?)&', url)
    return matches[0] if matches else None


def clean_text(sentence):
    # Remove URLs
    sentence = re.sub(r'http\S+', '', sentence)
    # Remove single quotes
    sentence = re.sub(r"'", '', sentence)
    # Remove HTML tags
    sentence = re.sub(r'<.*?>', '', sentence)
    # Remove extra whitespaces
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence
