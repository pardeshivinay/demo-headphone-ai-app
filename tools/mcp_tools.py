from langchain.tools import tool

# In-memory session state (simulates a user session)
_cart: list[dict] = []
_discount_codes = {
    "SAVE10": 10,
    "BUDGET20": 20,
    "FIRST15": 15,
}


@tool
def add_to_cart(product_name: str) -> str:
    """Add a headphone product to the shopping cart by product name."""
    _cart.append({"product": product_name})
    cart_list = ", ".join([item["product"] for item in _cart])
    return f"✅ '{product_name}' has been added to your cart. Cart now contains: {cart_list}."


@tool
def apply_discount(discount_code: str) -> str:
    """Apply a discount code to the current cart. Valid codes: SAVE10, BUDGET20, FIRST15."""
    code = discount_code.strip().upper()
    if code in _discount_codes:
        pct = _discount_codes[code]
        return f"✅ Discount code '{code}' applied! You get {pct}% off your order."
    else:
        valid = ", ".join(_discount_codes.keys())
        return f"❌ '{discount_code}' is not a valid code. Valid codes are: {valid}."


@tool
def check_stock(product_name: str) -> str:
    """Check stock availability for a headphone product by name."""
    import pandas as pd
    import os

    csv_path = os.path.join(os.path.dirname(__file__), "../data/headphones.csv")
    df = pd.read_csv(csv_path)

    match = df[df["name"].str.lower().str.contains(product_name.lower())]

    if match.empty:
        return f"❌ Could not find a product matching '{product_name}'. Try using the exact product name."

    row = match.iloc[0]
    stock = int(row["stock"])
    name = row["name"]

    if stock > 20:
        return f"✅ '{name}' is well stocked — {stock} units available. Ready to ship."
    elif stock > 0:
        return f"⚠️ '{name}' is low on stock — only {stock} units left. Order soon!"
    else:
        return f"❌ '{name}' is currently out of stock."


def get_tools():
    return [add_to_cart, apply_discount, check_stock]
