import numpy as np
from  PIL  import  Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration
import torch


def vqa(image_path):
    pil_image = Image.open(image_path).convert('RGB')
    question = 'List the individual objects/items that you see. Separate them individually with commas.'

    processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    prompt = f"Question: {question} Answer:" 

    inputs = processor(pil_image, text=prompt, return_tensors="pt").to(device, torch.float16)

    generated_ids = model.generate(**inputs, max_new_tokens=10)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    
    exclude_words = ['a', 'and']
    objects = [word for word in generated_text.replace(',','').split() if word.lower() not in exclude_words]

    print(objects)

    return objects


