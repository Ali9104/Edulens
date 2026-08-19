import os
import sqlite3

def get_connection():
    base = os.path.dirname(__file__) 
    chemin = os.path.join(base, '..', 'web', 'instance',  'edulens.db')
    conn = sqlite3.connect(chemin)
    return conn
