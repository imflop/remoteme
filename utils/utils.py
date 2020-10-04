def str2bool(string: str) -> bool:
    """
    Приводит строку к булеву значению
    :param string: строка
    """
    return string.lower() in ("yes", "true", "t", "1")


def bool2str(boolean: bool) -> str:
    """
    Приводит bool в строковое значение
    :param boolean: boolean
    """
    return 'true' if boolean else 'false'
