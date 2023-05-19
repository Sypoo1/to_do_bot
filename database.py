import psycopg2
from cfg import database_Password

conn = psycopg2.connect(database="to_do_bot", user="postgres",
                        password=database_Password, host="localhost", port="5432")

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
    
    
if __name__ == '__main__':
    # create_table_tasks()
    pass
