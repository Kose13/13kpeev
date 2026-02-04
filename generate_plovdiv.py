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
