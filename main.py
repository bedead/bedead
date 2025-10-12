import datetime
import re
import random

from dotenv import load_dotenv

from multi_generator import MultiModelGenerator

load_dotenv()

THEMES = [
    "motivational quote about perseverance and success",
    "short, witty programming quote with a touch of humor",
    "inspirational quote about learning and curiosity",
    "quote about creativity and innovation",
    "tech-related quote that sounds like wisdom from a senior engineer",
    "philosophical quote about the future of AI and humanity",
]


def generate_quote() -> str:
    theme_index = random.randint(0, len(THEMES) - 1)
    theme_values = THEMES[theme_index]
    prompt = f"Generate a unique, original {theme_values}. Keep it under 25 words."
    quote = MultiModelGenerator(prompt)
    if quote:
        return quote

    # Fallback quote
    fallback_quotes = [
        "Keep pushing forward — every bug is a step to mastery.",
        "Code, break, learn, repeat.",
        "Simplicity is the ultimate sophistication.",
    ]
    return random.choice(fallback_quotes)


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
