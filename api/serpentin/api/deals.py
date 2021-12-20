from flask_restful import Resource
from serpentin.api import api
from serpentin.managers.deals import get_deals


class Deals(Resource):
    def get(self):
        """Return deals"""

        deals = get_deals()
        formatted_deals = [d.get_formatted_data() for d in deals]

        return {"deals": formatted_deals}


api.add_resource(Deals, "/deals")
