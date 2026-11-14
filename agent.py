"""ShopAgent: a shopping assistant where Gemini decides which tool to call.

Run:
    pip install google-genai
    $env:GEMINI_API_KEY="your-key"   
    python agent.py
"""

import functools
import os
import sys

from google import genai
from google.genai import types

import tools

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are a helpful assistant for an online electronics and footwear store.
Rules:
- For anything about products, stock, prices or orders, call a tool. Never guess or invent data.
- Only call start_return when the customer clearly asks to return an order and has given a reason.
  If you don't have the order id or the reason, ask for it first.
- If a tool returns an error, explain it politely in plain words and suggest what the customer can do.
- Prices are in rupees. Keep answers short and friendly."""


def logged(fn):
    """Wrap a tool so every call is printed. Keeps the name, docstring and type
    hints, which Gemini reads to decide how to use the tool."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"  [tool call]   {fn.__name__}({kwargs if kwargs else args})")
        result = fn(*args, **kwargs)
        print(f"  [tool result] {result}")
        return result
    return wrapper


TOOLS = [logged(f) for f in (
    tools.search_products,
    tools.check_inventory,
    tools.get_order_status,
    tools.start_return,
)]


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Set the GEMINI_API_KEY environment variable first.")

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=TOOLS)
    chat = client.chats.create(model=MODEL, config=config)

    print("ShopAgent ready. Try: 'Where is order O1001?'  Type 'quit' to exit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("quit", "exit", "q"):
            break
        if not user:
            continue
        try:
            response = chat.send_message(user)
            print(f"Agent: {response.text}\n")
        except Exception as exc:  # network or API problem
            print(f"Error talking to Gemini: {exc}\n")


if __name__ == "__main__":
    main()