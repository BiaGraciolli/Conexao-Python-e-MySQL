from prettytable import PrettyTable 
import mysql.connector

def abrirbanco():
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

def professoresedisciplinas():
    try:
        comandosql=conexao.cursor()
        comandosql.execute('select registro, nomeprof from professores;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount>0:
            print('-' * 80)
            print('PROFESSORES')
            print('-' * 80)
            for dados in tabela:
                print(f'Registro: {dados[0]} - Nome do professor: {dados[1]}')
        else:
            print('Não há registros na tabela professores')
        print('-' * 80)
        comandosql.close()
    except Exception as erro:
        print(f'Erro: {erro}')
    try:
        comandosql=conexao.cursor()
        comandosql.execute('select codigodisc, nomedisc from disciplinas;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount>0:
            print('DISCIPLINAS')
            print('-' * 80)
            for dados in tabela:
                print(f'Código: {dados[0]} - Nome da disciplina: {dados[1]}')
        else:
            print(f'Não há registros na tabela disciplinas')
        print('-' * 80)
        comandosql.close()
    except Exception as erro:
        print(f'Erro: {erro}')

def cadastros():
    grid=PrettyTable(['Cód. disciplinanocurso','Cód. disciplina','Cód. professor','Curso','Carga horária','Ano letivo'])
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores;')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0:
            for dados in tabela:
                grid.add_row([dados[0],dados[1],dados[2],dados[3], dados[4], dados[5]])
            print(grid)
        else:
            print('-'*80)
            print('Não há registros no banco de dados.\n')
            print('-'*80)
        comandosql.close()
    except Exception as erro:
        print(f'ERRO: {erro}')

def consulta(cdp=""):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores where codigodisciplinanocurso="{cdp}";')
        tabela=comandosql.fetchall()
        if comandosql.rowcount>0:
            for dados in tabela:
                print(f'''
--------------------------------------------------------------------------------
Cód. disciplina: {dados[1]}
Cód. professor:  {dados[2]}
Curso:           {dados[3]}
Carga horária:   {dados[4]}
Ano letivo:      {dados[5]}
--------------------------------------------------------------------------------
                ''')
            comandosql.close()
            return 'c'
        else:
            comandosql.close()
            return 'nc'
    except Exception as error:
        return (f'ERRO NA CONSULTA: {error}')

def cadastrar(cdp="",cd=0,cp=0,curso=0, ch=0, al=0):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'insert into disciplinasxprofessores(codigodisciplinanocurso,coddisciplina,codprofessor,curso,cargahoraria,anoletivo) values ("{cdp}",{cd},{cp},{curso},{ch},{al});')
        conexao.commit()
        comandosql.close()
        return 'Cadastro no banco realizado !!!'
    except Exception as erro:
        print(f'Erro:{erro}')
        return 'Não foi possível cadastrar os dados.'

def alterarcoddisciplina(cdp="",cd=0):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'update disciplinasxprofessores SET coddisciplina={cd} where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Código da disciplina alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o código da disciplina.'

def alterarcodprofessor(cdp="",cp=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update disciplinasxprofessores SET codprofessor={cp} where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Código do professor alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o código do professor.'

def alterarcurso(cdp="", curso=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update disciplinasxprofessores SET curso={curso} where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Curso alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o curso.'

def alterarcargahoraria(cdp="", ch=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update disciplinasxprofessores SET cargahoraria={ch} where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Carga horária alterada com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar a carga horária.'

def alteraranoletivo(cdp="", al=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update disciplinasxprofessores SET anoletivo={al} where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Ano letivo alterado com sucesso !!!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível alterar o ano letivo.'

def excluir(cdp=""):
    try:
        comandosql=conexao.cursor()
        comandosql.execute(f'delete from disciplinasxprofessores where codigodisciplinanocurso="{cdp}";')
        conexao.commit()
        comandosql.close()
        return 'Registro excluído com sucesso!'
    except Exception as erro:
        print(f'Erro: {erro}')
        return 'Não foi possível excluir o registro.'

##################################################################################################################
if abrirbanco()==1:
    resp=input('Deseja entrar no módulo de disciplinasxprofessores? (1-Sim/Qualquer tecla-Sair):')
    while resp=='1':
        print('=' * 80)
        print('{:^80}'.format('SISTEMA UNIVAP - DISCIPLINASXPROFESSORES'))
        print('=' * 80)
        while True:
            codigodisciplinanocurso=input('Código da disciplina no curso para consultar ou cadastrar (0 para mostrar todos):')
            if codigodisciplinanocurso=='0':
                cadastros()
                professoresedisciplinas()
                print('\n\n')
                print('=' * 80)
            if consulta(codigodisciplinanocurso)=='nc' and codigodisciplinanocurso!='0':
                cancelar=0
                comandosql = conexao.cursor()
                comandosql.execute('select registro, nomeprof from professores;')
                professores=comandosql.fetchall()
                comandosql.execute('select codigodisc, nomedisc from disciplinas;')
                disciplinas=comandosql.fetchall()
                comandosql.close()
                if professores and disciplinas:
                    professoresedisciplinas()
                    while True:
                        coddisciplina = input('Cadastrar - Código da disciplina (ou N para cancelar): ')
                        if coddisciplina.upper()=='N':
                            print('Cadastro cancelado.')
                            cancelar=1
                            break
                        if coddisciplina.isnumeric():
                            coddisciplina = int(coddisciplina)
                            try:
                                comandosql=conexao.cursor()
                                comandosql.execute(f'select * from disciplinas where codigodisc = {coddisciplina}')
                                if comandosql.fetchone():
                                    comandosql.close()
                                    break
                                else:
                                    comandosql.close()
                                    print('Disciplina não encontrada!')
                            except Exception as erro:
                                print(f'Erro: {erro}')
                        else:
                            print('Código da disciplina inválido! Apenas números.')
                    if cancelar>0:
                        continue
                    while True:
                        codprofessor = input('\nCadastrar - Código do professor (ou N para cancelar): ')
                        if codprofessor.upper()=='N':
                            print('Cadastro cancelado.')
                            cancelar=1
                            break
                        if codprofessor.isnumeric():
                            codprofessor = int(codprofessor)
                            try:
                                comandosql=conexao.cursor()
                                comandosql.execute(f'select * from professores where registro = {codprofessor}')
                                if comandosql.fetchone():
                                    comandosql.close()
                                    break
                                else:
                                    comandosql.close()
                                    print('Professor não encontrado!')
                            except Exception as erro:
                                print(f'Erro: {erro}')
                        else:
                                print('Código do professor inválido! Apenas números.')
                    if cancelar>0:
                        continue
                    while True:
                        curso = input('\nCadastrar - Curso (ou N para cancelar): ')
                        if curso.upper()=='N':
                            print('Cadastro cancelado')
                            cancelar=1
                            break
                        if curso.isnumeric():
                            curso=int(curso)
                            break
                        else:
                            print('Curso inválido! Apenas números.')
                    if cancelar>0:
                        continue
                    while True:
                        cargahoraria = input('\nCadastrar - Carga horária (ou N para cancelar) :')
                        if cargahoraria.upper()=='N':
                            print('Cadastro cancelado')
                            cancelar=1
                            break
                        if cargahoraria.isnumeric():
                            cargahoraria=int(cargahoraria)
                            break
                        else:
                            print('Carga horária inválida! Apenas números.')
                    if cancelar>0:
                        continue
                    while True:
                        anoletivo = input('\nCadastrar - Ano letivo (ou N para cancelar:')
                        if anoletivo.upper()=='N':
                            print('Cadastro cancelado')
                            cancelar=1
                            break
                        if anoletivo.isnumeric():
                            anoletivo=int(anoletivo)
                            break
                        else:
                            print('Ano letivo inválido! Apenas números.')
                    if cancelar>0:
                        continue
                    msg = cadastrar(codigodisciplinanocurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo)
                    print(msg)
                else:
                 print('Não há disciplinas e professores cadastrados no banco de dados.')
            elif (codigodisciplinanocurso!='0'):
                op=input('Escolha... [A]-Alterar   [E]-Excluir   [C]-Cancelar :')
                while op.upper()!='A' and op.upper()!='E' and op.upper()!='C':
                    op=input('Operação errada. Digite novamente... [A]-Alterar   [E]-Excluir   [C]-Cancelar :')
                if op.upper()=='A':
                    print('ATENÇÃO: Código da disciplina no curso não pode ser alterado')
                    if input('Deseja alterar o código da disciplina? S-sim/Qualquer tecla-não: ').upper() == 'S':
                        while True:
                            coddisciplina = input('Informe o novo código da disciplina ou 0 para sair: ')
                            if coddisciplina=='0':
                                break
                            if coddisciplina.isnumeric():
                                coddisciplina=int(coddisciplina)
                                if coddisciplina>0:
                                    comandosql=conexao.cursor()
                                    comandosql.execute((f'select codigodisc from disciplinas where codigodisc = {coddisciplina}'))
                                    if comandosql.fetchone():
                                        comandosql.close()
                                        msg = alterarcoddisciplina(codigodisciplinanocurso, coddisciplina)
                                        print(msg)
                                        break
                                    comandosql.close()
                                else:
                                    print('Código da disciplina não encontrado.')
                            else:
                                print('Código da disciplina inválido! Digite novamente um número int.')
                    if input('Deseja alterar o código do professor? S-sim/Qualquer tecla-não: ').upper() == 'S':
                        while True:
                            codprofessor = input('Informe o novo código do professor ou 0 para sair: ')
                            if codprofessor == '0':
                                break
                            if codprofessor.isnumeric():
                                codprofessor=int(codprofessor)
                                if codprofessor>0:
                                    comandosql=conexao.cursor()
                                    comandosql.execute(f'select registro from professores where registro={codprofessor}')
                                    if comandosql.fetchone():
                                        comandosql.close()
                                        msg = alterarcodprofessor(codigodisciplinanocurso, codprofessor)
                                        print(msg)
                                        break
                                    comandosql.close()
                                else:
                                    print('Código do professor não encontrado.')
                            else:
                                print('Código do professor inválido! Digite novamente um número int.')
                    if input('Deseja alterar o curso? S-sim/Qualquer tecla-não: ').upper() == 'S':
                        while True:
                            curso = input('Informe o novo curso ou 0 para sair: ')
                            if curso == '0':
                                break
                            if curso.isnumeric():
                                curso=int(curso)
                                if curso>0:
                                    msg = alterarcurso(codigodisciplinanocurso, curso)
                                    print(msg)
                                    break
                                else:
                                    print('Código do curso inválido! Digite novamente')
                            else:
                                print('Código do curso inválido! Digite novamente um número int.')
                    if input('Deseja alterar a carga horária? S-sim/Qualquer tecla-não: ').upper() == 'S':
                        while True:
                            cargahoraria = input('Informe a nova carga horária ou 0 para sair: ')
                            if cargahoraria == '0':
                                break
                            if cargahoraria.isnumeric():
                                cargahoraria=int(cargahoraria)
                                if cargahoraria>0:
                                    msg = alterarcargahoraria(codigodisciplinanocurso, cargahoraria)
                                    print(msg)
                                    break
                                else:
                                    print('Carga horária inválida.')
                            else:
                                print('Carga horária inválida! Digite novamente um número int.')
                    if input('Deseja alterar o ano letivo? S-sim/Qualquer tecla-não: ').upper() == 'S':
                        while True:
                            anoletivo = input('Informe o novo ano letivo ou 0 para sair): ')
                            if anoletivo=='0':
                                break
                            if anoletivo.isnumeric():
                                anoletivo=int(anoletivo)
                                if anoletivo>0:
                                    msg = alteraranoletivo(codigodisciplinanocurso, anoletivo)
                                    print(msg)
                                    break
                                else:
                                    print('Ano letivo inválido! Digite novamente.')
                            else:
                                print('Ano letivo inválido! Digite novamente um número int.')
                if op.upper()=='E':
                    confirmacao=input('ATENÇÃO!! TEM CERTEZA QUE DESEJA EXCLUIR? S-SIM OU N-NÃO: ')
                    while confirmacao.upper()!='S' and confirmacao.upper()!='N':
                        confirmacao=input('RESPOSTA INVÁLIDA!! TEM CERTEZA QUE DESEJA EXCLUIR? S-SIM OU N-NÃO: ')
                    if confirmacao.upper()=='S':
                        msg=excluir(codigodisciplinanocurso)
                        print(msg)
            print('\n\n')
            print('=' * 80)
            if input('Deseja continuar usando o programa? 1- Sim OU qualquer tecla para sair:') != '1':
                comandosql.close()
                conexao.close()
                break
else:
    print('FIM DO PROGRAMA!! Algum problema existente na conexão com banco de dados.')