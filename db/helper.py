import sqlite3

DB_PATH = './db/todo.db'   # Update this path accordingly
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(item,status):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"insert into items(item, status, date) values('{item}','{status}',strftime('%m-%d-%Y',date('now')))")
        conn.commit()
        return {"item": item, "status": status}
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)
        status = c.fetchone()[0]
        return status
    except Exception as e:
        print('Error: ', e)
        return None

def update_status(item, status):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if c.execute(f"SELECT EXISTS (SELECT * FROM items WHERE item='{item}')"):
            c.execute(f"update items set status='{status}',date=strftime('%m-%d-%Y',date('now')) where item='{item}'")
            conn.commit()
            return {item: status}
        else:
            print('Error: Item Not Found')
            return None
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        if c.execute(f"SELECT EXISTS (SELECT * FROM items WHERE item='{item}')"):
            c.execute(f"DELETE FROM items WHERE item='{item}'")
            conn.commit()
            return {'item': item}
        else:
            print('Error: Item Not Found')
            return None
    except Exception as e:
        print('Error: ', e)
        return None
