from diffusers import DiffusionPipeline
import torch 
import os
import PIL.Image
from huggingface_hub import login

login(token="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")

pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("mps")


# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = "a photo of an astronaut with a pokemon on mars"

# First-time "warmup" pass if PyTorch version is 1.13 (see explanation above)
_ = pipe(prompt, num_inference_steps=1)

# Results match those from the CPU device after the warmup pass.
image = pipe(prompt).images[0]
image.save("output11.png")
lora_path="sayakpaul/sd-model-finetuned-lora-t4"
pipe.unet.load_attn_procs(lora_path)
image_1=pipe(prompt).images[0]
image_1.save("output_after_lora.png")

# Print the ASCII art to the terminal.
image.show()
image_1.show()
def mrge_lora_to_main(pipe,)