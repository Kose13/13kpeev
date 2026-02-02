# Plovdiv Image Prompt

Use the following prompt with your preferred image-generation model to create a
photorealistic scene of Plovdiv at golden hour.

```
A photorealistic view of Plovdiv, Bulgaria at golden hour, featuring the Ancient Roman Theatre, warm stone textures, and a clear sky. Wide-angle, high detail, 8k.
```

## Generate via Python (OpenAI Images API)

1) Install the SDK:

```bash
pip install openai
```

2) Create a script (for example, `generate_plovdiv.py`) and run it:

```python
from openai import OpenAI
import base64

client = OpenAI()

prompt = (
    "A photorealistic view of Plovdiv, Bulgaria at golden hour, "
    "featuring the Ancient Roman Theatre, warm stone textures, "
    "and a clear sky. Wide-angle, high detail, 8k."
)

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1024",
)

image_base64 = result.data[0].b64_json
with open("plovdiv.png", "wb") as file:
    file.write(base64.b64decode(image_base64))
```

## Generate via Python (Stable Diffusion + diffusers)

1) Install dependencies (GPU recommended):

```bash
pip install diffusers transformers accelerate torch
```

2) Create a script (for example, `generate_plovdiv_sd.py`) and run it:

```python
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
```
