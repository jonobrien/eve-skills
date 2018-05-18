# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""skillsheet.py: """
from esipy.exceptions import APIException

import eveapi_simple as api
from evestatic import StaticDB

from flask.views import MethodView
from flask import request, make_response, redirect
from urllib.parse import urlencode




class SkillSheet(MethodView):
    def get(self):
        print('='*20)
        characters = []
        token = request.args.get('code')
        cli = None
        try:  # refresh page, just relogin instead of storing tokens between sessions (bad)
            cli = api.ESIClient(token)
        except APIException:
            return make_response(redirect('/api/v1/login'))

        data = cli.get_info()
        cID = data['CharacterID']
        cName = data['CharacterName']
        enc_data = urlencode({'n':cName, 'cid':cID, 'rtok':cli.token['refresh_token']})  # need a quick way to access other route

        html = '<!DOCTYPE html>'
        html += '<html>'
        html +='<head>'
        html +='<title>API key info</title>'
        html +='<link rel="stylesheet" type="text/css" href="/static/style.css" />'
        html +='</head>'
        html +='<body>'
        html += '<a href=/api/v1/skillcheck/{0}>skillcheck</a>'.format(enc_data)
        html += '<br><br>'
        html += '<a href=/api/v1/login><img src=https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-small.png /></a>'
        html += '<br><br>'
        html += 're-login to see other toons on account'
        html +='</body>'
        html +='</html>'

        sdb = StaticDB()

        charsheet = api.get_skills(cli, cID)

        skills = {}
        for skill in charsheet['skills']:
            skill_id = int(skill['skill_id'])
            skill_level = int(skill['trained_skill_level'])
            skill_name = sdb.skill_name(skill_id)
            skill_group = sdb.skill_group(skill_id)
            if skill_group not in skills:
                skills[skill_group] = []
            skills[skill_group].append((skill_name, skill_id, skill_level))

        html +='<h2>{0}</h2>'.format(cName)
        for group in sorted(skills.keys()):
            html +='<h3>{0}</h3>'.format(group)
            html +='<table class="skills">'
            for skill in sorted(skills[group]):
                skill_name, skill_id, skill_level = skill
                html +='<tr>'
                html +='<td>' if skill_level < 5 else '<td class="l5skill">'
                html +='<a class="igblink" onclick="CCPEVE.showInfo({0})">{1}</a></td>'.format(skill_id, skill_name)  # rip igb o7
                html +='<td><img src="/static/gfx/level{0}.png" alt="Level {1}" /></td>'.format(skill_level, skill_level)
                html +='</tr>'
            html +='</table>'

        html +='</body>'
        html +='</html>'
        return html
