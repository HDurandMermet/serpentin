from pony.orm import select
from serpentin.models.executives import Executive


def get_executives() -> Executive:
    return select(e for e in Executive)
