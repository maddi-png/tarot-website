import sqlite3
from sqlite3 import Error

from flask import Flask, render_template, request

app = Flask(__name__)
DATABASE = "tarot.db"


def create_connection(db_file):
    """
    yeah"""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_home():
    return render_template("index.html", types=get_types())

@app.route('/cards/<arcana>')
def render_webpage(arcana):
    title = arcana.title()
    query = "SELECT name, number FROM cards WHERE arcana=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # query the database
    cur.execute(query, (title,))
    card_list = cur.fetchall()
    con.close()
    print(card_list)
    return render_template('cards.html', cards=card_list, title=title)


def get_cards(arcana):
    title = arcana.upper()
    query = "SELECT name, number FROM cards WHERE arcana=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # query db
    cur.execute(query, (title,))
    card_list = cur.fetchall()
    con.close()
    print(card_list)
    return card_list


def get_types():
    con = create_connection(DATABASE)
    cur = con.cursor()
    query = "SELECT DISTINCT arcana FROM cards"
    records = cur.fetchall()
    print(records)
    for i in range(len(records)):
        records[i] = records[i][0]
    print(records)
    return records


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT name, number FROM cards WHERE name LIKE ? OR number LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    card_list = cur.fetchall()
    con.close()

    return render_template("cards.html", cards=card_list, title=title, types=get_types()
                          )


@app.route('/sort/<title>')
def render_sortpage(title):
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')
    new_order = "desc" if order == "asc" else "asc"
    if sort == "name" and title == "Minor":
        sort = "suit"
    query = f'SELECT name, number FROM cards WHERE arcana=? ORDER BY {sort} {order}'
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (title,))
    card_list = cur.fetchall()
    print(card_list)
    con.close()

    return render_template('cards.html', cards=card_list, title=title,
                           types=get_types(), order=new_order)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
