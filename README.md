# Plovdiv Image Prompt

Use the following prompt with your preferred image-generation model to create a
photorealistic scene of Plovdiv at golden hour.

```
A photorealistic view of Plovdiv, Bulgaria at golden hour, featuring the Ancient Roman Theatre, warm stone textures, and a clear sky. Wide-angle, high detail, 8k.
```

## Generate via Python (OpenAI Images API)

Example script: [`generate_plovdiv.py`](generate_plovdiv.py)

1) Install the SDK:

```bash
pip install openai
```

2) Run the script:

```bash
python generate_plovdiv.py
```

## Generate via Python (Stable Diffusion + diffusers)

Example script: [`generate_plovdiv_sd.py`](generate_plovdiv_sd.py)

1) Install dependencies (GPU recommended):

```bash
pip install diffusers transformers accelerate torch
```

2) Run the script:

```bash
python generate_plovdiv_sd.py
```
