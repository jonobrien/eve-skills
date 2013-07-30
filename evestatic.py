# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""evestatic.py: """

import sqlite3


class StaticDB(object):
    def __init__(self):
        self._connection = sqlite3.connect('evestatic.db')
        self._cursor = self._connection.cursor()

    def __del__(self):
        self._connection.close()

    def getSkillName(self, skillID):
        self._cursor.execute("SELECT typeName"
                             " FROM invtypes WHERE typeID = :id",
                             {'id': skillID})
        result = self._cursor.fetchone()
        return result[0]

    def getSkillGroup(self, skillID):
        self._cursor.execute("SELECT g.marketGroupName"
                             " FROM invtypes t"
                             " JOIN invmarketgroups g"
                             " ON t.marketGroupID = g.marketGroupID"
                             " WHERE t.typeID = :id",
                             {'id': skillID})
        result = self._cursor.fetchone()
        return result[0]