from pony.orm import Required, Set

from serpentin.core.database import db
from serpentin.models.compensations import Compensation
from serpentin.models.executives import Executive


class Statement(db.Entity):
    executive = Required(Executive)
    month = Required(int)
    year = Required(int)

    compensations = Set("StatementCompensation")

    def get_formatted_data(self) -> dict:
        return {
            "executive": self.executive.name,
            "month": self.month,
            "year": self.year,
        }


class StatementCompensation(db.Entity):
    compensation = Required(Compensation)
    statement = Required(Statement)
    amount = Required(float)

    def get_formatted_data(self) -> dict:
        return {
            "statement": self.statement.get_formatted_data(),
            "compensation": self.compensation.get_formatted_data(),
            "amount": self.amount,
        }
