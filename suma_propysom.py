"""Сума прописом українською для рахунків і актів.

    >>> suma_propysom(Decimal("1250.50"))
    'Одна тисяча двісті п’ятдесят гривень 50 копійок'

Рід і відмінювання: гривня — жіночого роду (одна, дві гривні), тисяча — теж (дві тисячі),
мільйон — чоловічого (два мільйони). Форма слова залежить від останніх двох цифр:
1 → гривня, 2–4 → гривні, 5–20 і 0 → гривень (11–14 завжди «гривень»).
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

ONES_M = ["", "один", "два", "три", "чотири", "п’ять", "шість", "сім", "вісім", "дев’ять"]
ONES_F = ["", "одна", "дві", "три", "чотири", "п’ять", "шість", "сім", "вісім", "дев’ять"]
TEENS = ["десять", "одинадцять", "дванадцять", "тринадцять", "чотирнадцять", "п’ятнадцять",
         "шістнадцять", "сімнадцять", "вісімнадцять", "дев’ятнадцять"]
TENS = ["", "", "двадцять", "тридцять", "сорок", "п’ятдесят", "шістдесят", "сімдесят",
        "вісімдесят", "дев’яносто"]
HUNDREDS = ["", "сто", "двісті", "триста", "чотириста", "п’ятсот", "шістсот", "сімсот",
            "вісімсот", "дев’ятсот"]

# (одна, дві–чотири, п’ять і більше), рід
UNITS = [
    (("", "", ""), "f"),                                  # одиниці: назву валюти додаємо окремо
    (("тисяча", "тисячі", "тисяч"), "f"),
    (("мільйон", "мільйони", "мільйонів"), "m"),
    (("мільярд", "мільярди", "мільярдів"), "m"),
]
CURRENCIES = {
    "UAH": (("гривня", "гривні", "гривень"), ("копійка", "копійки", "копійок")),
    "USD": (("долар", "долари", "доларів"), ("цент", "центи", "центів")),
    "EUR": (("євро", "євро", "євро"), ("цент", "центи", "центів")),
}


def form(n: int, forms: tuple[str, str, str]) -> str:
    """Форма іменника після числа n: 1 гривня, 2 гривні, 5 гривень, 11 гривень, 21 гривня."""
    n = abs(n) % 100
    if 11 <= n <= 14:
        return forms[2]
    last = n % 10
    if last == 1:
        return forms[0]
    if 2 <= last <= 4:
        return forms[1]
    return forms[2]


def triad(n: int, gender: str) -> list[str]:
    words = [HUNDREDS[n // 100]]
    rest = n % 100
    if 10 <= rest <= 19:
        words.append(TEENS[rest - 10])
    else:
        words.append(TENS[rest // 10])
        words.append((ONES_F if gender == "f" else ONES_M)[rest % 10])
    return [w for w in words if w]


def number_words(n: int, gender: str = "f") -> str:
    if n == 0:
        return "нуль"
    parts: list[str] = []
    for power in range(len(UNITS) - 1, -1, -1):
        chunk = (n // 1000 ** power) % 1000
        if not chunk:
            continue
        forms, unit_gender = UNITS[power]
        words = triad(chunk, gender if power == 0 else unit_gender)
        if power:
            words.append(form(chunk, forms))
        parts.extend(words)
    return " ".join(parts)


def suma_propysom(amount: Decimal | int | float | str, currency: str = "UAH",
                  kopecks_as_digits: bool = True) -> str:
    """'1250.50' → 'Одна тисяча двісті п’ятдесят гривень 50 копійок'.

    Копійки в бухгалтерських документах прийнято писати цифрами; kopecks_as_digits=False пише словами.
    """
    value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if value < 0:
        raise ValueError("сума не може бути від’ємною")
    whole = int(value)
    cents = int((value - whole) * 100)
    main_forms, minor_forms = CURRENCIES[currency]
    main_gender = "m" if currency in ("USD",) else "f"
    text = f"{number_words(whole, main_gender)} {form(whole, main_forms)}"
    minor = f"{cents:02d}" if kopecks_as_digits else number_words(cents, "f" if currency == "UAH" else "m")
    text += f" {minor} {form(cents, minor_forms)}"
    return text[0].upper() + text[1:]


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:] or ["1250.50"]:
        print(arg, "→", suma_propysom(arg))
