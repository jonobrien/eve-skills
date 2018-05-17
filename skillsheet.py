# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""charsheet.py: """

from flask.views import MethodView
import eveapi_simple as api
from evestatic import StaticDB


###api_args = {'keyID': argv[1], 'vCode': argv[2]}
class CharSheet(MethodView):
    def get(self):
        characters = []
        client = api.ESIClient()
        characters = api.get_character(client)  # [(id, name)]


        html = '<!DOCTYPE html>'
        html += '<html>'
        html +='<head>'
        html +='<title>API key info</title>'
        html +='<link rel="stylesheet" type="text/css" href="style.css" />'
        html +='</head>'
        html +='<body>'


        html += 'asdasdasdasdasdas'
        html +='</body>'
        html +='</html>'
        return html
        sdb = StaticDB()
        for character in characters:
            char_id, char_name = character
            api_args['characterID'] = char_id
            charsheet = api.get_skills(client)




            skills = {}
            for skill in charsheet.xpath("result/rowset[@name='skills']/row"):
                skill_id = int(skill.attrib['typeID'])
                skill_level = int(skill.attrib['level'])
                skill_name = sdb.skill_name(skill_id)
                skill_group = sdb.skill_group(skill_id)
                if skill_group not in skills:
                    skills[skill_group] = []
                skills[skill_group].append((skill_name, skill_id, skill_level))

            html +='<h2>%s</h2>' % char_name
            for group in sorted(skills.keys()):
                html +='<h3>%s</h3>' % group
                html +='<table class="skills">'
                for skill in sorted(skills[group]):
                    skill_name, skill_id, skill_level = skill
                    html +='<tr>'
                    html +='<td>' if skill_level < 5 else '<td class="l5skill">'
                    html +='<a class="igblink" onclick="CCPEVE.showInfo(%s)">%s</a></td>' % (skill_id, skill_name)
                    html +='<td><img src="gfx/level%s.png" alt="Level %s" /></td>' % (skill_level, skill_level)
                    html +='</tr>'
                html +='</table>'

        html +='</body>'
        html +='</html>'
        return html
