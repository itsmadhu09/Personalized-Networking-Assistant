"""
topic_generator.py
--------------------
GPT-2 text-generation helper: turns extracted themes + user interests into
clean, numbered conversation starters. Raw GPT-2 output is noisy, so this
module wraps generation with prompt templating and post-processing.
"""

import os
import re
from functools import lru_cache
from transformers import pipeline

MODEL_NAME = os.getenv("GPT2_MODEL", "gpt2")


@lru_cache(maxsize=1)
def _get_generator():
    return pipeline("text-generation", model=MODEL_NAME)


def _build_prompt(themes: list[str], interests: list[str]) -> str:
    theme_str = ", ".join(themes) if themes else "the event"
    interest_str = ", ".join(interests) if interests else "networking"
    return (
        f"Here are engaging conversation starters about {theme_str} "
        f"for someone interested in {interest_str}:\n1."
    )


def _clean_starters(raw_text: str, prompt: str, n: int) -> list[str]:
    """
    Strip the echoed prompt, then split on numbered-list markers
    (1. 2. 3. ...) to get individual starters. Falls back to sentence
    splitting if the model didn't produce numbering.
    """
    text = raw_text[len(prompt):] if raw_text.startswith(prompt) else raw_text
    text = "1." + text  # re-attach the "1." that was part of the prompt

    chunks = re.split(r"\n?\d+\.\s*", text)
    chunks = [c.strip().replace("\n", " ") for c in chunks if c.strip()]

    if not chunks:
        chunks = [s.strip() for s in text.split(".") if s.strip()]

    return chunks[:n] if chunks else ["Could not generate a starter — try rephrasing the event description."]


def generate_starters(themes: list[str], interests: list[str], n: int = 3) -> list[str]:
    generator = _get_generator()
    prompt = _build_prompt(themes, interests)

    outputs = generator(
        prompt,
        max_new_tokens=80,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.85,
        top_p=0.92,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    raw_text = outputs[0]["generated_text"]
    return _clean_starters(raw_text, prompt, n)
