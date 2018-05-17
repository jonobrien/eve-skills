# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""eveapi_simple.py: simple eve api query helper"""

#from httplib import HTTPSConnection
#from lxml import objectify

from esipy import App, EsiClient


class APIError(Exception):
    pass

class ESIClient():
    """
    didn't use esiSecurity for callback handling as flask seems fine
    """
    def __init__(self):
        self.app = App.create(url="https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility")
        self.client = EsiClient(
            header={'User-Agent': 'EVE-SKILLS'},
            raw_body_only=False,  # parse json automatically, slow, bad performance
        )

def get_skills(cli, args=None):
    """Query the eve online API and return a result object."""



    # generate the operation tuple
    # the parameters given are the actual parameters the endpoint requires
    market_order_operation = cli.app.op['get_markets_region_id_orders'](
        region_id=10000002,
        type_id=34,
        order_type='all',
    )

    response = cli.client.request(market_order_operation)

    return response.data

def get_character(cli):
    """
    esi uses access_tokens associated with a single toon
    """
    return {'message': 'success'}


