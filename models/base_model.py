# models/base_model.py
from abc import ABC, abstractmethod
import torch
import logging
from typing import Tuple, Optional
from PIL import Image

logger = logging.getLogger(__name__)

class BaseVisionModel(ABC):
    def __init__(self):
        logger.info("Initializing vision model...")
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        logger.info(f"Using device: {self.device} with dtype: {self.torch_dtype}")
        self._setup_model()

    @abstractmethod
    def _setup_model(self) -> None:
        pass

    @abstractmethod
    def analyze_image(self, image_path: str, quality: str = "standard") -> Tuple[str, Optional[str]]:
        """
        Analyze an image using the model.
        
        Args:
            image_path (str): Path to the image file
            quality (str): Quality level - "standard", "detailed", or "creative"
            
        Returns:
            Tuple[str, Optional[str]]: (description, clean_caption)
        """
        raise NotImplementedError("Subclasses must implement analyze_image")

    def clean_output(self, text: str) -> str:
        """Clean model output by removing special tokens and formatting."""
        import re
        try:
            text = text.replace('</s>', '').replace('<s>', '')
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'<loc_\d+>', '', text)
            text = ' '.join(text.split())
            text = re.sub(r'http\S+', '', text)
            return text.strip()
        except Exception as e:
            logger.error(f"Error cleaning output text: {str(e)}")
            return text  # Return original text if cleaning fails