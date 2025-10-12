import datetime
import re
import random
import os
import argparse
from dotenv import load_dotenv

from multi_generator import MultiModelGenerator

load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument("--quote_length", choices=["short", "medium", "long"], default=None,
                    help="Control how long the generated quotes can be")
args = parser.parse_args()


QUOTE_LENGTH = args.quote_length or os.getenv("QUOTE_LENGTH", "medium")

THEMES = [
    "motivational quote about perseverance and success",
    "short, witty programming quote with a touch of humor",
    "inspirational quote about learning and curiosity",
    "quote about creativity and innovation",
    "tech-related quote that sounds like wisdom from a senior engineer",
    "philosophical quote about the future of AI and humanity",
]


def generate_quote(length: str = "medium") -> str:
    theme_index = random.randint(0, len(THEMES) - 1)
    theme_values = THEMES[theme_index]

    
    if length == "short":
        word_limit = 10
    elif length == "medium":
        word_limit = 25
    else:  # long
        word_limit = 50

    prompt = f"Generate a unique, original {theme_values}. Keep it under {word_limit} words."
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
    quote = generate_quote(QUOTE_LENGTH)

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
