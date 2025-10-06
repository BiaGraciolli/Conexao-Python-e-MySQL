from prettytable import PrettyTable
import mysql.connector

def abrirbd():
    try:
        global conexao
        conexao=mysql.connector.Connect(host='localhost',database='univap',user='root',password='')
        if conexao.is_connected():
            infobd=conexao.get_server_info()
            print("-"*80+"\nConexão ao servidor - Versão {}".format(infobd))
            global comandosql
            comandosql=conexao.cursor()
            comandosql.execute('select database();')
            nomebd=comandosql.fetchone()
            print(f'Banco de dados - {nomebd}')
            comandosql.close()
            print('-'*80)
            return 1
        else:
            print("-"*80+'\n CONEXÃO NÃO REALIZADA\n'+"-"*80)
            return 0
    except Exception as erro:
        print(f'Erro: {erro}')
        return 0

def cadastrados():
    grid=PrettyTable(['Registro','Nome do professor','Telefone','Idade','Salário'])
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'select * from professores;')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0:
            for dados in tabela:
                grid.add_row([dados[0],dados[1],dados[2],dados[3], f"{dados[4]:.2f}"])
            print(grid)
        else:
            print('Não há professores cadastrados no banco de dados.\n')
        comandosql.close()
    except Exception as erro:
        print(f'ERRO: {erro}')

def consulta(cp=0):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'select * from professores where registro={cp};')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0:
            for dados in tabela:
                print(f'''
--------------------------------------------------------------------------------
Nome do professor: {dados[1]}
Telefone:          {dados[2]}
Idade:             {dados[3]}
Salário:           {dados[4]:.2f}
--------------------------------------------------------------------------------
                ''')
            comandosql.close()
            return 'c'
        else:
            comandosql.close()
            return 'nc'
    except Exception as error:
        return (f'ERRO NA CONSULTA: {error}')

def cadastrar(cp=0,np='',tp='',id=0, sa=0.00):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'insert into professores(registro,nomeprof,telefoneprof,idadeprof,salarioprof) values ({cp},"{np}","{tp}",{id},{sa});')
        conexao.commit()
        comandosql.close()
        return 'Cadastro de professor realizado !!!'
    except Exception as erro:
        print(f'Erro:{erro}')
        return 'Não foi possível cadastrar o professor.'

def alterarnome(cp=0,np=''):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'update professores SET nomeprof="{np}" where registro={cp};')
        conexao.commit()
        comandosql.close()
        return 'Nome alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o nome.'

def alterartelefone(cp=0, tp=''):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update professores SET telefoneprof="{tp}" where registro={cp};')
        conexao.commit()
        comandosql.close()
        return 'Telefone alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o telefone.'

def alteraridade(cp=0, id=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update professores SET idadeprof="{id}" where registro={cp};')
        conexao.commit()
        comandosql.close()
        return 'Idade alterada com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar a idade.'

def alterarsalario(cp=0, sa=0.0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update professores SET salarioprof="{sa}" where registro={cp};')
        conexao.commit()
        comandosql.close()
        return 'Salário alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o salário.'

def excluir(cp=0):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores where codprofessor={cp};')
        verificacao=comandosql.fetchone()
        if verificacao:
            comandosql.close()
            return 'Não é possível deletar um professor vínculado a uma disciplina na tabela disciplinasxprofessores!'
        else:
            comandosql.execute(f'delete from professores where registro={cp};')
            conexao.commit()
            comandosql.close()
            return 'Professor excluído !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível deletar o professor'

##################################################################################################################
if abrirbd()==1:
    resp=input('Deseja entrar no módulo de professores? (1-Sim/Qualquer tecla-Sair):')
    while resp=='1':
        print('=' * 80)
        print('{:^80}'.format('SISTEMA UNIVAP - PROFESSORES'))
        print('=' * 80)
        while True:
            codigoprof=input('Código do professor para consultar ou cadastrar (0 para mostrar todos):')
            if codigoprof.isnumeric():
                codigoprof=int(codigoprof)
                break
        if codigoprof==0:
            cadastrados()
            print('\n\n')
            print('=' * 80)
        if consulta(codigoprof) == 'nc' and codigoprof!=0:
            cancelar = 0
            while True:
                nomeprof = input('Cadastrar - Nome do professor (ou N para cancelar): ')
                if nomeprof.upper() == 'N':
                    print('Cadastro cancelado.')
                    cancelar = 1
                    break
                if len(nomeprof) <= 50 and not nomeprof.isnumeric():
                    break
                else:
                    print('Nome inválido! O nome deve ter até 50 caracteres.')
            if cancelar > 0:
                continue
            while True:
                telefoneprof = input('Cadastrar - Telefone do professor (ou N para cancelar): ')
                if telefoneprof.upper() == 'N':
                    print('Cadastro cancelado.')
                    cancelar = 1
                    break
                if len(telefoneprof) <= 30 and not telefoneprof.isalpha():
                    break
                else:
                    print('Telefone inválido! Deve possuir até 30 caracteres.')
            if cancelar > 0:
                continue
            while True:
                idadeprof = input('Cadastrar - Idade do professor (ou N para cancelar): ')
                if idadeprof.upper() == 'N':
                    print('Cadastro cancelado.')
                    cancelar = 1
                    break
                if idadeprof.isdigit():
                    idadeprof = int(idadeprof)
                    if 18 < idadeprof < 100:
                        break
                    else:
                        print('Idade inválida! Digite um número maior que 18 e menor que 100.')
                else:
                    print('Idade inválida! Digite um número maior que 18 e menor que 100.')
            if cancelar > 0:
                continue
            while True:
                salarioprof = input('Cadastrar - Salário do professor (ou N para cancelar): ')
                if salarioprof.upper() == 'N':
                    print('Cadastro cancelado.')
                    cancelar = 1
                    break
                try:
                    salarioprof = float(salarioprof)
                    if salarioprof > 0:
                        break
                    else:
                        print('Salário inválido! O salário deve ser maior que zero.')
                except:
                    print('Salário inválido! Deve ser um número decimal ou inteiro.')
            if cancelar > 0:
                continue
            msg = cadastrar(codigoprof, nomeprof, telefoneprof, idadeprof, salarioprof)
            print(msg)
        elif (codigoprof!=0):
            op=input('Escolha... [A]-Alterar   [E]-Excluir   [C]-Cancelar :')
            while op!='A' and op!='E' and op!='C':
                op=input('Operação errada. Digite novamente... [A]-Alterar   [E]-Excluir   [C]-Cancelar :')
            if op=='A':
                comandosql.execute(f'select * from disciplinasxprofessores where codprofessor={codigoprof};')
                if comandosql.fetchone():
                    comandosql.close()
                    print('Alterações não permitidas! Professor vinculado a uma disciplina.')
                else:
                    comandosql.close()
                    print('ATENÇÃO: Código do professor não pode ser alterado')
                    if input('Deseja alterar o nome? S-sim/Qualquer tecla-não: ') == 'S':
                        while True:
                            nomeprof = input('Informe o novo nome do professor ou N para sair: ')
                            if nomeprof=='N':
                                break
                            if len(nomeprof)<50 and not nomeprof.isdigit():
                                msg = alterarnome(codigoprof, nomeprof)
                                print(msg)
                                break
                            else:
                                print('Nome inválido! Digite novamente com menos de 50 caracteres.')
                    if input('Deseja alterar o telefone? S-sim/Qualquer tecla-não: ')=='S':
                        while True:
                            telefoneprof = input('Informe o novo telefone do professor ou N para sair: ')
                            if telefoneprof=='N':
                                break
                            if len(telefoneprof) < 30:
                                msg = alterartelefone(codigoprof, telefoneprof)
                                print(msg)
                                break
                            else:
                                print('Telefone inválido! Digite novamente (menos de 30 caracteres).')
                    if input('Deseja alterar a idade? S-sim/Qualquer tecla-não: ')=='S':
                        while True:
                            idadeprof = int(input('Informe a nova idade do professor ou 0 para sair: '))
                            if idadeprof==0:
                                break
                            if idadeprof>18 and idadeprof<100:
                                msg = alteraridade(codigoprof, idadeprof)
                                print(msg)
                                break
                            else:
                                print('Idade inválida! Digite novamente (maior que 18 e menor que 100).')
                    if input('Deseja alterar o salário? S-sim/Qualquer tecla-não: ')=='S':
                        while True:
                            salarioprof =float(input('Informe o novo salário do professor ou 0 para sair : '))
                            if salarioprof==0:
                                break
                            if salarioprof>0:
                                msg = alterarsalario(codigoprof, salarioprof)
                                print(msg)
                                break
                            else:
                                print('Salário inválido! Digite novamente (maior que 0)')
            elif op=='E':
                confirmacao=input('ATENÇÃO!! TEM CERTEZA QUE DESEJA EXCLUIR? S-SIM OU N-NÃO: ')
                while confirmacao!='S' and confirmacao!='N':
                    confirmacao=input('RESPOSTA INVÁLIDA!! TEM CERTEZA QUE DESEJA EXCLUIR? S-SIM OU N-NÃO: ')
                if confirmacao=='S':
                    msg=excluir(codigoprof)
                    print(msg)
        print('\n\n')
        print('=' * 80)
        if input('Deseja continuar usando o programa? 1- Sim OU qualquer tecla para sair:') == '1':
            continue
        else:
            comandosql.close()
            conexao.close()
            break
else:
    print('FIM DO PROGRAMA!! Algum problema existente na conexão com banco de dados.')