from pony.orm import (
    db_session,
    commit,
    select,
)

from serpentin.models.compensations import Compensation


def get_compensations() -> Compensation:
    return select(c for c in Compensation)


@db_session
def post_compensation(name: str, type: str) -> Compensation:
    compensation = Compensation(
        name=name,
        type=type
    )
    commit()
    return compensation
