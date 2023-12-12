from transformers import OwlViTProcessor, OwlViTForObjectDetection
import tarfile
import torch

processor = None
model = None

def load_model():
    global processor
    global model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = OwlViTProcessor.from_pretrained("google/owlvit-large-patch14")
    model = OwlViTForObjectDetection.from_pretrained("google/owlvit-large-patch14").to(device)

def get_model():
    return model

def get_processor():
    return processor
