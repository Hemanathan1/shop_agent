![CI](https://github.com/Hemanathan1/shop_agent/actions/workflows/ci.yml/badge.svg)

# ShopAgent

A shopping assistant for an online electronics and footwear store. The user chats in plain English, and Gemini decides which tool to call: search products, check stock, look up an order, or start a return. Business rules are enforced in code, not in the prompt.

## How it works

```
User message -> Gemini (with 4 tools) -> picks a tool -> Python function runs -> result goes back to Gemini -> reply
```

| Tool | What it does |
|---|---|
| `search_products(query, max_price)` | Finds products by name, with an optional price limit |
| `check_inventory(product_id)` | Returns the stock count for a product |
| `get_order_status(order_id)` | Returns the status and expected arrival of an order |
| `start_return(order_id, reason)` | Starts a return, if the order is eligible |

The model reads each tool's name, type hints and docstring to decide when to use it.

## Rules enforced in code

`start_return` refuses a return when:

- the order id does not exist
- the order has not been delivered yet
- a return was already requested
- the 7-day return window has passed

The model cannot override these. It only explains the refusal politely. The system prompt also tells the agent to ask for the order id and reason before starting a return.

## Example session

```
You: Where is order O1001
  [tool call]   get_order_status({'order_id': 'O1001'})
Agent: Your order O1001 with a Wireless Mouse is shipped and is expected to arrive on 2026-11-16.

You: Do you have shoes under 3000?
  [tool call]   search_products({'query': 'shoes', 'max_price': 3000})
Agent: Yes, we have Running Shoes for 2999 rupees.

You: Return order O1003
Agent: What is the reason for returning order O1003?

You: Return order O1003, wrong size
  [tool call]   start_return({'order_id': 'O1003', 'reason': 'wrong size'})
  [tool result] {'error': 'Return window of 7 days has passed (delivered 25 days ago).'}
Agent: I'm sorry, but the return window of 7 days has passed for order O1003.
```

## Run it

Requires Python 3.10 or newer and a Gemini API key.

```
pip install google-genai
$env:GEMINI_API_KEY="your-key"     # PowerShell; never commit your key
python agent.py
```

## Tests

The tools are plain Python functions, so they are tested without calling the API.

```
pip install pytest
python -m pytest -v
```

11 tests cover search, stock, order status and every return rule. The tests fix today's date so the 7-day window is predictable.

## Project structure

```
agent.py        chat loop, system prompt, Gemini tool calling
tools.py        the four tools and their business rules
shop_data.py    mock products and orders
tests/          pytest tests for the tools
```

## Limitations and next steps

- Data is mock data in memory. A real version would use a database.
- The agent has no login, so any order id can be queried.
- Add tests that check which tool the agent picks for sample prompts.
- Add a `check_inventory` hint so stock questions return the exact count.

-----------------------------------------------------------------------
