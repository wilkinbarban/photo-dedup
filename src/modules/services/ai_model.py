import logging

import numpy as np
from PIL import Image


class PhotoAIAnalyzer:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        logging.info("Initializing AI model (MobileNetV2)...")
        import torch
        import torchvision.models as models
        import torchvision.transforms as transforms

        self._torch = torch
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        self.model.classifier = torch.nn.Identity()
        self.model.eval()
        self.model.to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def get_embedding(self, img_path: str):
        try:
            with Image.open(img_path) as img:
                img_rgb = img.convert('RGB')
                tensor = self.transform(img_rgb).unsqueeze(0).to(self.device)
                with self._torch.no_grad():
                    embedding = self.model(tensor)
                emb_array = embedding.cpu().numpy().flatten()
                return emb_array
        except Exception as error:
            logging.error(f"Error computing embedding for {img_path}: {error}")
            return None

    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Returns similarity score between 0.0 and 1.0 using cosine similarity."""
        if emb1 is None or emb2 is None:
            return 0.0
        try:
            dot = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            if norm1 == 0 or norm2 == 0:
                return 0.0
            cos_sim = dot / (norm1 * norm2)
            return max(0.0, min(1.0, (cos_sim + 1.0) / 2.0))
        except Exception:
            return 0.0
