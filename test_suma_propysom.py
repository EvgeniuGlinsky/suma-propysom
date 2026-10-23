import unittest
from decimal import Decimal

from suma_propysom import form, number_words, suma_propysom

UAH = ("гривня", "гривні", "гривень")


class Forms(unittest.TestCase):
    def test_noun_forms(self):
        cases = {1: "гривня", 2: "гривні", 4: "гривні", 5: "гривень", 11: "гривень", 12: "гривень",
                 14: "гривень", 20: "гривень", 21: "гривня", 22: "гривні", 25: "гривень", 101: "гривня",
                 111: "гривень", 112: "гривень", 1000: "гривень", 1001: "гривня"}
        for n, expected in cases.items():
            self.assertEqual(form(n, UAH), expected, n)


class Words(unittest.TestCase):
    def test_numbers(self):
        cases = {
            0: "нуль",
            1: "одна",
            2: "дві",
            12: "дванадцять",
            21: "двадцять одна",
            205: "двісті п’ять",
            1000: "одна тисяча",
            2000: "дві тисячі",
            5000: "п’ять тисяч",
            11000: "одинадцять тисяч",
            21000: "двадцять одна тисяча",
            22500: "двадцять дві тисячі п’ятсот",
            1000000: "один мільйон",
            2000000: "два мільйони",
            1234567: "один мільйон двісті тридцять чотири тисячі п’ятсот шістдесят сім",
        }
        for n, expected in cases.items():
            self.assertEqual(number_words(n), expected, n)


class Amounts(unittest.TestCase):
    def test_invoice_amounts(self):
        self.assertEqual(suma_propysom(Decimal("1250.50")), "Одна тисяча двісті п’ятдесят гривень 50 копійок")
        self.assertEqual(suma_propysom("1"), "Одна гривня 00 копійок")
        self.assertEqual(suma_propysom("22.01"), "Двадцять дві гривні 01 копійка")
        self.assertEqual(suma_propysom("4000"), "Чотири тисячі гривень 00 копійок")
        self.assertEqual(suma_propysom("11.12"), "Одинадцять гривень 12 копійок")
        self.assertEqual(suma_propysom("0.99"), "Нуль гривень 99 копійок")
        self.assertEqual(suma_propysom("2.345"), "Дві гривні 35 копійок")  # округлення до копійки

    def test_kopecks_in_words(self):
        self.assertEqual(suma_propysom("3.21", kopecks_as_digits=False),
                         "Три гривні двадцять одна копійка")

    def test_other_currencies(self):
        self.assertEqual(suma_propysom("21", "USD"), "Двадцять один долар 00 центів")
        self.assertEqual(suma_propysom("2", "USD"), "Два долари 00 центів")
        self.assertEqual(suma_propysom("100", "EUR"), "Сто євро 00 центів")

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            suma_propysom("-5")


if __name__ == "__main__":
    unittest.main()
