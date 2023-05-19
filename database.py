import psycopg2


conn = psycopg2.connect(database="to_do_bot", user="postgres",
                        password='cool1234', host="localhost", port="5432")

cursor = conn.cursor()

              

def create_table_tasks():
    cursor.execute('CREATE TABLE tasks(id serial primary key, name varchar(1024), date varchar(1024), completed boolean);')
    conn.commit()
    

def insert_into_tasks(msg):
    name = msg[0]
    date = msg[1]
    complete = False
    cursor.execute(f"INSERT INTO tasks (name, date, completed) VALUES ('{name}', '{date}', {complete});")
    conn.commit()
 
    
def get_tasks():
        cursor.execute('select * from tasks;')
        records = list(cursor.fetchall())
        return records

def get_tasks_boolean(bol):
    cursor.execute(f'select * from tasks where completed={bol};')
    conn.commit()
    records = list(cursor.fetchall())
    return records
    
def delete_task(id):
     cursor.execute(f'delete from tasks where id={id}')
     conn.commit()
    
def complete_task(id):
     cursor.execute(f'update tasks set completed=true where id={id};')
     conn.commit()
if __name__ == '__main__':
    # create_table_tasks()
    pass
