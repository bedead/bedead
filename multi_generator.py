import os
from typing import Optional


def MultiModelGenerator(prompt: str) -> Optional[str]:
    """
    Tries to generate content using multiple models in sequence.
    Stops at first successful response.
    """

    # --- Google Generative AI ---
    if os.getenv("GEMINI_API_KEY"):
        try:
            from google import genai

            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            if hasattr(response, "text") and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[WARN] Google model failed: {e}")

    # --- Groq API ---
    elif os.getenv("GROQ_API_KEY"):
        try:
            from groq import Groq

            client = Groq(api_key=os.environ["GROQ_API_KEY"])
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
            )
            text = completion.choices[0].message.content
            if text:
                return text.strip()
        except Exception as e:
            print(f"[WARN] Groq model failed: {e}")

    else:
        print(f"[INFO] Skipping model generation: no API key found.")

    return None
