from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split  # train/valid 분리를 위해 추가

# 1. 데이터 로드 (CSV에서 pandas DataFrame으로 읽어옴)
df = pd.read_csv("my_custom_dataset.csv")    # CSV 파일에 'text', 'label' 컬럼이 있어야 함

# 2. 라벨을 숫자로 매핑 (문자 → 숫자)
label2id = {
    "영향 없음": 0,
    "치명적 영향": 1,
    "경고 (일부 영향)": 2,
    "알수없음": 3
}
df["label"] = df["label"].map(label2id)

# 3. train/validation 데이터 분리 (실무에서는 반드시 필요!)
train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

# 4. pandas DataFrame을 Hugging Face Dataset 객체로 변환
train_dataset = Dataset.from_pandas(train_df)
valid_dataset = Dataset.from_pandas(valid_df)

# 5. DistilBERT 토크나이저(문장을 토큰ID로 변환해주는 도구)와 분류용 사전학습 모델 준비
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
# num_labels는 클래스(라벨) 개수와 반드시 일치해야 함!
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)

# 6. 전처리 함수: 입력 데이터셋을 DistilBERT가 이해할 수 있게 토크나이즈
def preprocess(examples):
    return tokenizer(
        examples["text"],
        truncation=True,              # 최대 길이보다 긴 문장은 자름
        padding="max_length",         # 짧은 문장은 max_length까지 0-padding
        max_length=64                 # 토큰 최대 길이 (실제 데이터에 따라 조정)
    )

# 7. map 함수를 이용해 전체 데이터셋을 토크나이즈 (배치로 빠르게 처리)
train_encoded = train_dataset.map(preprocess, batched=True)
valid_encoded = valid_dataset.map(preprocess, batched=True)

# 8. Trainer의 학습 설정 정의
args = TrainingArguments(
    output_dir="./my_distilbert_model",   # 모델, 로그 저장 경로
    evaluation_strategy="epoch",          # 에폭마다 검증(validation) 수행
    num_train_epochs=3,                   # 학습 에폭 수
    per_device_train_batch_size=8,        # 장치별 배치 사이즈 (GPU/CPU 한 대 기준)
    save_strategy="epoch"                 # 에폭마다 모델 저장
)

# 9. Trainer 객체 생성 (학습, 평가 자동화)
trainer = Trainer(
    model=model,                    # 학습할 모델
    args=args,                      # 학습 파라미터(TrainingArguments)
    train_dataset=train_encoded,    # 학습 데이터셋
    eval_dataset=valid_encoded,     # 검증 데이터셋
)

# 10. 학습 실행 (파인튜닝 시작)
trainer.train()

# 11. 학습이 끝난 모델과 토크나이저를 디스크에 저장 (서빙/재학습 등에 활용)
model.save_pretrained("./my_distilbert")
tokenizer.save_pretrained("./my_distilbert")
