import sqlite3

# Database Tutorial
MY_DB_PATH = './db/todo.db'   # Update this path accordingly
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(item,status):
    try:
        conn = sqlite3.connect(MY_DB_PATH)
        c = conn.cursor()
        c.execute(f"insert into items(item, status, date) values('{item}','{status}',strftime('%m-%d-%Y',date('now')))")
        conn.commit()
        return {"item": item, "status": status}
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items():
    try:
        conn = sqlite3.connect(MY_DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item):
    try:
        conn = sqlite3.connect(MY_DB_PATH)
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)
        status = c.fetchone()[0]
        return status
    except Exception as e:
        print('Error: ', e)
        return None

def update_status(item, status):
    try:
        conn = sqlite3.connect(MY_DB_PATH)
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
        conn = sqlite3.connect(MY_DB_PATH)
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


#API Tutorial
BOOK_PATH = './db/books.db'
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def api_all():
    conn = sqlite3.connect(BOOK_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return all_books


def api_filter(id=None,published=None,author=None):
    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)

    query = query[:-4] + ';'

    conn = sqlite3.connect(BOOK_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return results

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]
