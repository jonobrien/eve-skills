# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""skillcheck.py: """

from flask.views import MethodView

import csv
import eveapi_simple as api
from evestatic import StaticDB
from urllib.parse import parse_qs

from esipy.exceptions import APIException




class SkillCheck(MethodView):
    def get(self, token):
        """
        token is urlencode({'n':cName, 'cid':cID, 'rtok':cli.token['refresh_token']})
        """
        sdb = StaticDB()

        data = parse_qs(token)

        data = parse_qs(token)
        cName = data['n'][0]
        cid = data['cid'][0]
        rTok = data['rtok'][0]
        print(rTok)
        cli = None
        try:  # refresh page, just relogin instead of storing tokens between sessions (bad)
            cli = api.ESIClient(rTok, refresh=True)
        except APIException:
            return make_response(redirect('/api/v1/login'))
        skillset_name = 'test.csv'


        skillset = {}
        skillset_name = 'test.csv'
        with open(skillset_name, 'r') as csvfile:
            skillsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in skillsreader:
                skill_group, skill_name, required_level = row
                required_level = int(required_level)
                if not 1 <= required_level <= 5:
                    continue
                skill_id = sdb.skill_id(skill_name)
                if skill_group not in skillset:
                    skillset[skill_group] = []
                skillset[skill_group].append((skill_name, skill_id, required_level))

        #api_args = {'keyID': argv[2], 'vCode': argv[3]}


        title = "Skillcheck - %s" % skillset_name

        html = '<!DOCTYPE html>'
        html += '<html>'
        html += '<head>'
        html += '<title>%s</title>' % title
        html += '<link rel="stylesheet" type="text/css" href="/static/style.css" />'
        html += '</head>'
        html += '<body>'
        html += '<br><br>'
        html += '<a href=/api/v1/login><img src=https://web.ccpgamescdn.com/eveonlineassets/developers/eve-sso-login-black-small.png /></a>'
        html += '<br><br>'
        html += 're-login to see other toons on account'
        html += '<h1>%s</h1>' % title

        char_id, char_name = (cid, cName)
        charsheet = api.get_skills(cli, cid)
        trained_skills = {}
        for skill in charsheet['skills']:
            skill_id = int(skill['skill_id'])
            skill_level = int(skill['trained_skill_level'])
            skill_name = sdb.skill_name(skill_id)
            trained_skills[skill_name] = required_level

        html += '<h2>{0}</h2>'.format(char_name)
        low_skill_counter = 0
        for group in sorted(skillset.keys()):
            groupheader_printed = False

            for skill in sorted(skillset[group]):
                skill_name, skill_id, required_level = skill

                if skill_name in trained_skills:
                    trained_level = trained_skills[skill_name]
                else:
                    trained_level = 0

                if trained_level < required_level:
                    if not groupheader_printed:
                        html += '<h3>{0}</h3>'.format(group)
                        html += '<table class="skills">'
                        groupheader_printed = True

                    html += '<tr class="lowskill">'
                    html += '<td><a class="igblink" onclick="CCPEVE.showInfo({0})">{1}</a></td>'.format(skill_id, skill_name)
                    html += '<td><img style="background:url(/static/gfx/level{1}_red.png)" src="/static/gfx/level{0}.png" alt="Level {0}/{1}" /></td>'.format(trained_level, required_level)
                    html += '</tr>'
                    low_skill_counter += 1

            if groupheader_printed:
                html += '</table>'

        if low_skill_counter == 0:
            html += '<span>Skill requirements met</span>'

        html += '</body></html>'
        return html
