import pandas as pd
from text_preprocessing import preprocess_text, remove_stopwords

# 크롤링한 csv 파일 불러오기
df = pd.read_csv('Crawling.csv')

# 제목과 내용을 합친 'post' column
df = pd.DataFrame({'post': df['new']})

# 전처리 적용
df['post_preprocessed'] = df['post'].apply(preprocess_text)

# 전처리된 데이터를 csv 파일로 저장
df.to_csv('preprocessed.csv', encoding='utf-8', index=False)