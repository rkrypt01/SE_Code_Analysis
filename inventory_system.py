"""Inventory manager."""

import json
import logging
from datetime import datetime

stock = {}


def add_item(item: str, qty: int) -> None:
    """Add items."""
    if not isinstance(item, str) or not item:
        raise ValueError("item")
    if not isinstance(qty, int) or qty < 0:
        raise ValueError("qty")
    stock[item] = stock.get(item, 0) + qty
    logging.info("%s: Added %d of %s", datetime.now(), qty, item)


def remove_item(item: str, qty: int) -> None:
    """Remove items."""
    if not isinstance(item, str) or not item:
        raise ValueError("item")
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty")
    try:
        cur = stock[item]
    except KeyError:
        logging.warning("Remove missing item: %s", item)
        return
    if qty >= cur:
        del stock[item]
        logging.info("%s: Removed %s", datetime.now(), item)
    else:
        stock[item] = cur - qty
        logging.info("%s: Removed %d of %s", datetime.now(), qty, item)


def get_qty(item: str) -> int:
    """Get quantity."""
    if not isinstance(item, str) or not item:
        raise ValueError("item")
    return stock.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.warning("Missing file: %s", file)
        return
    except json.JSONDecodeError:
        logging.error("Bad JSON: %s", file)
        return
    if not isinstance(data, dict):
        logging.error("Bad format: %s", file)
        return
    stock.clear()
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, int):
            stock[k] = v
        else:
            logging.warning("Skip entry: %r:%r", k, v)
    logging.info("Loaded %d items from %s", len(stock), file)


def save_data(file: str = "inventory.json") -> None:
    """Save inventory."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock, f, ensure_ascii=False, indent=2)
    logging.info("Saved %d items to %s", len(stock), file)


def print_data() -> None:
    """Print inventory."""
    for n, q in stock.items():
        print(f"{n} -> {q}")


def check_low_items(threshold: int = 5):
    """Return low items."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold")
    return [n for n, q in stock.items() if q < threshold]


def main() -> None:
    """Run demo."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.info("Start")
    add_item("apple", 10)
    add_item("banana", 5)
    remove_item("apple", 3)
    save_data()
    load_data()
    print_data()
    logging.info("Done")


if __name__ == "__main__":
    main()
