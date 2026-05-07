import sqlite3
from datetime import datetime


BANCO = "estoque.db"
LOG = "log_estoque.txt"


def conectar():
    return sqlite3.connect(BANCO)


def criar_tabela():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
            """
        )


def listar_produtos():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, quantidade, preco FROM produtos ORDER BY id")
        return cursor.fetchall()


def cadastrar_produto(nome, quantidade, preco):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            (nome, quantidade, preco),
        )


def atualizar_produto(produto_id, nome, quantidade, preco):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
            (nome, quantidade, preco, produto_id),
        )


def excluir_produto(produto_id):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))


def registrar_log(texto):
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{data}] {texto}\n")
