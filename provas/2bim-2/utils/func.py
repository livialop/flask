from flask import * 

import sqlite3

def get_connection():
    '''Função para realizar a conexão com o banco de dados'''
    conn = sqlite3.connect('jogo.db')
    conn.row_factory = sqlite3.Row
    return conn 

def close_connection():
    '''Função para fechar a conexão com o banco de dados'''
    conn = get_connection()
    conn.close()
