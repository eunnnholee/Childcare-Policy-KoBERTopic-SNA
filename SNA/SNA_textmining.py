import numpy as np
import pandas as pd
from gensim import corpora, models

def load_data(file_path):
    """
    CSV 파일을 불러오는 함수

    Parameters:
    - file_path (str): 불러올 CSV 파일의 경로

    Returns:
    - DataFrame: 불러온 데이터프레임
    """
    return pd.read_csv(file_path, encoding="utf-8", index_col=0)

def remove_stopwords(text, stopwords):
    """
    불용어를 제거하는 함수

    Parameters:
    - text (str): 입력 텍스트
    - stopwords (list): 불용어 리스트

    Returns:
    - str: 불용어가 제거된 텍스트
    """
    return " ".join([word for word in str(text).split() if word not in stopwords])

def preprocess_data(df, stopwords):
    """
    데이터프레임에서 불용어를 제거하는 함수

    Parameters:
    - df (DataFrame): 입력 데이터프레임
    - stopwords (list): 불용어 리스트

    Returns:
    - DataFrame: 불용어가 제거된 데이터프레임
    """
    df['nouns'] = df['nouns'].apply(lambda post: remove_stopwords(post, stopwords))
    return df

def get_bow_vectors(posts):
    """
    문서의 BOW 벡터를 구하는 함수

    Parameters:
    - posts (list): 단어 리스트로 분리된 문서 리스트

    Returns:
    - list: BOW 벡터 리스트
    - Dictionary: 단어 사전
    """
    id2word = corpora.Dictionary(posts)
    corpus_tf = [id2word.doc2bow(text) for text in posts]
    return corpus_tf, id2word

def calculate_tfidf(corpus_tf):
    """
    TF-IDF 값을 계산하는 함수

    Parameters:
    - corpus_tf (list): BOW 벡터 리스트

    Returns:
    - list: TF-IDF 값을 계산한 리스트
    - TfidfModel: TF-IDF 모델
    """
    tfidf = models.TfidfModel(corpus_tf)
    corpus_tfidf = tfidf[corpus_tf]
    return corpus_tfidf, tfidf

def get_high_tfidf_words(corpus_tfidf, id2word, threshold=5):
    """
    TF-IDF 값이 일정 기준 이상인 단어를 추출하는 함수

    Parameters:
    - corpus_tfidf (list): TF-IDF 값을 계산한 리스트
    - id2word (Dictionary): 단어 사전
    - threshold (float): TF-IDF 값 기준

    Returns:
    - list: TF-IDF 값이 기준 이상인 단어 리스트
    """
    word_tfidf_sums = {}

    for doc in corpus_tfidf:
        for word_id, tfidf_value in doc:
            word = id2word[word_id]
            if word in word_tfidf_sums:
                word_tfidf_sums[word] += tfidf_value
            else:
                word_tfidf_sums[word] = tfidf_value

    sorted_word_tfidf_sums = sorted(word_tfidf_sums.items(), key=lambda x: x[1], reverse=True)
    high_tfidf_words = [word for word, tfidf_sum in sorted_word_tfidf_sums if tfidf_sum >= threshold]

    return high_tfidf_words

def remove_irrelevant_words(words, remove_list):
    """
    불필요한 단어를 제거하는 함수

    Parameters:
    - words (list): 단어 리스트
    - remove_list (list): 제거할 단어 리스트

    Returns:
    - list: 불필요한 단어가 제거된 단어 리스트
    """
    for remove_word in remove_list:
        try:
            words.remove(remove_word)
        except ValueError:
            continue
    return words

def calculate_cooccurrence(texts, target_words):
    """
    단어 쌍의 동시 출현 빈도를 계산하는 함수

    Parameters:
    - texts (Series): 텍스트 데이터
    - target_words (list): 타겟 단어 리스트

    Returns:
    - list: 단어 쌍의 동시 출현 빈도 리스트
    """
    cooccur = {}

    for text in texts:
        words = set(text.split())
        words = list(words)

        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                word1 = words[i]
                word2 = words[j]
                if (word1, word2) in cooccur:
                    cooccur[(word1, word2)] += 1
                elif (word2, word1) in cooccur:
                    cooccur[(word2, word1)] += 1
                else:
                    cooccur[(word1, word2)] = 1

    cooccur_list = list(cooccur.items())

    final_edgelist = [(pair, weight) for pair, weight in cooccur_list if pair[0] in target_words and pair[1] in target_words]

    return final_edgelist

def save_sna_data(final_edgelist, file_path):
    """
    SNA 데이터를 저장하는 함수

    Parameters:
    - final_edgelist (list): 최종 edge 리스트
    - file_path (str): 저장할 파일 경로

    Returns:
    - None
    """
    df1 = pd.DataFrame(final_edgelist, columns=['Word', 'Weight'])

    series_split1 = df1["Word"].apply(lambda x: x[0])
    series_split2 = df1["Word"].apply(lambda x: x[1])

    SNA_data = pd.DataFrame({
        "Source": series_split1,
        "Target": series_split2,
        "Weight": df1["Weight"]
    })

    SNA_data.to_csv(file_path, encoding="utf-8", index=False)

def main():
    # 데이터 불러오기
    df = load_data('konlpy이후.csv')

    # 추가 불용어 정의 및 제거
    stop_words = "것 저 수 분 데 중 전 일 때 이 안녕 육아휴직 육휴 육아 휴직 출산휴가"
    stop_words = stop_words.split(' ')
    df = preprocess_data(df, stop_words)

    # BOW 벡터 구하기
    posts = [x.split(' ') for x in df['nouns']]
    corpus_tf, id2word = get_bow_vectors(posts)

    # TF-IDF 모델 생성 및 계산
    corpus_tfidf, tfidf = calculate_tfidf(corpus_tf)

    # TF-IDF 값이 5 이상인 단어 추출
    high_tfidf_words = get_high_tfidf_words(corpus_tfidf, id2word, threshold=5)

    # 의미 없는 단어 제거
    remove_list = """
    다음날 연락 15일 질문드 몸 얘 바 날 그 2일 축 10일 이거 동안 29일 육 여기 앞 되는거 둘다 인정 예정인데요
    곳 150 3일 5일 어느정도 12일 이럴경우 21일 이런경우 4일 진짜 걸 건가요 20일 개 19일 14일 육아휴직이요 4 정확 대
    2023 봐주세용 관련해서 몇 체크 줄 정도 위 듯 라 누구 끝 편 육아휴직1년 반 어제 의견 예 있는거 다음주 25 부 25일
    23일 17일 5 13일 100 일요일 금요일 한 안쓰 뭔가 45 18일 이런식 23 31 궁금 1월 2월 3월 4월 5월 6월 7월 8월 9월
    10월 11월 12월 1일 다들 근데 1 들 감사 애 부탁드 부터 관련 오늘 2 지 무 후 내 어마 질문이요 나 계 저희 되 3
    문의드 이번 맘님들 있을까요 그때 리 자 첫 문 적 육아휴직중이 안 거
    """
    remove_list = remove_list.split(' ')
    high_tfidf_words = remove_irrelevant_words(high_tfidf_words, remove_list)

    # 단어 쌍의 동시 출현 빈도 계산
    final_edgelist = calculate_cooccurrence(df['nouns'], high_tfidf_words)

    # SNA 데이터 저장
    save_sna_data(final_edgelist, "SNA_df.csv")

if __name__ == "__main__":
    main()