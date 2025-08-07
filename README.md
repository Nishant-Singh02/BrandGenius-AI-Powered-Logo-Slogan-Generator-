# BrandGenius – AI-Powered Logo & Slogan Generator

BrandGenius is an AI-based web app that empowers startups to instantly generate brand identities through custom logos and slogans.

<img width="1811" height="854" alt="image" src="https://github.com/user-attachments/assets/47248aba-37e2-4843-9fd6-d113fd4abdf6" />
<img width="1667" height="861" alt="image" src="https://github.com/user-attachments/assets/170d6a31-b3b3-447f-849e-8c1626afa5af" />
<img width="1618" height="834" alt="image" src="https://github.com/user-attachments/assets/2ef9120a-3cf8-4bd3-b4cf-b968369c4aa6" />



## ✨ Features
- 🔧 Fine-tuned **Stable Diffusion** (LoRA-based) on 94K modern logo samples to generate high-quality, style-consistent vector logos.
- 🧠 Fine-tuned **Google FLAN-T5** using HuggingFace’s `Seq2SeqTrainer` for generating contextual, brand-relevant slogans.
- 🌐 Built a full-stack web app using **Flask, HTML, CSS, and JavaScript** for real-time generation.
- 🎯 End-to-end AI branding solution with live preview and download options.

## 🚀 Tech Stack
- Python, Flask
- HuggingFace Transformers
- Diffusers (Stable Diffusion + LoRA)
- HTML, CSS, JavaScript

## 📂 Directory Overview
- `app.py`: Backend Flask app.
- `slogan_model/`: Pre-trained FLAN-T5 model for slogan generation.
- `logo_model/`: LoRA fine-tuned Stable Diffusion model for logo generation.
- `static/` and `templates/`: Frontend files.

## 🛠 Installation
```bash
git clone https://github.com/yourusername/BrandGenius.git
cd BrandGenius
pip install -r requirements.txt
python app.py
