# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""charsheet.py: """

from sys import argv
import eveapi_simple as api
from evestatic import StaticDB


api_args = {'keyID': argv[1], 'vCode': argv[2]}

characters = []
key_info = api.query('/account/APIKeyInfo', api_args)
for character in key_info.result.key.rowset.row:
    char_id = character.attrib['characterID']
    char_name = character.attrib['characterName']
    characters.append((char_id, char_name))

print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('<title>API key info</title>')
print('<link rel="stylesheet" type="text/css" href="style.css" />')
print('</head>')
print('<body>')

sdb = StaticDB()
for character in characters:
    char_id, char_name = character
    api_args['characterID'] = char_id
    charsheet = api.query('/char/CharacterSheet', api_args)
    skills = {}
    for skill in charsheet.xpath("result/rowset[@name='skills']/row"):
        skill_id = int(skill.attrib['typeID'])
        skill_level = int(skill.attrib['level'])
        skill_name = sdb.skill_name(skill_id)
        skill_group = sdb.skill_group(skill_id)
        if skill_group not in skills:
            skills[skill_group] = []
        skills[skill_group].append((skill_name, skill_id, skill_level))

    print('<h2>%s</h2>' % char_name)
    for group in sorted(skills.keys()):
        print('<h3>%s</h3>' % group)
        print('<table class="skills">')
        for skill in sorted(skills[group]):
            skill_name, skill_id, skill_level = skill
            print('<tr>')
            print('<td>' if skill_level < 5 else '<td class="l5skill">')
            print('<a class="igblink" onclick="CCPEVE.showInfo(%s)">%s</a>'
                  '</td>' % (skill_id, skill_name))
            print('<td><img src="gfx/level%s.png" alt="Level %s" /></td>'
                  % (skill_level, skill_level))
            print('</tr>')
        print('</table>')

print('</body>')
print('</html>')