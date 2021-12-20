from datetime import date

from pony.orm import Optional, Required
from serpentin.core.database import db
from serpentin.models.executives import Executive


class Deal(db.Entity):
    name = Required(str)
    active = Required(bool, sql_default=True)
    modified = Required(bool, sql_default=False)

    amount = Optional(float)
    closed = Optional(bool)
    close_date = Optional(date)
    owner = Optional(Executive)

    def get_formatted_data(self) -> dict:
        return {
            "name": self.name,
            "active": self.active,
            "modified": self.modified,
            "amount": self.amount,
            "closed": self.closed,
            "close_date": str(self.close_date) if self.close_date is not None else None,
            "owner": self.owner.name if self.owner is not None else None,
        }
