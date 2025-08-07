import subprocess

def configure_accelerate():
    print("⚙️ Configuring Accelerate...")
    subprocess.run(["accelerate", "config", "default"])


def train_model():
    print("🚀 Continuing training from last checkpoint...")
    subprocess.run([
        "accelerate", "launch",
        "examples/text_to_image/train_text_to_image_lora.py",
        "--dataset_name=logo-wizard/modern-logo-dataset",
        "--pretrained_model_name_or_path=stabilityai/stable-diffusion-2-1-base",
        "--resolution=512",
        "--train_batch_size=1",
        "--gradient_accumulation_steps=1",
        "--learning_rate=1e-4",
        "--lr_scheduler=constant",
        "--lr_warmup_steps=0",
        "--max_train_steps=95000",   # ⏫ increase total steps
        "--output_dir=./logo-lora-model",
        "--resume_from_checkpoint=latest",  # ✅ resume from last checkpoint
        "--checkpointing_steps=2000",
        "--validation_prompt= a logo of cafe restaurant bar with a circle with an ornament on the sides, tableware above and two leaves on top and bottom, lightcyan background, midnightblue, midnightblue foreground, minimalism, modern",
        "--validation_epochs=1",
        "--report_to=tensorboard",
        "--mixed_precision=fp16",
        "--caption_column=text",
        "--image_column=image"
    ])
    print("✅ Continued training complete.")

#  logo of a herbal store, clay pot and leaf, vector art, green and brown"
# minimal vector logo of a flower shop with pink tulip in a pot, modern flat design"
