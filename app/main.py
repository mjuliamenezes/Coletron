import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar():
    return mysql.connector.connect(
        host="db",
        user="user",
        password="senha",
        database="coletron"
    )

# ===== USUÁRIO =====
def criar_usuario():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    senha = input("Senha (6 dígitos): ")

    if len(senha) != 6:
        print("A senha deve conter 6 dígitos.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Usuario (nome, cpf, email, senha, pontos_acum) VALUES (%s, %s, %s, %s, 0)",
            (nome, cpf, email, senha)
        )
        conn.commit()
        print("Usuário cadastrado com sucesso!")
    except Error as e:
        print("Erro:", e)
    finally:
        cursor.close()
        conn.close()

def consultar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario")
        for row in cursor.fetchall():
            print(row)
    finally:
        cursor.close()
        conn.close()

def deletar_usuario():
    cpf = input("CPF do usuário a excluir: ")
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE cpf = %s", (cpf,))
        conn.commit()
        print("Usuário deletado.")
    finally:
        cursor.close()
        conn.close()

# ===== RESÍDUO =====
def criar_residuo():
    tipo = input("Tipo de resíduo (pequeno, médio, grande): ")
    pontos = int(input("Pontos atribuídos: "))
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Residuo (tipo, pontos_residuo) VALUES (%s, %s)",
            (tipo, pontos)
        )
        conn.commit()
        print("Resíduo cadastrado!")
    finally:
        cursor.close()
        conn.close()

def consultar_residuos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Residuo")
        for row in cursor.fetchall():
            print(row)
    finally:
        cursor.close()
        conn.close()

def atualizar_residuo():
    id_residuo = input("ID do resíduo: ")
    novo_tipo = input("Novo tipo: ")
    novos_pontos = input("Nova pontuação: ")
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Residuo SET tipo = %s, pontos_residuo = %s WHERE id_residuo = %s",
            (novo_tipo, novos_pontos, id_residuo)
        )
        conn.commit()
        print("Resíduo atualizado.")
    finally:
        cursor.close()
        conn.close()

def deletar_residuo():
    id_residuo = input("ID do resíduo a excluir: ")
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Residuo WHERE id_residuo = %s", (id_residuo,))
        conn.commit()
        print("Resíduo deletado.")
    finally:
        cursor.close()
        conn.close()

# ===== DESCARTE =====
def realizar_descarte():
    cpf = input("CPF do usuário: ")
    id_residuo = input("ID do resíduo: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_usuario FROM Usuario WHERE cpf = %s", (cpf,))
        usuario = cursor.fetchone()
        if not usuario:
            print("Usuário não encontrado.")
            return
        id_usuario = usuario[0]

        cursor.execute("SELECT pontos_residuo FROM Residuo WHERE id_residuo = %s", (id_residuo,))
        residuo = cursor.fetchone()
        if not residuo:
            print("Resíduo não encontrado.")
            return
        pontos = residuo[0]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO Descarte (data_hora, pontos_descarte, fk_usuario_id, fk_residuo_id) VALUES (%s, %s, %s, %s)",
            (now, pontos, id_usuario, id_residuo)
        )

        cursor.execute(
            "UPDATE Usuario SET pontos_acum = pontos_acum + %s WHERE id_usuario = %s",
            (pontos, id_usuario)
        )

        conn.commit()
        print("Descarte registrado com sucesso!")

    finally:
        cursor.close()
        conn.close()

def consultar_descartes():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nome, r.tipo, d.data_hora, d.pontos_descarte
            FROM Descarte d
            JOIN Usuario u ON d.fk_usuario_id = u.id_usuario
            JOIN Residuo r ON d.fk_residuo_id = r.id_residuo
        """)
        for row in cursor.fetchall():
            print(f"Usuário: {row[0]}, Resíduo: {row[1]}, Data: {row[2]}, Pontos: {row[3]}")
    finally:
        cursor.close()
        conn.close()

# ===== MENU =====
def menu():
    while True:
        print("\n====== MENU COLETRON ======")
        print("="*30)
        
        print("\n----- GERENCIAR USUÁRIOS -----")
        print("1. Criar usuário")
        print("2. Consultar usuários")
        print("3. Deletar usuário")
        
        print("\n----- GERENCIAR RESÍDUOS -----")
        print("4. Criar resíduo")
        print("5. Consultar resíduos")
        print("6. Atualizar resíduo")
        print("7. Deletar resíduo")
        
        print("\n---- OPERAÇÕES DE DESCARTE ----")
        print("8. Realizar descarte")
        print("9. Consultar descartes")
        
        print("\n" + "-"*30)
        opcao = input("Escolha: ")

        match opcao:
            case '1': criar_usuario()
            case '2': consultar_usuarios()
            case '3': deletar_usuario()
            case '4': criar_residuo()
            case '5': consultar_residuos()
            case '6': atualizar_residuo()
            case '7': deletar_residuo()
            case '8': realizar_descarte()
            case '9': consultar_descartes()
            case '0': break
            case _: print("Opção inválida!")

if __name__ == "__main__":
    menu()