import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

db = sqlite3.connect('works.sqlite')
curs = db.cursor()

curs.execute('DROP TABLE IF EXISTS works')
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

data = pd.read_csv('works.csv')
data.to_sql('works', db, if_exists='append', index=False)
curs.execute('CREATE INDEX salary_index '
                 'ON works (salary)')
db.commit()

curs.execute('SELECT COUNT(*) '
             'FROM works')
print('#3-------------------')
print(curs.fetchall()[0][0])


curs.execute('SELECT gender, COUNT(*) '
             'FROM works '
             'GROUP BY works.gender')
print('#4------------------')
print(curs.fetchall())


curs.execute('SELECT count(*) '
             'FROM works '
             'WHERE works.skills IS NOT NULL')
print('#5-------------------')
print(curs.fetchall()[0][0])

curs.execute("SELECT * "
             "FROM works "
             "WHERE works.skills IS NOT NULL")
print('#6-------------------')
print(curs.fetchall())

curs.execute('SELECT salary '
             'FROM works '
             'WHERE skills LIKE "%Python%"')
print('#7-------------------')
print(curs.fetchall())

curs.execute('SELECT salary '
             'FROM works '
             'WHERE gender = "Мужской"')
man_sal = [x[0] for x in curs.fetchall()]
m_quantile = np.quantile(man_sal, np.linspace(0.1, 1, 10))
plt.hist(m_quantile, 100)
plt.show()

curs.execute('SELECT salary '
             'FROM works '
             'WHERE gender = "Женский"')
woman_sal = [x[0] for x in curs.fetchall()]
w_quantile = np.quantile(woman_sal, np.linspace(0.1, 1, 10))
plt.hist(w_quantile, 100)
plt.show()
