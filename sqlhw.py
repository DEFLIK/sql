import pandas as pd
import sqlite3
import re

db = sqlite3.connect('works.sqlite')
data = pd.read_csv("works.csv")
curs = db.cursor()

curs.execute('DROP TABLE works')
curs.execute('CREATE TABLE works ('
                   'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
                   'salary INTEGER,'
                   'educationType TEXT,'
                   'jobTitle TEXT,'
                   'qualification TEXT,'
                   'gender TEXT,'
                   'dateModify TEXT,'
                   'skills TEXT,'
                   'otherInfo TEXT)')

regxp = lambda x: re.sub(r'<[^>]*>', '', str(x))
data['skills'] = data['skills'].apply(regxp)
data['otherInfo'] = data['otherInfo'].apply(regxp)

data.to_sql('works', db, if_exists='append', index=False)

curs.execute(
    'DROP TABLE '
    'IF EXISTS genders')
curs.execute('CREATE TABLE genders('
             'genderName TEXT PRIMARY KEY)')
curs.execute('INSERT INTO genders '
             'SELECT DISTINCT gender '
             'FROM works '
             'WHERE gender IS NOT NULL')
curs.execute('DROP TABLE '
             'IF EXISTS educations')
curs.execute('CREATE TABLE educations('
             'educationType TEXT PRIMARY KEY)')
curs.execute('INSERT INTO educations '
             'SELECT '
                 'DISTINCT educationType '
                 'FROM works '
                 'WHERE works.educationType IS NOT NULL')
curs.execute('PRAGMA foreign_keys = true')
db.commit()

curs.execute('DROP TABLE works_appended')
curs.execute('CREATE TABLE works_appended ('
               'ID INTEGER PRIMARY KEY AUTOINCREMENT,'
               'salary INTEGER,'
               'educationType TEXT REFERENCES educations(educationType) ON DELETE CASCADE ON UPDATE CASCADE,'
               'jobTitle TEXT,'
               'qualification TEXT,'
               'gender TEXT REFERENCES genders(genderName) ON DELETE CASCADE ON UPDATE CASCADE,'
               'dateModify TEXT,'
               'skills TEXT,'
               'otherInfo TEXT)')
db.commit()
curs.execute('INSERT INTO works_appended '
             'SELECT * '
             'FROM works')
curs.execute('DROP TABLE works')
curs.execute('ALTER TABLE works_appended RENAME TO works')
db.commit()