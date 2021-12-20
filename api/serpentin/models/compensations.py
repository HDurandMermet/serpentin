from pony.orm import Required, Set

from serpentin.core.database import db


class Compensation(db.Entity):
    name = Required(str)
    type = Required(str)  # Can be Simple or Complex
    statement_compensations = Set("StatementCompensation")

    def get_formatted_data(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
        }
