from random import randrange

from .models import Opinion


def random_opinion():
    """Возвращает случайное мнение или None, если база пуста."""
    quantity = Opinion.query.count()
    if not quantity:
        return None
    offset_value = randrange(quantity)
    return Opinion.query.offset(offset_value).first()
