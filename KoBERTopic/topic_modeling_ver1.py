from sklearn.feature_extraction.text import CountVectorizer
from konlpy.tag import Okt
from bertopic import BERTopic
import pandas as pd

# 전처리된 CSV 파일 불러오기
df = pd.read_csv('preprocessed.csv', index_col=0)

# 전처리된 텍스트 데이터를 최종 칼럼 변수로 설정
docs = df['post_preprocessed']
# print(docs)

class CustomTokenizer:
    """
    형태소 분석기를 래핑하여 토큰화를 수행하는 클래스

    Parameters:
        tagger (object): 형태소 분석기 객체
    """

    def __init__(self, tagger):
        """
        CustomTokenizer 클래스의 초기화 메서드

        Parameters:
            tagger (object): 형태소 분석기 객체
        """
        self.tagger = tagger

    def __call__(self, sent):
        """
        형태소 분석기를 사용하여 입력 문장을 토큰화하는 메서드

        Parameters:
            sent (str): 입력 문장

        Returns:
            list: 길이가 1보다 큰 토큰 리스트
        """
        sent = sent[:1000000]  # 입력 문장이 너무 길 경우, 1000000자 이하로 자름
        word_tokens = self.tagger.nouns(sent)  # 형태소 분석기를 사용하여 명사로 토큰화
        result = [word for word in word_tokens if len(word) > 1]  # 길이가 1보다 큰 토큰만 결과에 포함
        return result

# Okt 형태소 분석기를 사용하는 CustomTokenizer 인스턴스 생성
custom_tokenizer = CustomTokenizer(Okt())

# CustomTokenizer를 사용하여 텍스트 데이터를 벡터화
vectorizer = CountVectorizer(tokenizer=custom_tokenizer, max_features=3000)

# BERTopic 모델 설정
model = BERTopic(
    embedding_model="sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens",  # 임베딩 모델 지정
    vectorizer_model=vectorizer,  # 벡터화 모델 지정
    nr_topics=10,  # 토픽 개수 지정
    min_topic_size=5,  # 최소 토픽 크기 지정
    top_n_words=10,  # 각 토픽당 상위 단어 개수 지정
    calculate_probabilities=True  # 확률 계산 설정
)

# 전처리가 완료된 텍스트 데이터로 BERTopic 모델 학습 및 토픽 추출
topics, probs = model.fit_transform(docs)

# 각 토픽 출력
for i in range(10):
    print(i, '번째 토픽 :', model.get_topic(i))