# prepare_data.py
import os
from datasets import load_dataset
from PIL import Image

def prepare_dataset():
    os.makedirs("data/images", exist_ok=True)
    os.makedirs("data/captions", exist_ok=True)

    print("📦 Downloading dataset...")
    dataset = load_dataset("logo-wizard/modern-logo-dataset", split="train")

    for i, sample in enumerate(dataset):
        img_path = f"data/images/logo_{i:05d}.png"
        cap_path = f"data/captions/logo_{i:05d}.txt"

        # ✅ Fix here: assign caption
        caption = sample["text"]
        sample["image"].save(img_path)

        with open(cap_path, "w", encoding="utf-8") as f:
            f.write(caption)

    print(f"✅ Saved {len(dataset)} image-caption pairs to ./data/")
