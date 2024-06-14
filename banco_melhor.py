import textwrap


def menu():
    menu = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [l]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"\033[32mDepósito: R$ {valor: .2f}\n\033[0m"
        print("\n Depósito realizado!")

    else:
        print(
            "Operação Inválida!\nValor inválido, lembre-se de informar um valor positivo.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if valor > saldo:
        print(f"Operação negada por saldo insuficiente!\nSeu saldo atual é: R$ {
              saldo: .2f} ")

    elif valor > limite:
        print(
            f"Operação negada por exceder o limite!\nLembre-se: você tem um limite de R$ {limite: .2f}")

    elif numero_saques >= LIMITE_SAQUES:
        print("Operação negada por exceder o limite de saques diários!\nLembre-se: você tem um limite de 3 saques diários.")

    elif valor > 0:
        saldo -= valor
        extrato += f"\033[31mSaque: R$ {valor:.2f}\n\033[0m"
        numero_saques += 1
        print("\nSaque realizado!")

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):

    print("\n\033[1m================ EXTRATO ================\033[0m")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("\033[1m==========================================\033[0m")

    return extrato


def criar_user(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_user(cpf, usuarios)

    if usuario:
        print("Erro! Este CPF já está cadastrado.")
        return
    nome = input("Por favor, informe o nome completo: ")
    data_nascimento = input(
        "Por favor, informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Por favor, informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})

    print(" === Usuário registrado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Por favor, insira o CPF do usuário (apenas números): ")
    usuario = filtrar_user(cpf, usuarios)

    if usuario:
        print("\n === Conta criada com Sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n Usuário não encontrado, processo de criação de conta encerrado.")


def filtrar_user(cpf, usuarios):

    usuarios_encontrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]

    return usuarios_encontrados[0] if usuarios_encontrados else None


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta["agencia"]}
            C/C:\t\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}

        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():

    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe  valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                LIMITE_SAQUES=LIMITE_SAQUES,

            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_user(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
