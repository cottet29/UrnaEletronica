import sqlite3
import pandas as pd
import statistics

banco = sqlite3.connect('Urnas.db')  #Criação da conexão com banco de dados (se não existir, o mesmo se cria sozinho)
cursor = banco.cursor()  #Criado para executar comandos dentro do banco de dados3
cursor.execute('''CREATE TABLE IF NOT EXISTS presidente(nome text,num primary key,partido text, votos int)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS governador(nome text,num primary key,partido text, votos int)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS prefeito(nome text,num primary key,partido text, votos int)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS eleitores(nome text,cpf text, votou int)''')
#Com cursor criado, é executado comandos dentro do banco de dados para criar as tabelas que não existem

def preencher(): #Inserção de valores dentro do banco de dados para testes
    cursorr = banco.cursor()
    cursorr.execute(f'''INSERT INTO presidente VALUES ("Bolsonaro", "22", "pl", '0')''')
    cursorr.execute(f'''INSERT INTO presidente VALUES ("Lula", "13", "pt", '0')''')
    cursorr.execute(f'''INSERT INTO presidente VALUES ("NULO", "-1", null, '0')''')
    cursorr.execute(f'''INSERT INTO presidente VALUES ("BRANCO", "-2", null, '0')''')
    cursorr.execute(f'''INSERT INTO governador VALUES ("tarcisio", "10", "pl", '0')''')
    cursorr.execute(f'''INSERT INTO governador VALUES ("haddad", "13", "pt", '0')''')
    cursorr.execute(f'''INSERT INTO governador VALUES ("NULO", "-1", null, '0')''')
    cursorr.execute(f'''INSERT INTO governador VALUES ("BRANCO", "-2", null, '0')''')
    cursorr.execute(f'''INSERT INTO prefeito VALUES ("prefeito1", "10", "pl", '0')''')
    cursorr.execute(f'''INSERT INTO prefeito VALUES ("prefeito2", "13", "pt", '0')''')
    cursorr.execute(f'''INSERT INTO prefeito VALUES ("NULO", "-1", null, '0')''')
    cursorr.execute(f'''INSERT INTO prefeito VALUES ("BRANCO", "-2", null, '0')''')
    cursorr.execute(f'''INSERT INTO eleitores VALUES ("luiza quina", "123.123.123-22", '0')''')
    cursorr.execute(f'''INSERT INTO eleitores VALUES ("lucas cottet", "123.123.123-22", '0')''')
    banco.commit()  #Salvar banco de dados apos alguma alteração
    banco.close()  #encerrar conexão do banco de dados
#INSERT INTO 'tabela' VALUES '(dados de preenchimento)'

def cadastrar_cand(): #cadastramento dos candidatos manualmente
    nome = input("Nome: ").lower()
    num = input("Numero: ").lower()
    partido = input("Partido: ").lower()
    cargo = input("Cargo: ").lower()
    if cargo == 'presidente':
        try:  # estruturo de erro pra conectar ao banco de dados
            bancodb = sqlite3.connect('Urnas.db')
            cursorr = bancodb.cursor()
            cursorr.execute(f'''INSERT INTO presidente VALUES ("{nome}", "{num}", "{partido}", '0')''')
            bancodb.commit()
            bancodb.close()
        except Exception as e:  # retorna o erro printando o motivo
            print(f'erro {e}')
    elif cargo == 'governador':
        try:
            bancodb = sqlite3.connect('Urnas.db')
            cursorr = bancodb.cursor()
            cursorr.execute(f'''INSERT INTO governador VALUES ("{nome}", "{num}", "{partido}", '0')''')
            bancodb.commit()
            bancodb.close()
        except Exception as e:
            print(f'erro {e}')
    elif cargo == 'prefeito':
        try:
            bancodb = sqlite3.connect('Urnas.db')
            cursorr = bancodb.cursor()
            cursorr.execute(f'''INSERT INTO prefeito VALUES ("{nome}", "{num}", "{partido}", '0')''')
            bancodb.commit()
            bancodb.close()
        except Exception as e:
            print(f'erro {e}')
    else:
        print("digite um cargo existente (presidente, prefeito, governador")
        cadastrar_cand()
    resp = input('deseja cadastras mais um?')
    if resp in ('s', 'sim'):
        cadastrar_cand()


def cadastrar_eleit(): #Cadastramento dos eleitores manualmente
    nome = input("Nome e sobrenome: ").lower()
    cpf = input("CPF: ").lower()
    try:
        bancodb = sqlite3.connect('Urnas.db')
        cursorr = bancodb.cursor()
        cursorr.execute(f'''INSERT INTO eleitores VALUES ("{nome}", "{cpf}", '{0}')''')
        bancodb.commit()
        bancodb.close()
        print("eleitor cadastrado")
    except Exception as e:
        print(f'erro {e}')
    resp = input('deseja cadastras mais um?')
    if resp in ('s', 'sim'):
        cadastrar_eleit()


def salvar_voto(voto, cargo): #Voto, numero do candidato digitado pelo eleitor
    bancodb = sqlite3.connect('Urnas.db')
    cursorr = bancodb.cursor()
    cursorr.execute(f'''SELECT * from {cargo} WHERE num = '{voto}' ''') #SELECT * seleciona tudo da tabela que voce desejar e WHERE é uma condição para o SELECT
    nome, num, partido, votos = cursorr.fetchall()[0]  #retorna a linha do SELECT em forma de lista
    cursorr.execute(f'''UPDATE {cargo} SET votos= '{int(votos) + 1}' WHERE num='{voto}' ''')  #UPDATE para alterar o valor de algo na tabela
    bancodb.commit()
    bancodb.close()


def votar():
    if verificar_eleitor():  #verificação se eleitor está cadastrado para poder votar
        for cargo in ('prefeito', 'governador', 'presidente'): #responsavel por organizar a ordem de votação, primeiro para prefeito e assim por diante
            bancodb = sqlite3.connect('Urnas.db')
            lista_final = pd.read_sql(f'SELECT * from {cargo}', bancodb) #Usado PANDAS (pd.) para ler o banco de dados dos candidatos e mostrar uma tabela organizada dos candidatos disponiveis
            nulo = lista_final[lista_final['nome'] == 'NULO']  #remoção do Branco e do Nulo na tabela do PANDAS, para que nao fique como um candidato.
            lista_final.drop(nulo.index, axis=0, inplace=True)  #remoção do Branco e do Nulo na tabela do PANDAS, para que nao fique como um candidato.
            branco = lista_final[lista_final['nome'] == 'BRANCO']  #remoção do Branco e do Nulo na tabela do PANDAS, para que nao fique como um candidato.
            lista_final.drop(branco.index, axis=0, inplace=True)  #remoção do Branco e do Nulo na tabela do PANDAS, para que nao fique como um candidato.
            print("\n     CANDIDATOS   \n")
            print(lista_final[['nome', 'num', 'partido']])
            print(f'\nVOTACAO PARA {cargo}')
            print('''Voto nulo digitar -1 e voto branco -2''')
            voto = input(f'Qual voto para {cargo.upper()}: ')
            if voto == '-1':
                print('votou nulo')
            elif voto == '-2':
                print('votou em branco')
            else:  #Nao utilizou -1 ou -2, entrar no num do partido que a pessoa votou (caso digite numero inexistente programa crasha)
                bancodb = sqlite3.connect('Urnas.db')
                cursorr = bancodb.cursor()
                cursorr.execute(f'''SELECT * from {cargo} WHERE num = '{voto}' ''')  #SELECT feito para mostrar qual candidato e seu partido foi selecionado
                nome, num, partido, votos = cursorr.fetchall()[0]
                bancodb.close()
                print(f'Voce selecionou {num} esta votando em {nome}, {partido}')

            resp = input('COMFIRMAR? ')
            if resp in ('nao', 'n'):
                votar()
            elif resp in ('sim', 's'):
                salvar_voto(voto, cargo)
                print('VOTO CONFIRMADO')
                print('*'*15)
    else:
        main()


def resultados():
    print("RESULTADO DAS URNAS")
    for cargo in ('prefeito', 'governador', 'presidente'):
        bancodb = sqlite3.connect('Urnas.db')
        lista_final = pd.read_sql(f'SELECT * from {cargo}', bancodb)
        lista_final = lista_final.sort_values(by='votos', ascending=False)  #.sort_value responsavel por colocar em ordem crescende ou descrescente (ascending) de acordo com o by (coluna na tabela)
        total = lista_final['votos'].sum()
        lista_final["Porcentagem de votos"] = lista_final['votos']*(100/total)
        lista_final.drop(["num"], axis=1, inplace=True)  #.drop responsavel por remover o num do candidato
        nulo = lista_final[lista_final['nome'] == 'NULO']
        lista_final.drop(nulo.index, axis=0, inplace=True)
        branco = lista_final[lista_final['nome'] == 'BRANCO']
        lista_final.drop(branco.index, axis=0, inplace=True)
        print(f'{"*"*50}{cargo.upper()}{"*"*50}\n')
        print(lista_final)
        print(f'''
TOTAL DE VOTOS: {total}
TOTAL DE VOTOS VALIDOS e %: {lista_final['votos'].sum()}--{(lista_final['votos'].sum()*100)/total :.1f}%
TOTAL DE VOTOS EM BRANCO e %: {nulo['votos'].values[0]}--{nulo['Porcentagem de votos'].values[0]:.1f}%
TOTAL DE VOTOS NULOS: {branco['votos'].values[0]}--{branco['Porcentagem de votos'].values[0]:.1f}%
    ''')


def verificar_eleitor():  #verificar se o eleitor está cadastrado de acordo com seu nome e sobrenome
    resp = input('Voce esta cadastradado?: ')
    if resp in ('sim', 's'):
        nome = input('digite seu nome e sobrenome: ')
        bancodb = sqlite3.connect('Urnas.db')
        lista = pd.read_sql('SELECT * from eleitores', bancodb)
        listaNomes = lista['nome'].values
        if nome in listaNomes:  #Se o nome digitado estiver cadastrado no banco de dados, retorna TRUE e pode votar
            print('*'*50)
            print(f'Nome encontrado, pode votar')
            return True
        else:
            print('Nome nao encontrado, digite novamente ou se cadastre')
            return False


def relatorio():
    bancodb = sqlite3.connect('Urnas.db')
    lista = pd.read_sql(f'SELECT * from eleitores', bancodb)
    lista_presidente = pd.read_sql(f'SELECT * from presidente', bancodb)
    listaNomes = lista['nome'].values
    print(f'lista de nomes que votaram: {sorted(listaNomes)}') #listagem dos nomes dos eleitores da lista em ordem albabetica
    total_pessoas = len(listaNomes)
    total = lista_presidente['votos'].sum()
    if total == total_pessoas:  #Total de pessoas comparado com total de votos no presidente (branco e nulo entram tmb) e verificado se são iguais
        print(f'Total de votos {total}')
        print(f'Total de pessoas que votaram {total_pessoas}')
    lista_de_partidos = []
    for i in ('prefeito', 'governador', 'presidente'):  #Gera lista_de_partidos com os canditados que venceram em cada cargo
        bancodb = sqlite3.connect('Urnas.db')
        lista_final = pd.read_sql(f'SELECT * from {i}', bancodb)
        lista_final = lista_final.sort_values(by='votos', ascending=False)
        nulo = lista_final[lista_final['nome'] == 'NULO']
        lista_final.drop(nulo.index, axis=0, inplace=True)
        branco = lista_final[lista_final['nome'] == 'BRANCO']
        lista_final.drop(branco.index, axis=0, inplace=True)
        nome = lista_final['nome'].values[0]
        partido = lista_final[lista_final['nome'] == nome]
        lista_de_partidos.append(partido['partido'].values[0].upper())  #Adcionar na lista o partido dos 3 ganhadores que foi criada (lista de partidos)
    moda = statistics.mode(lista_de_partidos)  #Pega o partido que mais se repetiu na lista
    print(f'O partido mais elegeu foi o {moda}')
    for i in range(0, lista_de_partidos.count(moda)):  #Remoção do que menos se repetiu para dizer qual o que menos foi elegido
        lista_de_partidos.remove(moda)
    print(f'O partido que menos elegeu foi o {lista_de_partidos}')


def main():
    print("""
1. Cadastrar Candidatos
2. Cadastrar Eleitores
3. Votar
4. Apurar Resultados
5. Relatório e Estatísticas
6. Encerrar
""")
    opt = int(input("Input: "))
    if opt == 1:
        cadastrar_cand()
        main()
    elif opt == 2:
        cadastrar_eleit()
        main()
    elif opt == 3:
        votar()
        main()
    elif opt == 4:
        resultados()
        main()
    elif opt == 5:
        relatorio()
        main()

    elif opt == 6:
        print('Até breve!')
    elif opt == 666:  #Criação para preenchimento automatico do banco de dados.
        preencher()
        print('banco preenchido')
    else:
        print("nenhuma opcacao valida")


if __name__ == '__main__':
    main()
