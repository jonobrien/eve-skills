# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""eveapi_simple.py: simple eve api query helper"""

#from httplib import HTTPSConnection
#from lxml import objectify

from esipy import App, EsiClient, EsiSecurity
import os

class APIError(Exception):
    pass

class ESIClient():
    """
    didn't use esiSecurity for callback handling as flask seems fine
    """
    def __init__(self, token, refresh=False):
        self.client_id = os.environ.get('EVE_SKILLS_CID')
        self.secret_id = os.environ.get('EVE_SKILLS_SECRET')
        self.redir_url = os.environ.get('EVE_SKILLS_REDIR')
        self.app = App.create(url="https://esi.evetech.net/latest/swagger.json?datasource=tranquility")
        self.security = EsiSecurity(
            app=self.app,
            redirect_uri=self.redir_url,
            client_id=self.client_id,
            secret_key=self.secret_id,
        )
        self.client = EsiClient(
            header={'User-Agent': 'EVE-SKILLS'},
            raw_body_only=False,  # parse json automatically, slow, bad performance
            security=self.security
        )
        self.token = None
        if not refresh:
            self.token = self.security.auth(token)  # use code from login redirect
        if refresh:
            print('[I] refreshing token')
            self.security.update_token({
                'access_token': '',
                'expires_in': -1,  # force refresh anyway
                'refresh_token': token
            })
            self.token = self.security.refresh()

        print(self.token)


    def get_info(self):
        return self.security.verify()  # verify token, get character info


def get_skills(cli, cid):
    """Query the eve online API and return a result object."""



    # generate the operation tuple
    # the parameters given are the actual parameters the endpoint requires
    skills_op = cli.app.op['get_characters_character_id_skills'](
        character_id=cid
    )

    response = cli.client.request(skills_op)

    return response.data
