import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#pip install scikit-surprise pandas numpy scikit-learn
# 사용자-아이템 상호작용 데이터
interaction_data = {
    'user_id': [1, 2, 3, 1, 2, 3, 4],
    'item_id': [1, 2, 3, 2, 3, 4, 5],
    'rating': [5, 4, 5, 4, 5, 3, 2]  #평점은 구매여부, 조회수 등으로 변환할 수 있다.
}

interaction_df = pd.DataFrame(interaction_data)

# 아이템 콘텐츠 데이터
content_data = {
    'item_id': [1, 2, 3, 4, 5],
    'feature_1': [1, 1, 0, 0, 1],
    'feature_2': [0, 1, 1, 1, 0]
}

content_df = pd.DataFrame(content_data)

# Surprise 데이터셋 생성
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(interaction_df[['user_id', 'item_id', 'rating']], reader)


# 학습 데이터와 테스트 데이터로 분리
trainset, testset = train_test_split(data, test_size=0.2)

# SVD 모델 생성 및 훈련
#model = SVD(random_state=42)
model = SVD() 
model.fit(trainset)

# 아이템 특징 행렬 생성 및 코사인 유사도 계산
item_features = content_df.drop(columns=['item_id']).values
item_similarity = cosine_similarity(item_features)

# 특정 아이템과 유사한 상위 N개의 아이템을 추천하는 함수
def content_based_recommend(item_id, item_similarity, top_n=3):
    item_index = content_df[content_df['item_id'] == item_id].index[0]
    similarity_scores = list(enumerate(item_similarity[item_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_items = [content_df.iloc[i[0]]['item_id'] for i in similarity_scores[1:top_n+1]]
    return top_items

# 특정 사용자에 대한 협업 필터링 추천 생성 함수
def collaborative_recommend(user_id, model, item_ids, top_n=3):
    predictions = [model.predict(user_id, iid) for iid in item_ids]
    predictions.sort(key=lambda x: x.est, reverse=True)
    top_items = [pred.iid for pred in predictions[:top_n]]
    return top_items

# 특정 사용자에 대한 하이브리드 추천 생성 함수
def hybrid_recommend(user_id, model, item_ids, item_similarity, top_n=3):
    collab_recommendations = collaborative_recommend(user_id, model, item_ids, top_n)
    hybrid_recommendations = []

    for item in collab_recommendations:
        content_recommendations = content_based_recommend(item, item_similarity, top_n=1)
        hybrid_recommendations.extend(content_recommendations)

    hybrid_recommendations = list(set(hybrid_recommendations))  # 중복 제거
    return hybrid_recommendations[:top_n]



# 사용자 ID 2에 대한 협업 필터링 추천
user_id = 2
item_ids = content_df['item_id'].tolist()
collaborative_recommendations = collaborative_recommend(user_id, model, item_ids)
print("협업 필터링 추천 (user_id={}):".format(user_id), collaborative_recommendations)

# 특정 아이템에 대한 콘텐츠 기반 추천 (여기서는 협업 필터링 추천 결과의 첫 번째 아이템을 사용)#ex)[3,?,?] 중 첫번째 3번아이템사용
if collaborative_recommendations:
    item_id = collaborative_recommendations[0]
    content_based_recommendations = content_based_recommend(item_id, item_similarity)
    print("콘텐츠 기반 추천 (item_id={}):".format(item_id), content_based_recommendations)


# 예시: 사용자 ID 2에 대한 하이브리드 추천
user_id = 2
item_ids = content_df['item_id'].tolist()
print("하이브리드 추천 (user_id={}):".format(user_id), hybrid_recommend(user_id, model, item_ids, item_similarity))