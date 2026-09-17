import torch
from diffusers import StableDiffusionPipeline

prompt = (
    "A photorealistic view of Plovdiv, Bulgaria at golden hour, "
    "featuring the Ancient Roman Theatre, warm stone textures, "
    "and a clear sky. Wide-angle, high detail, 8k."
)

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
image.save("plovdiv.png")
