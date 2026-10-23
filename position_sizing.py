"""Shared, broker-independent position sizing for Equity and FnO."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PositionSize:
    mode: str
    quantity: int
    lots: int
    budget: float
    estimated_value: float
    unit_price: float


def calculate_position_size(
    *,
    mode: str,
    price: float,
    lot_size: int = 1,
    fixed_quantity: int = 0,
    fixed_amount: float = 0.0,
    capital: float = 0.0,
    capital_percent: float = 0.0,
    max_quantity: int = 0,
) -> PositionSize:
    """
    Calculate shares (Equity) or lots/contracts (FnO).

    FIXED_QUANTITY:
        fixed_quantity is shares when lot_size=1, or lots when lot_size>1.
    FIXED_AMOUNT:
        Budget is fixed_amount INR.
    CAPITAL_PERCENT:
        Budget is capital * capital_percent / 100.

    max_quantity is a cap in the same units as fixed_quantity:
    shares for Equity, lots for FnO. Zero means no configured cap.
    For budget modes, quantity is always rounded down. This is an
    estimated notional-value calculation, not a broker margin calculator.
    """
    mode = str(mode).strip().upper()
    aliases = {
        "FIXED": "FIXED_QUANTITY",
        "QUANTITY": "FIXED_QUANTITY",
        "AMOUNT": "FIXED_AMOUNT",
        "RUPEES": "FIXED_AMOUNT",
        "PERCENT": "CAPITAL_PERCENT",
        "CAPITAL_PCT": "CAPITAL_PERCENT",
    }
    mode = aliases.get(mode, mode)

    if mode not in {"FIXED_QUANTITY", "FIXED_AMOUNT", "CAPITAL_PERCENT"}:
        raise ValueError(f"Unsupported sizing mode: {mode!r}")

    if isinstance(lot_size, bool) or not isinstance(lot_size, int) or lot_size < 1:
        raise ValueError("lot_size must be a positive integer")

    if isinstance(max_quantity, bool) or not isinstance(max_quantity, int) or max_quantity < 0:
        raise ValueError("max_quantity must be a non-negative integer")

    price = float(price)
    if not math.isfinite(price) or price <= 0:
        raise ValueError("price must be finite and greater than zero")

    if mode == "FIXED_QUANTITY":
        if isinstance(fixed_quantity, bool) or not isinstance(fixed_quantity, int) or fixed_quantity < 1:
            raise ValueError("fixed_quantity must be a positive integer")
        units = min(fixed_quantity, max_quantity) if max_quantity else fixed_quantity
        budget = 0.0

    else:
        if mode == "FIXED_AMOUNT":
            budget = float(fixed_amount)
            if not math.isfinite(budget) or budget <= 0:
                raise ValueError("fixed_amount must be finite and greater than zero")
        else:
            capital = float(capital)
            capital_percent = float(capital_percent)
            if not math.isfinite(capital) or capital <= 0:
                raise ValueError("capital must be finite and greater than zero")
            if not math.isfinite(capital_percent) or not 0 < capital_percent <= 100:
                raise ValueError("capital_percent must be greater than 0 and at most 100")
            budget = capital * capital_percent / 100.0

        units = math.floor(budget / (price * lot_size))
        if max_quantity:
            units = min(units, max_quantity)

        if units < 1:
            raise ValueError(
                f"Budget ₹{budget:.2f} cannot cover one unit "
                f"at estimated value ₹{price * lot_size:.2f}"
            )

    quantity = units * lot_size
    estimated_value = quantity * price

    if mode != "FIXED_QUANTITY" and estimated_value > budget + 1e-8:
        raise ValueError("Calculated position exceeds its configured budget")

    return PositionSize(
        mode=mode,
        quantity=quantity,
        lots=units,
        budget=budget,
        estimated_value=estimated_value,
        unit_price=price,
    )
