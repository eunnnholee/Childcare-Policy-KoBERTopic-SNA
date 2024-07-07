# 육아지원정책: KoBERTopic과 SNA를 통한 심층 분석 

## I. 프로젝트 개요

### 데이터셋: 
> -  네이버 맘카페 '맘스홀릭베이베' 개시글 제목과 내용 크롤링 (약 4000개의 텍스트 데이터)
> -  육아 및 출산과 관련된 대표적인 정책 중 하나인 ‘육아휴직’을 키워드로 선정
> -  ‘육아휴직’ 키워드가 포함된 질문이 가장 많은 상위 4개의 게시판 선정
> -  약 1년간의 누적 게시글 데이터를 크롤링

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/crawler/naver_cafe_crawler.py)

​
### Research Question: 

> 정권교체와 시기에 따른 육아지원 정책들이 꾸준하게 신규 수립되고 수정되고 있다. 그렇다면 정작 바뀌는 정책에 따라 부모들은 이러한 정보를 정확하게 인지 하고 있을까?

</br>

### 연구 배경:

> 직장을 병행하는 부모의 입장에서 꾸준한 정보의 생성은 정보의 비대칭을 야기할 것으로 판단된다. 많은 육아지원정책이 존재하지만, 워라밸을 중시하는 현재 시기에서 육아휴직에 대한 논의는 끊이지 않고 있다. 매년 새로운 육아휴직 제도가 새롭게 제정되고 있으며, 예를 들어 '3+3 육아휴직제도'와 '아빠 육아휴직 장려금' 등이 있다. 이렇게 매번 변하고 어려운 육아지원정책에 대한 정보를 더 쉽고 명확하게 전달할 수 있는 방법을 마련하는 것이 이번 연구의 배경이자 목표이다. 

​

### 방법론:
1. TF-IDF

> -  정보검색과 텍스트마이닝에서 이용하는 가중치, 어떤 단어가 특정문서에서 얼마나 중요한지를 나타내는 통계적 수치이다.
> -  모든 문서에서 자주 등장하는 단어는 중요도가 낮다고 판단하며, 특정 문서에만 자주 등장하는 단어는 중요도가 높다고 판단한다. 다시말해, TF-IDF 값이 낮으면 중요도가 낮은 것이며 반대로 크면 중요도가 큰 것이다.
>    -  즉, 문장에서는 많이 나오는데, 문서 전체에서는 적게 나오는 단어를 중요도가 높다고 판단한다.
> -  본 연구에서는 '육아휴직', '기간' 등과 같은 단어의 경우에는 모든 문서에 자주 등장하기 때문에 자연스럽게 TF-IDF의 값이 다른 단어에 비해서 낮아지게 된다.



2. Social Network Analysis

> -  사회적 관계망을 분석하는 기술로, 개인 또는 조직 사이의 관계와 상호작용을 시각화하여 분석하는 방법이다.
> - 이때 Node는 질문에서 토픽이 되어 자주 등장하는 단어들이 될 것이며, Weight은 각 단어들이 게시글 내에서 동시 출현하는 빈도가 될 것이다.

​
3. Community Detection

> -  Louvain algorithm을 사용하며, 네트워크 내에서 밀도가 높은 커뮤니티를 식별하고 구조를 파악하여 서로 묶어서 분석하는 방법이다.


4. KoBERTopic
> -  BERT embeddings과 클래스 기반(class-based) C-TF-IDF를 활용하여 문서의 중요한 단어를 유지하면서, 쉽게 해석할 수 있는 조밀한 클러스터를 만드는 토픽 모델링
> -  선택이유:
>    -  대규모 텍스트 데이터로 사전에 학습된 모델을 사용하여 적은 양의 데이터로 효과적인 결과 추출 가능
>    -  텍스트 데이터의 특성에 따라 토픽 수를 유연하게 조절할 수 있어 다양한 데이터에 대한 적응성이 우수 - BERT 모델의 특성상 단어의 의미를 파악할 때 문맥을 고려

</br>

### 설치 패키지: 
- python 3

```
pip install selenium
pip install chromedriver-autoinstaller
pip install konlpy
pip install bertopic
pip install python-louvain
```

</br>

## II. 데이터 분석

### 1. 텍스트 전처리
적용 모델에 따라 추가로 진행한 부분이 있으나, 기본적인 전처리는 아래와 같이 진행되었음:
- URL 및 e-mail 형태의 문자열 제거   
- 연속된 공백을 하나로 줄임
- 특수문자 제거
- 불용어 처리

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/preprocess/text_preprocessing.py)

</br>

### 2. KoBERTopic
모델 구성:
```
model = BERTopic(
    embedding_model="sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens",  # 임베딩 모델 지정
    vectorizer_model=vectorizer,  # 벡터화 모델 지정
    nr_topics=10,  # 토픽 개수 지정
    min_topic_size=5,  # 최소 토픽 크기 지정
    top_n_words=10,  # 각 토픽당 상위 단어 개수 지정
    calculate_probabilities=True  # 확률 계산 설정
)
```
</br>

1차시도:
- 불용어 처리 전 1차 시도 결과
   - 토픽수: 10
   - 최소 토픽 크기: 5
> -  해석할 수 없는 결과 도출
> -  추가적인 불용어 처리 후 섬세한 결과를 기대

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/KoBERTopic/topic_modeling_ver1.py)

</br>

2차시도:
- 불용어 처리 처리 후 2차 시도 결과
   - 토픽 수: 10
   - 최소 토픽 크기: 5
> - 토픽의 수가 확 줄어 듦
> - 다른 방법론을 통해 질문지를 재구성할 필요성 대두
> - **SNA를 통한 토픽모델링화: 질문지 재구성** 

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/KoBERTopic/topic_modeling_ver2.py)

</br>

### 3. SNA(Social Network Analysis)

#### 추가적인 전처리:
   1. Konlpy를 이용한 명사 추출
   2. 추가적으로 필터링하지 못한 단어 제거

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/SNA/SNA_preprocessing.py)

</br>

#### 텍스트마이닝:

1. TF-IDF
- 각 문서 별 단어의 BOW 벡터 산출 후 TF-IDF 값을 계산
- 누적 TF-IDF 합이 5 이상인 단어들을 선정
- 선정된 단어들 안에서 추가적인 불용어 처리
> 총 334개의 단어가 주요 Topic 단어로 선정
> 각 단어를 SNA의 node로 사용

</br>

2. 동시출현빈도
- 각 단어들끼리의 동시출현빈도를 리스트로 저장
> 동시출현관계 : SAN의 Edge로 사용
> 동시출현빈도 : SNA의 가중치로 사용

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/SNA/SNA_textmining.py)

</br>


#### SNA info
```
노드의 개수 : 334
엣지의 개수 : 37137

Diamter : 2
Density : 0.66779
Transitivity : 0.75742 

Degree centrality (연결 중심성) :
[('출산', 1.0), ('회사', 0.99699), ('신청', 0.99699)]
Betweenness centrality (매개 중심성) :
[('출산', 0.00326), ('기간', 0.00323), ('1년', 0.00321)]
Closeness centrality (근접 중심성):
[('출산', 1.0), ('회사', 0.99700), ('신청', 0.99700)]
Eigenvector centrality :
[('출산', 0.07428), ('신청', 0.07420), ('회사', 0.07420)]
```

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/SNA/SNA_visualization.py)

</br>


#### Community Detection(Louvain algorithm)
```
# community_louvain
partition = cl.best_partition(G_data, random_state = 42, resolution=1.08)
```
> Resolution 값을 1.0에서 1.1 사이의 값으로 변경해가며 가장 해석에 용의한 1.08 값을 채택

[바로가기](https://github.com/eunnnholee/childcare-policy-KoBERTopic-SNA/blob/main/SNA/community_detection.py)

</br>
</br>


## III. 결론
총 16개 Cluster가 도출되었지만 Node의 개수가 매우 작은 경우, Cluster 해석에서 중요하지 않다고 판단하여 제외
> 4, 5, 7, 8, 9, 10, 12, 13, 15 Cluster 제외
```
Cluster0 : [권고사직, 계약직, 퇴직금, 사후지급금, 사업장, 대체인력]
Cluster1 : [계획, 출산예정일, 날짜계산, 휴가, 연차, 소진]
Cluster2 : [어린이집, 연장반, 맞벌이, 직장맘, 신랑, 단축근무]
Cluster3 : [33(3+3육아휴직), 12개월, 지급, 기준, 금액, 2022년]
Cluster6 : [급여, 신청, 휴직기간, 육아휴직수당, 소득, 1년]
Cluster11 : [공무원, 올해, 퇴사, 변경, 인터넷, 연차수당]
Cluster14 : [고용보험, 고용노동부, 제출, 서류, 고용센터, 조기복직]

```

</br>

질문지 정리:
1. Cluster0 [권고사직, 계약직, 퇴직금, 사후지급금, 사업장, 대체인력]
> 본인의 근로조건 상황에 따라, 충분한 육아휴직 지원을 활용하지 못할 경우, 기타 급여 처리에 관한 최적화 방안은 무엇일까?

2. Cluster1 [계획, 출산예정일, 날짜계산, 휴가, 연차, 소진]
> 출산 예정일 및 연차 소진 등을 고려하여 육아휴직을 어떻게 스케쥴링하는 것이 좋을까요?(출잔전후휴가, 산전(후)육아휴직 등)

3. Cluster2 [어린이집, 연장반, 맞벌이, 직장맘, 신랑, 단축근무]
> 맞벌이 중인 육아휴직을 고려하는 직장맘의 입장에서, 어린이집에서의 연장반 이용 유지를 위한 방법이 있을까?

4. Cluster3 [33(3+3육아휴직), 12개월, 지급, 기준, 금액, 2022년]
> 3+3 부모육아휴직제의 내용과 혜택은 어떻게 진행될까?

5. Cluster6 [급여, 신청, 휴직기간, 육아휴직수당, 소득, 1년]
> 육아휴직 급여 신청방법 및 신청기간에 대해 궁금해요!

6. Cluster11 [공무원, 올해, 퇴사, 변경, 인터넷, 연차수당]
> 일반근로자와 달리 공무원들의 육아휴직 신청 조건 및 법 조항이 다른가요?

7. Cluster14 [고용보험, 고용노동부, 제출, 서류, 고용센터, 조기복직]
> 육아휴직 신청 관련해서 필요한 서류와 급여지급은 어디에서 이뤄질까요?

[바로가기]()

</br>

기대효과: 
> - 육아휴직과 관련해 부모들이 공통적으로 갖고 있는 대표적인 질문을 정부 차원에서 수집 및 활용할 수 있다.
> - 수집한 질문들을 바탕으로 정부는 국민들에게 관심사가 되는 문제들을 통합적으로 제공함으로써, 정보의 비대칭을 줄일 수 있다.
> - 정부가 정책을 신규 수립 및 변경할 때, 국민들에게 정보를 어떻게 전달해야 할 지 가이드라인을 제시할 수 있다.

</br>

한계:
> -  텍스트 마이닝을 진행 했음에도 TF-IDF는 단어의 빈도를 기반으로 하기 때문에, 단어가 출현하는 빈도에만 주목하고 문맥을 고려하지 않았다.
> -  따라서 문서의 전반적인 의미나 문맥을 파악하는 데에는 한계가 있을 수 있어 명사가 아니거나 사용할 수 없는 단어들이 존재하였다. 이런 단어들을 일일이 제거하는 시도를 거쳤으나, 추가적인 정제 작업 또는 딥러닝 모델 구축을 통해 개선된 결과를 도출할 수 있을 것이다.
> -  긴 문서는 짧은 문서에 비해 많은 단어를 포함할 수 있어 해당 문서의 TF-IDF 점수가 높아지는 경향이 있다. 따라서 문서의 길이에 따라 TF-IDF 점수가 편향될 수 있다.

</br>

Reference:
1. 텍스트마이닝 방법을 이용한 간편결제 서비스 이용자의 질문분석
> 위 논문에서는 텍스트마이닝을 이용해 소비자들이 간편결제서비스를 이용하면서 가장 많이 묻는 질문을 분석했으며, 그 질문에 한해 관심도를 파악했다. 하지만 본 연구는 문서 별로 자주 나온 단어를 clustering 하여 질문을 재구성하는데 초점을 맞추었다.

​

2. 소셜 네트워크 분석을 통한 국민의 관광에 대한 인식 변화 연구
> 관광에 대한 인식을 파악하고자 빈도수가 잦은 단어를 하나의 클러스터로 묶어 해석을 용이하게 했다. 따라서 본 연구에서도 해당 논문의 방법론을 벤치마킹하여 단어들 사이의 연관성을 파악하기 위해서 클러스터링을 진행했다.

​

3. AI 챗봇을 활용한 정부 및 지자체의 해택, 복지, 소식 정보 제공 및 추천 서비스에 대한 연구 
> 위 논문에서는 다양한 플랫폼을 활용해 정보 및 지자체 혜택 및 정보 추천 서비스를 제공하는 챗봇을 구현했다. 이 논문을 바탕으로 빈도수 기반의 재구성된 질문을 사전에 역제시하면서 효율적으로 정보를 제공하는 아이디어를 얻었다.


4. [KoBERTopic 모델 GitHub 소스 코드 활용](https://github.com/ukairia777/KoBERTopic)





