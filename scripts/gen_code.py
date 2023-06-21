#!/usr/bin/env python
# Run: python gen_code.py "is_palindrome"
from dotenv import load_dotenv

load_dotenv()
import os

import json
import pprint as pp
from pprint import PrettyPrinter, pprint, pformat

pprint = pp.PrettyPrinter(sort_dicts=False).pprint
pformat = pp.PrettyPrinter(sort_dicts=False).pformat

from simpleaichat import AIChat
from uuid import uuid4
import re
import argparse
from typing import Any, Dict, List, Optional, Union

from rich.console import Console

console = Console()


def pretty_print(json_object):
    print(json.dumps(json_object, indent=2, sort_keys=False, default=pformat))


def console_print(
    *objects: Any, title=None, title_color="bold white", sep="\n\n", **kwargs: Any
) -> None:
    # obj is first objects
    # obj = objects[0]
    # if inspect.isclass(obj) else title
    title = f"{objects[0].__class__.__name__}:" if title is None else title
    title = f"[{title_color}]{title}[/{title_color}]" if title_color is not None else title
    console.print(title, *objects, sep="\n\n", **kwargs)


def print_ai(ai: AIChat, default=repr):
    for i, (key, val) in enumerate(zip(ai.sessions.keys(), ai.sessions.values())):
        console_print(val, title=f"{val.__repr_name__()} {i}: {default(key)}")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-3.5-turbo"  # in production, may want to use model="gpt-4" if have access
TEMPERATURE = 0.0

SYSTEM_PROMPT = """You are a Python code example.

Follow ALL the following rules:
- ONLY EVER RESPOND WITH CODE IN PYTHON MARKDOWN BLOCKS, AND NOTHING ELSE
- NEVER include code comments."""

PATTERN = r"```python\n|```$"


def extract_text(text):
    pattern = r"```python\n(.*?)\n```$"
    return re.search(pattern, text, re.DOTALL).group(1)

def extract_text_2(text):
    start_index = text.find("```python\n")
    end_index = text.find("```$", start_index)
    if start_index != -1 and end_index != -1:
        return text[start_index + 10:end_index]
    else:
        return None

def gen_code(
    query,
    api_key=OPENAI_API_KEY,
    model=MODEL,
    temperature=TEMPERATURE,
    debug=False,
):
    ai_func = AIChat(api_key=api_key, console=False)

    params = {"temperature": temperature, "stop": ["``` ", "```\n"]}

    id = uuid4()
    ai_func.new_session(api_key=api_key, id=id, system=SYSTEM_PROMPT, params=params, model=model)
    _ = ai_func(query, id=id)
    response_optimized = ai_func("Make it more efficient.", id=id)
    # print(f"ai_func:\n{ai_func}\n")
    if debug:
        print_ai(ai_func)
        console_print(response_optimized, title="response_optimized")
    # response_cleaned = re.sub(PATTERN, "", response_optimized).strip()
    response_cleaned = extract_text(response_optimized)
    if debug:
        console_print(response_cleaned, title="response_cleaned")

    ai_func.delete_session(id=id)
    return response_cleaned

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python code generator")
    parser.add_argument("query", help="Generate code from query")
    parser.add_argument(
        "--api_key", "--api", type=str, default=OPENAI_API_KEY, help="OpenAI API key"
    )
    parser.add_argument("--model", "-m", type=str, default=MODEL, help="OpenAI model")
    parser.add_argument("--temp", "-t", type=float, default=TEMPERATURE, help="Temperature")
    args = parser.parse_args()
    code = gen_code(args.query, api_key=args.api_key, model=args.model, temperature=args.temp)
    print(code)
