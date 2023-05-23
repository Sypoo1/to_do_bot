import psycopg2


from cfg import bd_pass


conn = psycopg2.connect(database="to_do_bot", user="postgres",
                        password=bd_pass, host="localhost", port="5432")

cursor = conn.cursor()


def create_table_tasks():
    cursor.execute('CREATE TABLE tasks(id serial primary key,\
        name varchar(1024), date varchar(1024), completed boolean);')
    conn.commit()
    
def create_table_hide():
    cursor.execute('CREATE TABLE hide (id integer primary key);')
    conn.commit()

def insert_into_tasks(msg):
    name = msg[0]
    date = msg[1]
    complete = False
    cursor.execute(f"INSERT INTO tasks (name, date, completed)\
        VALUES ('{name}', '{date}', {complete});")
    conn.commit()
    
def insert_into_hide(id):
    cursor.execute(f'INSERT INTO hide VALUES ({id});')
    conn.commit()

def get_tasks():
        cursor.execute('select * from tasks where\
            id NOT IN (SELECT id FROM hide WHERE id IS NOT NULL );')
        records = list(cursor.fetchall())
        return records

def get_tasks_boolean(bol):
    cursor.execute(f'select * from tasks where completed={bol} and\
        id NOT IN (SELECT id FROM hide WHERE id IS NOT NULL );')

    records = list(cursor.fetchall())
    return records

def get_by_id(id):
    cursor.execute(f'select * from tasks where id={id} and\
        id NOT IN (SELECT id FROM hide WHERE id IS NOT NULL );')
    records = list(cursor.fetchall())
    return records

    
def complete_task(id):
     cursor.execute(f'update tasks set completed=true where id={id};')
     conn.commit()
     
     
if __name__ == '__main__':
    # create_table_tasks()
    # create_table_hide()
    pass
