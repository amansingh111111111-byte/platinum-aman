#!/usr/bin/env python3
"""Interactive, configuration-only setup wizard for Platinum Bot."""

import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path.home() / "platinum-aman"
CONFIGS = {
    "equity": ROOT / "equity.env",
    "fno": ROOT / "fno_agent" / ".env",
}


def read_env(path):
    result = {}
    if path.exists():
        for line in path.read_text().splitlines():
            text = line.strip()
            if text and not text.startswith("#") and "=" in text:
                key, value = text.split("=", 1)
                result[key.strip()] = value.strip().strip("'\"")
    return result


def ask(prompt, default=None, validator=None):
    while True:
        suffix = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{suffix}: ").strip()
        if not value and default is not None:
            value = str(default)
        if not value:
            print("A value is required.")
            continue
        if validator:
            try:
                validator(value)
            except (ValueError, TypeError) as exc:
                print(f"Invalid value: {exc}")
                continue
        return value


def positive_int(value):
    if int(value) <= 0:
        raise ValueError("enter an integer greater than zero")


def nonnegative_int(value):
    if int(value) < 0:
        raise ValueError("enter zero or a positive integer")


def positive_float(value):
    if float(value) <= 0:
        raise ValueError("enter a number greater than zero")


def pct(value):
    number = float(value)
    if not 0 < number <= 100:
        raise ValueError("percentage must be greater than 0 and at most 100")


def yes_no(prompt, default="yes"):
    while True:
        value = ask(f"{prompt} (yes/no)", default).lower()
        if value in ("yes", "y"):
            return True
        if value in ("no", "n"):
            return False
        print("Please enter yes or no.")


def show_current():
    for name, path in CONFIGS.items():
        values = read_env(path)
        print(f"\n--- {name.upper()} ({path.relative_to(ROOT)}) ---")
        safe_keys = (
            "TESTING_MODE", "TRADE_AMOUNT_INR", "DEFAULT_QUANTITY",
            "EQUITY_SL_TARGET_ENABLED", "EQUITY_SL_PCT",
            "EQUITY_TARGET_PCT", "EQUITY_SL_LIMIT_BUFFER_PCT",
            "EQUITY_MAX_SIGNAL_AGE_SEC", "FNO_CAPITAL_PER_TRADE",
            "FNO_MAX_LOTS", "FNO_MAX_CONCURRENT_SIGNALS",
            "FNO_MAX_SIGNAL_AGE_SEC", "FNO_SL_TARGET_ENABLED",
            "FNO_SL_PCT", "FNO_TARGET_PCT", "FNO_ENFORCE_MARKET_HOURS",
        )
        for key in safe_keys:
            if key in values:
                print(f"  {key}={values[key]}")
        print("  TESTING_MODE=ON (required for this setup wizard)")


def update_env(path, changes):
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    # Back up the existing file before any modification.
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_name(path.name + f".backup_{stamp}")
    shutil.copy2(path, backup)

    lines = path.read_text().splitlines()
    written = set()
    output = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in changes:
                if key not in written:
                    output.append(f"{key}={changes[key]}")
                    written.add(key)
                continue
        output.append(line)

    for key, value in changes.items():
        if key not in written:
            output.append(f"{key}={value}")

    fd, temporary = tempfile.mkstemp(prefix=".platinum-env-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write("\n".join(output) + "\n")
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

    print(f"Saved {path.relative_to(ROOT)}")
    print(f"Backup: {backup.name}")


def configure_equity():
    path = CONFIGS["equity"]
    old = read_env(path)
    print("\nEQUITY POSITION SIZING")
    print("1. Fixed quantity of shares")
    print("2. Fixed rupee amount per trade")
    choice = ask("Choose sizing mode", "1",
                 lambda x: None if x in ("1", "2") else
                 (_ for _ in ()).throw(ValueError("choose 1 or 2")))

    changes = {"TESTING_MODE": "ON"}

    if choice == "1":
        quantity = ask("Number of shares per trade",
                       old.get("DEFAULT_QUANTITY", "1"), positive_int)
        changes.update({
            "TRADE_AMOUNT_INR": "0",
            "DEFAULT_QUANTITY": str(int(quantity)),
        })
        summary = f"Fixed quantity: {quantity} shares"
    else:
        amount = ask("Maximum rupee budget per trade",
                     old.get("TRADE_AMOUNT_INR", "10000"), positive_float)
        changes.update({
            "TRADE_AMOUNT_INR": str(int(float(amount))),
            "DEFAULT_QUANTITY": "1",
        })
        summary = f"Fixed budget: ₹{float(amount):,.2f} per trade"

    if yes_no("Enable configured equity stop-loss and target",
              "yes" if old.get("EQUITY_SL_TARGET_ENABLED", "false").lower()
              in ("true", "1", "yes") else "no"):
        sl = ask("Stop-loss percentage",
                 old.get("EQUITY_SL_PCT", "1"), pct)
        target = ask("Target percentage",
                     old.get("EQUITY_TARGET_PCT", "2"), pct)
        buffer = ask("Stop-loss limit buffer percentage",
                     old.get("EQUITY_SL_LIMIT_BUFFER_PCT", "1"), pct)
        changes.update({
            "EQUITY_SL_TARGET_ENABLED": "true",
            "EQUITY_SL_PCT": sl,
            "EQUITY_TARGET_PCT": target,
            "EQUITY_SL_LIMIT_BUFFER_PCT": buffer,
        })
    else:
        changes["EQUITY_SL_TARGET_ENABLED"] = "false"

    age = ask("Maximum signal age in seconds",
              old.get("EQUITY_MAX_SIGNAL_AGE_SEC", "120"), positive_int)
    changes["EQUITY_MAX_SIGNAL_AGE_SEC"] = str(int(age))
    return path, changes, summary


def configure_fno():
    path = CONFIGS["fno"]
    old = read_env(path)
    print("\nFNO POSITION SIZING")
    print("The current FnO executor supports a rupee budget per trade")
    print("and a maximum-lots cap. Fixed-lots and percentage sizing")
    print("require execution-code integration before they can be selected.")

    budget = ask("Maximum rupee budget per trade",
                 old.get("FNO_CAPITAL_PER_TRADE", "10000"), positive_float)
    max_lots = ask("Maximum lots per trade (0 = no extra lots cap)",
                   old.get("FNO_MAX_LOTS", "1"), nonnegative_int)
    concurrent = ask("Maximum concurrent signals",
                     old.get("FNO_MAX_CONCURRENT_SIGNALS", "1"),
                     positive_int)
    age = ask("Maximum signal age in seconds",
              old.get("FNO_MAX_SIGNAL_AGE_SEC", "120"), positive_int)

    changes = {
        "TESTING_MODE": "ON",
        "FNO_CAPITAL_PER_TRADE": str(float(budget)),
        "FNO_MAX_LOTS": str(int(max_lots)),
        "FNO_MAX_CONCURRENT_SIGNALS": str(int(concurrent)),
        "FNO_MAX_SIGNAL_AGE_SEC": str(int(age)),
    }

    if yes_no("Enforce market-hours checks",
              "yes" if old.get("FNO_ENFORCE_MARKET_HOURS", "true").lower()
              in ("true", "1", "yes") else "no"):
        changes["FNO_ENFORCE_MARKET_HOURS"] = "true"
    else:
        changes["FNO_ENFORCE_MARKET_HOURS"] = "false"

    if yes_no("Enable configured FnO stop-loss and target",
              "yes" if old.get("FNO_SL_TARGET_ENABLED", "true").lower()
              in ("true", "1", "yes") else "no"):
        sl = ask("Stop-loss percentage",
                 old.get("FNO_SL_PCT", "20"), pct)
        target = ask("Target percentage",
                     old.get("FNO_TARGET_PCT", "30"), pct)
        changes.update({
            "FNO_SL_TARGET_ENABLED": "true",
            "FNO_SL_PCT": sl,
            "FNO_TARGET_PCT": target,
        })
    else:
        changes["FNO_SL_TARGET_ENABLED"] = "false"

    return path, changes, (
        f"Budget: ₹{float(budget):,.2f}; max lots: {max_lots}; "
        f"concurrent signals: {concurrent}"
    )


def main():
    if not ROOT.is_dir():
        print(f"Platinum project not found: {ROOT}", file=sys.stderr)
        return 1

    while True:
        print("\n========== PLATINUM BOT SETUP ==========")
        print("1. Configure Equity")
        print("2. Configure FnO")
        print("3. View current non-secret settings")
        print("4. Exit")
        choice = ask("Choose an option", "1")
        if choice == "3":
            show_current()
            continue
        if choice == "4":
            print("No changes made.")
            return 0
        if choice not in ("1", "2"):
            print("Choose 1, 2, 3 or 4.")
            continue

        try:
            path, changes, summary = (
                configure_equity() if choice == "1" else configure_fno()
            )
        except (ValueError, FileNotFoundError, OSError) as exc:
            print(f"Setup cancelled: {exc}")
            continue

        print("\n========== REVIEW ==========")
        print(f"Worker: {'Equity' if choice == '1' else 'FnO'}")
        print(summary)
        print("Testing mode: ON")
        print("Services: will NOT be started or restarted.")
        print("Live orders: will NOT be placed by this wizard.")

        if not yes_no("Save these settings?", "no"):
            print("Cancelled; configuration unchanged.")
            continue

        try:
            update_env(path, changes)
        except (OSError, ValueError) as exc:
            print(f"Save failed: {exc}")
            return 1
        print("Saved. Testing mode remains ON.")
        print("This wizard does not deploy, start, or restart workers.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
