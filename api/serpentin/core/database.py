from pony.orm import Database

db = Database()


def connect_to_database():
    db.bind(provider="sqlite", filename="./database.sqlite", create_db=True)

    from serpentin.models import compensations
    from serpentin.models import deals
    from serpentin.models import executives
    from serpentin.models import statements

    db.generate_mapping(create_tables=True)
