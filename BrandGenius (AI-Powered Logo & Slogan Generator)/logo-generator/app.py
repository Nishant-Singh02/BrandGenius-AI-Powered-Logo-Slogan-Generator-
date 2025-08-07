from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
import os

app = Flask(__name__)

# Initialize models (could be moved to a separate service for better performance)
def init_models():
    # Slogan generator
    slogan_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    slogan_model = AutoModelForSeq2SeqLM.from_pretrained("./slogan_model/checkpoint-final")
    
    # Logo generator
    logo_pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base",
        torch_dtype=torch.float16
    ).to("cuda")
    
    # Load LoRA weights if available
    adapter_path = "./logo_model/checkpoint-94000"
    weight_file = "pytorch_lora_weights.safetensors"
    if os.path.exists(os.path.join(adapter_path, weight_file)):
        logo_pipe.load_lora_weights(adapter_path, weight_name=weight_file)
        print(f"✅ LoRA fine-tuned weights loaded from: {os.path.join(adapter_path, weight_file)}")
    else:
        print("⚠️ LoRA weights not found. Using base model only.")

        
    logo_pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(logo_pipe.scheduler.config)
    
    return slogan_tokenizer, slogan_model, logo_pipe

slogan_tokenizer, slogan_model, logo_pipe = init_models()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = f"{data['prompt']} in {data['style']} style"


    
    # Generate slogans
    input_text = "Generate a slogan for: " + prompt
    inputs = slogan_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    
    slogan_outputs = slogan_model.generate(
        **inputs,
        max_length=32,
        num_return_sequences=3,
        do_sample=True,
        top_k=50,
        temperature=0.9
    )
    
    slogans = [slogan_tokenizer.decode(output, skip_special_tokens=True) 
               for output in slogan_outputs]
    
    # Generate logos
    negative_prompt = "low quality, worst quality, bad composition, extra digit, fewer digits, text, inscription, watermark, label, asymmetric"
    
    logo_images = []
    for _ in range(3):
        result = logo_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            height=512,
            width=512
        )
        img = result.images[0]
        
        # Convert to base64 for web display
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logo_images.append(img_str)
    
    return jsonify({
        'slogans': slogans,
        'logos': logo_images
    })

if __name__ == '__main__':
    app.run(debug=False, threaded=False)
