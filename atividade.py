import json
import os

ARQUIVO = "alunos.json"

# -----------------------
# PERSISTÊNCIA (IMPERATIVO)
# -----------------------

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(alunos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(alunos, f, indent=4, ensure_ascii=False)


# -----------------------
# FUNÇÕES PURAS (FUNCIONAL)
# -----------------------

def criar_aluno(lista, aluno):
    return lista + [aluno]


def existe_aluno(lista, aluno_id):
    return any(a["id"] == aluno_id for a in lista)


def atualizar_aluno(lista, aluno_id, nome, idade):
    return list(map(
        lambda a: {"id": a["id"], "nome": nome, "idade": idade}
        if a["id"] == aluno_id else a,
        lista
    ))


def deletar_aluno(lista, aluno_id):
    return list(filter(lambda a: a["id"] != aluno_id, lista))


# -----------------------
# VALIDAÇÃO (IMPERATIVO)
# -----------------------

def ler_int(msg):
    while True:
        v = input(msg)
        try:
            n = int(v)
            if n > 0:
                return n
            print("O número deve ser maior que 0.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_nome(msg):
    while True:
        nome = input(msg).strip()

        if not nome:
            print("Nome não pode ser vazio.")
        elif any(c.isdigit() for c in nome):
            print("Nome não pode conter números.")
        else:
            return nome


# -----------------------
# APRESENTAÇÃO (UI)
# -----------------------

def listar_formatado(alunos):
    if not alunos:
        print("\n📭 Nenhum aluno cadastrado.\n")
        return

    print("\n📚 LISTA DE ALUNOS\n" + "-" * 30)

    for a in alunos:
        print(f"🆔 ID: {a['id']}")
        print(f"👤 Nome: {a['nome']}")
        print(f"🎂 Idade: {a['idade']}")
        print("-" * 30)


def buscar_formatado(alunos, aluno_id):
    resultado = list(filter(lambda a: a["id"] == aluno_id, alunos))

    if not resultado:
        print("\n❌ Aluno não encontrado.\n")
        return

    a = resultado[0]

    print("\n🔎 ALUNO ENCONTRADO\n" + "-" * 30)
    print(f"🆔 ID: {a['id']}")
    print(f"👤 Nome: {a['nome']}")
    print(f"🎂 Idade: {a['idade']}")
    print("-" * 30)


# -----------------------
# MAIN (IMPERATIVO)
# -----------------------

def main():
    alunos = carregar_dados()

    contador_id = max([a["id"] for a in alunos], default=0) + 1

    while True:
        print("\n=== MENU ===")
        print("1 - Criar aluno")
        print("2 - Listar alunos")
        print("3 - Buscar aluno")
        print("4 - Atualizar aluno")
        print("5 - Deletar aluno")
        print("0 - Sair")

        op = input("Escolha: ")

        # CREATE
        if op == "1":
            nome = ler_nome("Nome: ")
            idade = ler_int("Idade: ")

            aluno = {"id": contador_id, "nome": nome, "idade": idade}
            alunos = criar_aluno(alunos, aluno)
            contador_id += 1

            salvar_dados(alunos)
            print("Aluno criado com sucesso.")

        # READ ALL
        elif op == "2":
            listar_formatado(alunos)

        # READ ONE
        elif op == "3":
            id_busca = ler_int("ID: ")
            buscar_formatado(alunos, id_busca)

        # UPDATE
        elif op == "4":
            id_up = ler_int("ID: ")

            if not existe_aluno(alunos, id_up):
                print("Aluno não existe.")
            else:
                nome = ler_nome("Novo nome: ")
                idade = ler_int("Nova idade: ")

                alunos = atualizar_aluno(alunos, id_up, nome, idade)
                salvar_dados(alunos)

                print("Aluno atualizado com sucesso.")

        # DELETE
        elif op == "5":
            id_del = ler_int("ID: ")

            if not existe_aluno(alunos, id_del):
                print("Aluno não existe.")
            else:
                alunos = deletar_aluno(alunos, id_del)
                salvar_dados(alunos)

                print("Aluno removido com sucesso.")

        # EXIT
        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()