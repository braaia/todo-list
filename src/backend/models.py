import sqlite3
from typing import List
from .schemas import ClienteOut

def get_conn():
    return sqlite3.connect("clientes.db")

def criar_cliente(nome: str, email: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return ClienteOut(id=cid, nome=nome, email=email)

def listar_clientes():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    return [ClienteOut(id=x[0], nome=x[1], email=x[2]) for x in rows]

def atualizar_cliente(id: int, nome: str, email: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", (nome, email, id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def deletar_cliente(id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
