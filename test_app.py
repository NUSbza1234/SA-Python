import unittest
import pandas as pd
from sa_main import load_data, get_returns_emoji, get_ema_emoji, get_rsi_emoji, get_adx_emoji

class TestStockAnalysis(unittest.TestCase):

    def setUp(self):
        # Common setup for all tests
        self.stock = "AAPL"
        self.period = "1y"

    def test_load_data(self):
        # Test if data loading function works and returns a DataFrame
        df = load_data(self.stock, self.period)
        self.assertIsInstance(df, pd.DataFrame, "load_data should return a DataFrame")
        self.assertIn("close", df.columns, "DataFrame should have a 'close' column")
        self.assertGreater(len(df), 0, "DataFrame should not be empty")

    def test_get_returns_emoji(self):
        # Test return emoji function
        self.assertEqual(get_returns_emoji(5), ":white_check_mark:", "Positive return should give a check mark emoji")
        self.assertEqual(get_returns_emoji(-5), ":red_circle:", "Negative return should give a red circle emoji")

    def test_get_ema_emoji(self):
        # Test EMA emoji function
        self.assertEqual(get_ema_emoji(150, 140), ":white_check_mark:", "LTP greater than EMA should give a check mark emoji")
        self.assertEqual(get_ema_emoji(130, 140), ":red_circle:", "LTP less than EMA should give a red circle emoji")

    def test_get_rsi_emoji(self):
        # Test RSI emoji function
        self.assertEqual(get_rsi_emoji(50), ":white_check_mark:", "RSI between 30 and 70 should give a check mark emoji")
        self.assertEqual(get_rsi_emoji(75), ":red_circle:", "RSI outside 30 to 70 range should give a red circle emoji")

    def test_get_adx_emoji(self):
        # Test ADX emoji function
        self.assertEqual(get_adx_emoji(30), ":white_check_mark:", "ADX greater than 25 should give a check mark emoji")
        self.assertEqual(get_adx_emoji(20), ":red_circle:", "ADX less than 25 should give a red circle emoji")

if __name__ == '__main__':
    unittest.main()
