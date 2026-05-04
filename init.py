import sqlite3 as sql


con = sql.connect('banco.db')
cur = con.cursor()
cur.execute('''
            create table if not exists usuarios(
            id      integer primary key autoincrement,
            nome    text not null,
            email   text not null unique,
            senha   text not null
)
''')

con.commit()
con.close()
print('Banco criado com sucesso')
