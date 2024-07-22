from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error


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

@app.route('/cards/<suit>')
def render_webpage(suit):
    title = suit.upper()
    query = "SELECT name, number FROM cards WHERE suit=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # query the database
    cur.execute(query, (title,))
    card_list = cur.fetchall()
    con.close()
    print(card_list)
    return render_template('cards.html', cards=card_list, title=title)


def get_cards(suit):
    title = suit.upper()
    query = "SELECT name, number FROM cards WHERE suit=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # query db
    cur.execute(query, (title,))
    tag_list = cur.fetchall()
    con.close()
    print(tag_list)
    return tag_list


def get_types():
    con = create_connection(DATABASE)
    cur = con.cursor()
    query = "SELECT DISTINCT type FROM cards"
    records = cur.fetchall()
    print(records)
    for i in range(len(records)):
        records[i] = records[i][0]
    print(records)
    return records


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
