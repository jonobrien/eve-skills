# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""skillcheck.py: """

from sys import argv
import csv
import eveapi_simple as api
from evestatic import StaticDB


sdb = StaticDB()

skillset_name = argv[1]
skillset = {}
with open(skillset_name + '.csv', 'rb') as csvfile:
    skillsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in skillsreader:
        skill_name, required_level = row
        skill_id = sdb.skill_id(skill_name)
        skill_group = sdb.skill_group(skill_id)
        if skill_group not in skillset:
            skillset[skill_group] = []
        skillset[skill_group].append((skill_name, skill_id, required_level))

api_args = {'keyID': argv[2], 'vCode': argv[3]}

characters = []
key_info = api.query('/account/APIKeyInfo', api_args)
for character in key_info.result.key.rowset.row:
    char_id = character.attrib['characterID']
    char_name = character.attrib['characterName']
    characters.append((char_id, char_name))

print('<!DOCTYPE html>')
print('<html>')
print('<head>')
print('<title>Skill check</title>')
print('<link rel="stylesheet" type="text/css" href="style.css" />')
print('</head>')
print('<body>')

for character in characters:
    char_id, char_name = character
    api_args['characterID'] = char_id
    charsheet = api.query('/char/CharacterSheet', api_args)
    trained_skills = {}
    for skill in charsheet.xpath("result/rowset[@name='skills']/row"):
        skill_id = int(skill.attrib['typeID'])
        required_level = int(skill.attrib['level'])
        skill_name = sdb.skill_name(skill_id)
        trained_skills[skill_name] = required_level

    print('<h2>%s</h2>' % char_name)
    for group in sorted(skillset.keys()):
        print('<h3>%s</h3>' % group)
        print('<table class="skills">')

        for skill in sorted(skillset[group]):
            skill_name, skill_id, required_level = skill

            if skill_name in trained_skills:
                trained_level = trained_skills[skill_name]
            else:
                trained_level = 0

            if trained_level < required_level:
                print('<tr class="lowskill">')
                print('<td><a class="igblink" onclick="CCPEVE.showInfo(%s)">%s'
                      '</a></td>' % (skill_id, skill_name))
                print('<td><img style="background:url(gfx/level{1}_red.png)"'
                      ' src="gfx/level{0}.png"'
                      ' alt="Level {0}/{1}" /></td>'.format(trained_level,
                                                            required_level))
                print('</tr>')

        print('</table>')

print('</body>')
print('</html>')