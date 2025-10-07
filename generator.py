import datetime
import re
import os
import random

from dotenv import load_dotenv

load_dotenv()

from google import genai

# Configure Google API
KEY = os.getenv("GEMINI_API_KEY")
# print("Using API key:", KEY)
client = genai.Client(api_key=KEY)

THEMES = [
    "motivational quote about perseverance and success",
    "short, witty programming quote with a touch of humor",
    "inspirational quote about learning and curiosity",
    "quote about creativity and innovation",
    "tech-related quote that sounds like wisdom from a senior engineer",
    "philosophical quote about the future of AI and humanity",
]


def generate_quote():
    theme_index = random.randint(0, len(THEMES) - 1)
    theme_values = THEMES[theme_index]
    prompt = f"Generate a unique, original {theme_values}. Keep it under 25 words."
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", contents=prompt
    )
    if response.text:
        return response.text.strip()


if __name__ == "__main__":
    today = datetime.date.today().strftime("%Y-%m-%d")
    quote = generate_quote()

    # Read current README.md
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace between markers
    new_section = f"##### 🌟 *{today}*\n\n###### {quote}"
    updated = re.sub(
        r"(<!-- QUOTE:START -->)(.*?)(<!-- QUOTE:END -->)",
        f"\\1\n{new_section}\n\\3",
        content,
        flags=re.DOTALL,
    )

    # Write back
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)
