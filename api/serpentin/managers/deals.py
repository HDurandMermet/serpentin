from pony.orm import select

from serpentin.models.deals import Deal
from serpentin.models.executives import Executive


def get_deals() -> Deal:
    return select(d for d in Deal)


def get_deals_by_executives(executives: Executive) -> list[Deal]:
    return executives.deals
