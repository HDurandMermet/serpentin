import calendar
import datetime
import random

from faker import Faker
from pony.orm import db_session, commit, select

from serpentin.core.database import connect_to_database
from serpentin.models.deals import Deal
from serpentin.models.executives import Executive

connect_to_database()
fake = Faker("fr-FR")


@db_session
def provision_database():
    for _ in range(5):
        Executive(name=fake.name())
    commit()

    executives = select(e for e in Executive)

    for year in range(2020, 2023):
        for month in range(1, 13):
            month_range = calendar.monthrange(year, month)

            for executive in executives:
                for _ in range(random.randint(2, 10)):
                    closed = random.random() > 0.5

                    close_date = None
                    if closed:
                        close_date = fake.date_between(
                            start_date=datetime.date(
                                month=month, year=year, day=1
                            ),
                            end_date=datetime.date(
                                month=month, year=year, day=month_range[1]
                            ),
                        )

                    Deal(
                        name=fake.company(),
                        active=True,
                        modified=False,
                        amount=random.randint(10, 50) * 100,
                        closed=closed,
                        close_date=close_date,
                        owner=executive,
                    )

            commit()


if __name__ == "__main__":
    provision_database()
