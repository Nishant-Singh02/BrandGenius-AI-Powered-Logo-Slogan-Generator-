from datasets import Dataset, DatasetDict
from PIL import Image
import os

def load_local_data():
    image_dir = "data/images"
    caption_dir = "data/captions"

    data = []
    for fname in sorted(os.listdir(image_dir)):
        if fname.endswith(".png"):
            img_path = os.path.join(image_dir, fname)
            cap_path = os.path.join(caption_dir, fname.replace(".png", ".txt"))

            with open(cap_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()

            data.append({"image": img_path, "text": caption})

    return Dataset.from_list(data)

# Save as arrow or upload to Hugging Face
dataset = load_local_data()
dataset.save_to_disk("hf_local_logo_dataset")
