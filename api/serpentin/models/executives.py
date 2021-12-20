from pony.orm import Required, Set

from serpentin.core.database import db


class Executive(db.Entity):
    name = Required(str)
    deals = Set("Deal")
    statements = Set("Statement")

    def get_formatted_data(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
        }

