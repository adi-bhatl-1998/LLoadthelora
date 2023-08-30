import logging
from pathlib import Path
import math

import matplotlib.pyplot as plt
import torch
from diffusers import StableDiffusionPipeline
from fastcore.all import concat
from huggingface_hub import notebook_login
from PIL import Image

logging.disable(logging.WARNING)
model_id="CompVis/stable-diffusion-v1-4"
def generate(prompts, num_inference_steps,guidance_scale,negative_prompt,model_id ,total_nm_img_prompt,seed ):
    pipe = StableDiffusionPipeline.from_pretrained(model_id, revision="fp16", torch_dtype=torch.float16).to("cuda")
    pipe.enable_attention_slicing()
    torch.manual_seed(seed)
    total_nm_img_prompt=5
    prompts = [prompts] * total_nm_img_prompt
    negative_prompt=["blue"]*total_nm_img_prompt
    image=pipe(prompts, num_inference_steps=num_inference_steps , guidance_scale=4,negative_prompt=negative_prompt).images
    num_rows=math.ceil(total_nm_img_prompt/3)

def image_grid(imgs, rows, cols):
    w,h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    for i, img in enumerate(imgs): grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid