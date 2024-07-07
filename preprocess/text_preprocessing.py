import re

def remove_urls(text):
    """
    텍스트에서 URL을 제거합니다.
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_emails(text):
    """
    텍스트에서 이메일 주소를 제거합니다.
    """
    email_pattern = re.compile(r'\S*@\S*\s?')
    return email_pattern.sub(r'', text)

def remove_new_line(text):
    """
    여러 개의 공백 문자 또는 줄 바꿈 문자를 하나의 공백 문자로 대체합니다.
    """
    return re.sub(r'\s+', ' ', text)

def remove_non_alpha(text):
    """
    텍스트에서 한글, 숫자, 알파벳 및 공백 문자를 제외한 모든 문자를 제거합니다.
    """
    return re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str(text))

def preprocess_text(text):
    """
    텍스트에 URL 제거, 이메일 제거, 줄 바꿈 제거, 비알파벳 문자 제거를 포함한 전처리 과정을 적용합니다.
    """
    t = remove_urls(text)
    t = remove_emails(t)
    t = remove_new_line(t)
    t = remove_non_alpha(t)
    return t

def remove_stopwords(text, stopwords):
    """
    텍스트에서 불용어를 제거합니다.
    """
    return " ".join([word for word in str(text).split() if word not in stopwords])