"""
analyze_outfit.py — Women's Fashion Critique Engine
Uses Qwen2.5-VL to analyze women's outfits with style persona detection.
"""

import os
import re
import gc
import torch
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from langchain.tools import tool

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# -------------------------------------------------------
# Model Setup
# -------------------------------------------------------
model_id = "Qwen/Qwen2.5-VL-3B-Instruct"

processor = AutoProcessor.from_pretrained(
    model_id,
    min_pixels=256*28*28,
    max_pixels=512*28*28
)

model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    device_map="cpu"
)

IMAGE_DIR = "Images"

# -------------------------------------------------------
# Women's Fashion Prompt (with Style Persona)
# -------------------------------------------------------
FASHION_PROMPT = (
    "You are a top women's fashion critic for Vogue and Harper's Bazaar. "
    "Your job is to analyze this women's outfit with sharp precision and brutal honesty.\n\n"

    "Consider these style personas when analyzing:\n"
    "- Gen-Z: Y2K revival, oversized, streetwear, cargo pants, chunky shoes, "
    "corsets, bold graphics, platform boots, low-rise jeans, crop tops\n"
    "- Millennial: minimalist, tailored, smart casual, silk blouses, neutral tones, "
    "structured bags, pointed flats, midi skirts, capsule wardrobe pieces\n"
    "- Aesthetic: cottagecore, dark academia, soft girl, lace, floral, "
    "vintage details, velvet, prairie dresses, Mary Janes, romantic silhouettes\n\n"

    "Follow this EXACT format — do not deviate:\n"
    "Style: [Describe the outfit in detail — silhouette, fabrics, colors, "
    "occasion suitability. Call out strengths and weaknesses with no filter]\n"
    "Rating: [Score out of 100 — average is 45. Weak fits: 20-45. "
    "Good fits: 46-70. Only elite looks break 80]\n"
    "Comment: [One savage but stylish one-liner — roast it if it deserves it, "
    "or give reluctant praise if it's genuinely good. No fluff, no mercy]\n"
    "Persona: [Classify as EXACTLY ONE word: Gen-Z, Millennial, or Aesthetic]"
)

# -------------------------------------------------------
# Utility Functions
# -------------------------------------------------------

def get_image(image_name: str) -> Image.Image:
    """Load image from Images/ folder."""
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return Image.open(image_path).convert("RGB")


def extract_rating(text: str):
    """Parse numeric rating from model output."""
    match = re.search(r'Rating:\s*(\d+)/100', text)
    if match:
        return int(match.group(1)) / 100.0
    return None


def extract_style_paragraph(text: str):
    """Extract Style section from model output."""
    match = re.search(
        r'Style:\s*(.*?)(?=\s*(Rating:|Comment:|Persona:|$))',
        text, re.DOTALL
    )
    if match:
        return match.group(1).strip()
    return None


def extract_comment(text: str):
    """Extract Comment section from model output."""
    match = re.search(r'Comment:\s*(.*?)(?=\s*(Persona:|$))', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_persona(text: str):
    """Extract style persona from model output."""
    match = re.search(r'Persona:\s*(Gen-Z|Millennial|Aesthetic)', text, re.IGNORECASE)
    if match:
        raw = match.group(1).strip()
        # Normalize
        if raw.lower() == "gen-z":
            return "Gen-Z"
        elif raw.lower() == "millennial":
            return "Millennial"
        elif raw.lower() == "aesthetic":
            return "Aesthetic"
    return "Millennial"  # default fallback


# -------------------------------------------------------
# Core Outfit Analyzer
# -------------------------------------------------------

def analyze_outfit(image_name: str) -> str:
    """
    Run Qwen2.5-VL on a women's outfit image.
    Returns structured critique with Style, Rating, Comment, Persona.
    """
    gc.collect()
    torch.cuda.empty_cache()

    print(f"[DEBUG] Analyzing: {image_name}")
    img = get_image(image_name)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": img},
                {"type": "text", "text": FASHION_PROMPT},
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[img],
        padding=True,
        return_tensors="pt"
    ).to("cpu")

    print("[DEBUG] Running inference...")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.2,
        do_sample=True,
        eos_token_id=processor.tokenizer.eos_token_id
    )

    generated_ids_trimmed = [
        out[len(inp):]
        for inp, out in zip(inputs.input_ids, outputs)
    ]
    result = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True
    )

    print("[DEBUG] Done!")
    return result[0]


# -------------------------------------------------------
# LangChain Tool
# -------------------------------------------------------

@tool
def analyze_outfit_tool(image_name: str) -> str:
    """
    LangChain tool for women's outfit analysis.
    Input: image filename in Images/
    Output: Style, Rating, Comment, Persona
    """
    return analyze_outfit(image_name)
