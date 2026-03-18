from typing import Optional


class ModelService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def load(self) -> None:
        # STEP2-0: 모델 로딩 비활성화 (크레딧/모델 준비 전까지)
        print("[STEP2] ML model loading skipped")
        self.model = None
        return

        # === 나중에 복구용 ===
        # import os, pickle
        # if not os.path.exists(self.model_path):
        #     self.model = None
        #     return
        #
        # with open(self.model_path, "rb") as f:
        #     self.model = pickle.load(f)

    def predict(self, price: int, views: int, sales: int) -> Optional[float]:
        if self.model is None:
            return None
        # return float(self.model.predict([[price, views, sales]])[0])
        return None
