from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
import torch
import os
from PIL import Image

def run_inference():
    print("🧠 Loading model...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base",
        torch_dtype=torch.float16
    ).to("cuda")

    # 🛠️ Use specific checkpoint
    adapter_path = "./logo-lora-model/checkpoint-94000"
    if os.path.exists(os.path.join(adapter_path, "pytorch_lora_weights.safetensors")):
        pipe.load_lora_weights(adapter_path, weight_name="pytorch_lora_weights.safetensors")
        print(f"✅ LoRA adapter loaded from {adapter_path}")
    else:
        print("⚠️ LoRA adapter not found. Running base model.")


    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    prompt = "a logo of flower store red rose two daffodils are located in the center in a light brown outline pattern,pink background, foreground, minimalism, modern"
    negative_prompt = "text, photo, blurry, watermark, realistic"

    print("🎨 Generating 3 images...")
    images = []
    for i in range(3):
        img = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            height=768,
            width=768
        ).images[0]
        images.append(img)

    # 🧱 Combine images side by side
    combined = Image.new("RGB", (768 * 3, 768))
    for i, img in enumerate(images):
        combined.paste(img, (i * 768, 0))

    combined.save("generated_logo_grid.png")
    print("✅ Image grid saved as generated_logo_grid.png")
