import sqlite3 as sql
import os

caminho = os.path.join(os.path.dirname(__file__), 'bdsqlite.db')
conexao = sql.connect(caminho)
cursor = conexao.cursor()

# CREATE
def criar_cliente():
    nome = input("Nome: ")
    instagram = input("Instagram: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    cursor.execute(
        "INSERT INTO clientes (nome, instagram, telefone, email) VALUES (?,?,?,?)",
        (nome, instagram, telefone, email)
    )
    conexao.commit()
    print("✅ Cliente cadastrado!")

# READ
def listar_clientes():
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n📋 Lista de clientes:")
    for c in clientes:
        print(c)

# UPDATE
def atualizar_cliente():
    id_cliente = int(input("ID do cliente: "))
    novo_nome = input("Novo nome: ")

    cursor.execute(
        "UPDATE clientes SET nome = ? WHERE id_cliente = ?",
        (novo_nome, id_cliente)
    )
    conexao.commit()
    print("✏️ Cliente atualizado!")

# DELETE
def deletar_cliente():
    id_cliente = int(input("ID do cliente: "))

    cursor.execute(
        "DELETE FROM clientes WHERE id_cliente = ?",
        (id_cliente,)
    )
    conexao.commit()
    print("🗑️ Cliente deletado!")

# MENU
def menu():
    while True:
        print("\n=== MENU ===")
        print("1 - Criar cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Deletar cliente")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            criar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            atualizar_cliente()
        elif opcao == "4":
            deletar_cliente()
        elif opcao == "0":
            break
        else:
            print("❌ Opção inválida!")

menu()

conexao.close()