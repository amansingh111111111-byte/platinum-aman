import unittest

from position_sizing import calculate_position_size


class PositionSizingTests(unittest.TestCase):
    def test_equity_fixed_quantity(self):
        r = calculate_position_size(
            mode="FIXED_QUANTITY", price=250, fixed_quantity=10
        )
        self.assertEqual(r.quantity, 10)
        self.assertEqual(r.estimated_value, 2500)

    def test_equity_fixed_quantity_cap(self):
        r = calculate_position_size(
            mode="FIXED_QUANTITY", price=250,
            fixed_quantity=10, max_quantity=4,
        )
        self.assertEqual(r.quantity, 4)

    def test_equity_fixed_amount_rounds_down(self):
        r = calculate_position_size(
            mode="FIXED_AMOUNT", price=333, fixed_amount=1000
        )
        self.assertEqual(r.quantity, 3)
        self.assertEqual(r.estimated_value, 999)

    def test_capital_percentage(self):
        r = calculate_position_size(
            mode="CAPITAL_PERCENT", price=100,
            capital=50000, capital_percent=2,
        )
        self.assertEqual(r.budget, 1000)
        self.assertEqual(r.quantity, 10)

    def test_fno_amount_calculates_whole_lots(self):
        r = calculate_position_size(
            mode="FIXED_AMOUNT", price=120,
            lot_size=25, fixed_amount=7000,
        )
        self.assertEqual(r.lots, 2)
        self.assertEqual(r.quantity, 50)
        self.assertEqual(r.estimated_value, 6000)

    def test_fno_lot_cap(self):
        r = calculate_position_size(
            mode="FIXED_AMOUNT", price=100,
            lot_size=50, fixed_amount=50000, max_quantity=3,
        )
        self.assertEqual(r.lots, 3)
        self.assertEqual(r.quantity, 150)

    def test_rejects_missing_price(self):
        with self.assertRaises(ValueError):
            calculate_position_size(
                mode="FIXED_AMOUNT", price=0, fixed_amount=1000
            )

    def test_rejects_budget_below_one_share(self):
        with self.assertRaises(ValueError):
            calculate_position_size(
                mode="FIXED_AMOUNT", price=1500, fixed_amount=1000
            )

    def test_rejects_budget_below_one_fno_lot(self):
        with self.assertRaises(ValueError):
            calculate_position_size(
                mode="FIXED_AMOUNT", price=100,
                lot_size=25, fixed_amount=2000,
            )

    def test_rejects_invalid_percentage(self):
        with self.assertRaises(ValueError):
            calculate_position_size(
                mode="CAPITAL_PERCENT", price=100,
                capital=50000, capital_percent=101,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
