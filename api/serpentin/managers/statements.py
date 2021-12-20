from pony.orm import (
    select,
    get,
    db_session,
    commit,
    count
)

from serpentin.models.deals import Deal
from serpentin.models.compensations import Compensation
from serpentin.models.executives import Executive
from serpentin.models.statements import (
    Statement,
    StatementCompensation
)


def get_statements() -> Statement:
    return select(s for s in Statement)


@db_session
def post_statement(executive_id: int, month: int, year: int) -> Statement:
    executive = get(e for e in Executive if e.id == executive_id)
    statement = Statement(
        executive=executive,
        month=month,
        year=year
    )
    commit()
    return statement


def get_statement_compensations() -> StatementCompensation:
    return select(sc for sc in StatementCompensation)


@db_session
def post_statement_compensation(compensation: Compensation, statement: Statement):
    if compensation.type == "Simple":
        number_of_closed_deals = count(
            d for d in Deal 
            if d.closed is True and d.owner == statement.executive
            and d.close_date.month == statement.month
            and d.close_date.year == statement.year
        )
        if number_of_closed_deals < 1:
            raise ValueError("Owner has no closed deals for this month")

        deals_sum_for_owner_and_month = get(
            (d.close_date.month, sum(d.amount)) for d in Deal 
            if d.closed is True and d.owner == statement.executive
            and d.close_date.month == statement.month
            and d.close_date.year == statement.year
        )[1]
        print(deals_sum_for_owner_and_month)
        if deals_sum_for_owner_and_month > 500:
            if number_of_closed_deals > 4:
                compensation_amount = deals_sum_for_owner_and_month * 0.2
            else:
                compensation_amount = deals_sum_for_owner_and_month * 0.1
        else:
            compensation_amount = 500

        response = StatementCompensation(
            compensation=compensation,
            statement=statement,
            amount=compensation_amount
        )
        commit()

        return response

        
        
