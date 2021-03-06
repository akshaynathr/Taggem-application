import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


#database setup function

def dbSetUp():
    connection=r.connect(host='localhost',port=28015)
    try:
        r.db_create('taggem2').run(connection)
        r.db('taggem2').table_create('user').run(connection)
        r.db('taggem2').table_create('post').run(connection)
        r.db('taggem2').table('user').index_create('apiKey').run(connection)
        r.db('taggem2').table('post').index_create('apiKey').run(connection)
        r.db('taggem2').table('post').index_create('views').run(connection)
        r.db('taggem2').table_create('post').run(connection)
        print("Database setup completed")
    except RqlRuntimeError:
        print("Database running Okay")
    finally:
        connection.close()

