class LevelType:
    """
    Класс коллекиця уровней кандидата
    """

    INTERN: str = 'intern'
    JUNIOR: str = 'junior'
    MIDDLE: str = 'middle'
    SENIOR: str = 'senior'
    CTO: str = 'cto'

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
