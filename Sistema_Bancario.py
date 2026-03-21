'''
Sistema Bancario: depósito, saque e extrato.

parte 1:
    depósito:
        apenas valores positivos
        armazenar o valor depositado na variavel extrato

    saque:
        limite diário de 3 saques
        500 reais por saque
        em caso de saldo insuficiente, informar ao usuário
        armazenar o valor sacado na variavel extrato

    extrato:
        listar todos os depósitos e saques realizados
        se não houver movimentações, informar ao usuário "Não foram realizadas movimentações."
        formato:
            "Depósito: R$ 1000.00"
            "Saque: R$ 500.00"

parte 2:
    criar usuário (cliente):
        lista = [{'Nome': str, 'CPF': apenas números, 'Endereço': cidade/ESTADO}]
        não podem haver CPFs repetidos

    criar conta corrente (banco):
        lista = [{'agencia': '0001', 'conta': sequencia, 'usuario': str}]

    listar contas correntes:
        listar todas as contas correntes cadastradas

parte 3:
        utilizar classes para implementar o sistema bancário
        criar métodos para cada funcionalidade        
'''

from app.models import *

usuarios = []

def criar_usuario():
    nome = input('\nNome: ').title()
    endereco = input('Endereço (Cidade/UF): ')
    cpf = input('CPF (apenas números): ')

    try:
        if not cpf.isdigit():
            raise Exception('CPF deve conter apenas números.')
        if cpf in [usuario.cpf for usuario in usuarios]:
            raise Exception('CPF já cadastrado.')
    
    except Exception as e:
        print(f"\nNão foi posível cadastrar usuário.\nERRO: {e}")
        return None
    
    else:
        usuarios.append(Usuario(nome, cpf, endereco))
    

def criar_conta():
    print("\nSelecione um usuário:")
    for i, usuario in enumerate(usuarios):
        print(f"({i}) {usuario}")

    try:
        indice = int(input("\nOpção: "))
        if indice not in range(len(usuarios)):
            raise Exception()
        
    except Exception:
        print('\nOpção inválida.')
        return None

    else:
        usuarios[indice].criar_conta_corrente()


def listar_contas_correntes():
    for conta in contas:
        print(conta)


def selecionar_conta_corrente():
    nome = input('\nBucar por nome do usuário: ').title()
    
    if nome not in [usuario.nome for usuario in usuarios]:
        print('\nUsuário não cadastrado.')
        return None
    
    else:
        for usuario in usuarios:
            if usuario.nome == nome:
                cliente = usuario
                break
        
        if not cliente.contas:
            print("O cliente não possui contas correntes.")
            return False

        else:
            cliente.listar_contas()
            
            try:
                cod_conta = input('\nSelecione a conta: ')
                if not cod_conta.isdigit():
                    raise Exception()
                if int(cod_conta) < 0 or int(cod_conta) >= len(cliente.contas):
                    raise Exception()

            except Exception:
                print('\nOpção inválida.')
                
            else:
                return cliente.contas[int(cod_conta)]


def deposito(conta):
    try:
        valor = float(input('\nValor do depósito: R$ ').replace(',', '.'))
    
    except ValueError:
        print('\nValor inválido.')
        return None
        
    else:
        if valor > 0:
            conta.depositar(valor)

        else:
            print('\nValor inválido.')


def saque(conta:dict):
    try:
        valor = float(input('\nValor do saque: R$ ').replace(',', '.'))
    
    except ValueError:
        print('\nValor inválido.')
        return None

    else:
        if valor > 0:
            if conta.sacar(valor):
                print('\nSaque realizado com sucesso.')
            
        else:
            print('\nValor inválido.')
   