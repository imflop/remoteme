class LevelType:
    """
    Класс коллекиця уровней кандидата
    """

    INTERN: str = "intern"
    JUNIOR: str = "junior"
    MIDDLE: str = "middle"
    SENIOR: str = "senior"
    CTO: str = "cto"

    ITEMS = (
        INTERN,
        JUNIOR,
        MIDDLE,
        SENIOR,
        CTO
    )

    CHOICES = (
        (INTERN, 'Intern'),
        (JUNIOR, 'Junior'),
        (MIDDLE, 'Middle'),
        (SENIOR, 'Senior'),
        (CTO, 'CTO'),
    )


class CurrencyType:
    """
    Класс коллекция валют
    """
    USD: str = "usd"
    EUR: str = "eur"
    RUB: str = "rub"
    GBP: str = "gbp"
    CNY: str = "cny"
    UAH: str = "uah"

    ITEMS = (
        USD,
        EUR,
        GBP,
        CNY,
        RUB,
        UAH
    )

    CHOICES = (
        (USD, '$'),
        (EUR, '€'),
        (GBP, '£'),
        (CNY, '¥'),
        (RUB, '₽'),
        (UAH, '₴')
    )

    @classmethod
    def get_icon_by_name(cls, val: str) -> str:
        return {
            'usd': '$',
            'eur': '€',
            'gbp': '£',
            'cny': '¥',
            'rub': '₽',
            'uah': '₴'
        }.get(val) if val else '$'
