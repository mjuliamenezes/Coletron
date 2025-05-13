import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar():
    return mysql.connector.connect(
        host='db',          # Nome do serviço no docker-compose
        port=3306,          # Porta interna do container do MySQL
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
        cursor.execute("SELECT nome, cpf, email, pontos_acum FROM Usuario")
        for row in cursor.fetchall():
            print(f"Nome: {row[0]}, CPF: {row[1]}, Email: {row[2]}, Pontos: {row[3]}")
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

def editar_usuario():
    cpf = input("Digite o CPF do usuário que deseja editar: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM Usuario WHERE cpf = %s", (cpf,))
        usuario = cursor.fetchone()
        if not usuario:
            print("Usuário não encontrado.")
            return

        print("Qual campo deseja editar?")
        print("1 - Nome")
        print("2 - CPF")
        print("3 - Email")
        print("4 - Pontos acumulados")
        print("5 - Senha")
        escolha = input("Digite o número da opção: ")

        if escolha == "1":
            novo_nome = input("Novo nome: ")
            cursor.execute("UPDATE Usuario SET nome = %s WHERE cpf = %s", (novo_nome, cpf))

        elif escolha == "2":
            novo_cpf = input("Novo CPF: ")
            cursor.execute("UPDATE Usuario SET cpf = %s WHERE cpf = %s", (novo_cpf, cpf))

        elif escolha == "3":
            novo_email = input("Novo email: ")
            cursor.execute("UPDATE Usuario SET email = %s WHERE cpf = %s", (novo_email, cpf))

        elif escolha == "4":
            novos_pontos = input("Novo valor de pontos acumulados: ")
            cursor.execute("UPDATE Usuario SET pontos_acum = %s WHERE cpf = %s", (novos_pontos, cpf))

        elif escolha == "5":
            nova_senha = input("Nova senha (6 dígitos): ")
            if len(nova_senha) != 6:
                print("A senha deve conter 6 dígitos.")
                return
            cursor.execute("UPDATE Usuario SET senha = %s WHERE cpf = %s", (nova_senha, cpf))

        else:
            print("Opção inválida.")
            return

        conn.commit()
        print("Usuário atualizado com sucesso!")

    except Error as e:
        print("Erro:", e)
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

def editar_descarte():
    id_descarte = input("ID do descarte a editar: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Buscar dados antigos do descarte
        cursor.execute("""
            SELECT d.fk_usuario_id, d.fk_residuo_id, d.pontos_descarte 
            FROM Descarte d
            WHERE d.id_descarte = %s
        """, (id_descarte,))
        descarte = cursor.fetchone()

        if not descarte:
            print("Descarte não encontrado.")
            return

        id_usuario, id_residuo_antigo, pontos_antigos = descarte

        # Novo resíduo
        id_residuo_novo = input("Novo ID do resíduo: ")

        # Buscar pontos do novo resíduo
        cursor.execute("SELECT pontos_residuo FROM Residuo WHERE id_residuo = %s", (id_residuo_novo,))
        res_novo = cursor.fetchone()
        if not res_novo:
            print("Novo resíduo não encontrado.")
            return
        pontos_novos = res_novo[0]

        # Atualizar o descarte
        cursor.execute("""
            UPDATE Descarte 
            SET fk_residuo_id = %s, pontos_descarte = %s
            WHERE id_descarte = %s
        """, (id_residuo_novo, pontos_novos, id_descarte))

        # Atualizar os pontos do usuário
        diferenca_pontos = pontos_novos - pontos_antigos
        cursor.execute("""
            UPDATE Usuario 
            SET pontos_acum = pontos_acum + %s
            WHERE id_usuario = %s
        """, (diferenca_pontos, id_usuario))

        conn.commit()
        print("Descarte atualizado com sucesso!")

    finally:
        cursor.close()
        conn.close()

def deletar_descarte():
    id_descarte = input("ID do descarte a excluir: ")

    try:
        conn = conectar()
        cursor = conn.cursor()

        # Buscar dados do descarte
        cursor.execute("""
            SELECT fk_usuario_id, pontos_descarte
            FROM Descarte
            WHERE id_descarte = %s
        """, (id_descarte,))
        descarte = cursor.fetchone()

        if not descarte:
            print("Descarte não encontrado.")
            return

        id_usuario, pontos = descarte

        # Deletar o descarte
        cursor.execute("DELETE FROM Descarte WHERE id_descarte = %s", (id_descarte,))

        # Atualizar pontos do usuário
        cursor.execute("""
            UPDATE Usuario 
            SET pontos_acum = pontos_acum - %s
            WHERE id_usuario = %s
        """, (pontos, id_usuario))

        conn.commit()
        print("Descarte deletado com sucesso!")

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
        print("4. Editar usuário")

        print("\n----- GERENCIAR RESÍDUOS -----")
        print("5. Criar resíduo")
        print("6. Consultar resíduos")
        print("7. Atualizar resíduo")
        print("8. Deletar resíduo")

        print("\n---- OPERAÇÕES DE DESCARTE ----")
        print("9. Realizar descarte")
        print("10. Consultar descartes")
        print("11. Editar descarte")
        print("12. Deletar descarte")
        print("0. Sair")

        
        print("\n" + "-"*30)
        opcao = input("Escolha: ")

        match opcao:
            case '1': criar_usuario()
            case '2': consultar_usuarios()
            case '3': deletar_usuario()
            case '4': editar_usuario()
            case '5': criar_residuo()
            case '6': consultar_residuos()
            case '7': atualizar_residuo()
            case '8': deletar_residuo()
            case '9': realizar_descarte()
            case '10': consultar_descartes()
            case '11': editar_descarte()
            case '12': deletar_descarte()
            case '0': break
            case _: print("Opção inválida!")


if __name__ == "__main__":
    menu()