import os
import threading
from time import sleep

# CONVERTE UM XML EM UM DICIONARIO PYTHON, QUE SERA GUARDADO UM ARQUIVO .DATA

def counter():
    global count
    while True:
        sleep(1)
        count += 1

def remove_text(cell):
    return str(cell).replace("text:", "").replace("'", "")

def main():
    import xlrd
    import pickle
    from sys import exit
    from time import sleep

    global nome_data
    global nome_xls
    global count

    # Calcular tempo levado
    t1 = threading.Thread(target=counter, daemon=True)
    t1.start()

    # Checar a existencia de um diretorio "data"
    data_exists = False
    for i in os.listdir():
        if i == "data":
            data_exists = True
    
    if not data_exists:
        os.mkdir("data")

    # Checar a existencia de um arquivo xls
    print("Procurando arquivo .xls...")
    xls_exists = False;
    for file in os.listdir():
        if (os.path.isfile(file) and file.endswith(".xls")):
            xls_exists = True
            nome_xls = file

    if not xls_exists:
        print("ERRO: Arquivo .xls nao encontrado.")
        sleep(4)
        return 1

    # Criar arquivo data, caso ele nao exista ainda
    if not os.path.exists(nome_data):
        print("Criando arquivo .data...")
        open(nome_data, "w")

    print("Lendo .xls...")
    # Carregar arquivo xls
    wb = xlrd.open_workbook(nome_xls)
    sh = wb.sheet_by_index(0)

    # Descobrir em que coluna os remedios comecam
    for fileira in range(sh.nrows):
        if (
            remove_text(sh.row(fileira)[0]) == 'SUBSTÂNCIA' and
            remove_text(sh.row(fileira)[1]) == 'CNPJ' and
            remove_text(sh.row(fileira)[2]) == 'LABORATÓRIO' and
            remove_text(sh.row(fileira)[3]) == 'CÓDIGO GGREM' and
            remove_text(sh.row(fileira)[4]) == 'REGISTRO'
            ):
            remedios_fileira = fileira + 1
            print("Remedios comecam na fileira", remedios_fileira + 1)
            break

    categorias = []
    remedios = {}

    # Popular categorias que todo remedio vai possuir
    # e.g: nome, produto, pmc, etc
    for i in sh.row(remedios_fileira - 1):
        categorias.append(remove_text(i))

    print("Convertendo dados...")
    for fileira in range(remedios_fileira, sh.nrows):
        # Criar cada remedio como um value do dicionario "remedios" e atribuir
        # um dicionario vazio a ele, que possuira suas categorias
        remedios[fileira] = {}
        for categoria in range(len(categorias)):
            # Atribuir categorias a cada remedio
            remedios[fileira][categorias[categoria]] = remove_text(sh.row(fileira)[categoria])

    # Organizar remedios por ordem alfabetica do produto
    print("Organizando remedios...")
    remedios = dict(sorted(tuple(remedios.items()), key=lambda x: f"{x[1]['PRODUTO']} {x[1]['LABORATÓRIO']} {x[1]['APRESENTAÇÃO']}"))

    # Escrever dicionario remedios em arquivo .data
    print("Escrevendo dados...")
    with open(nome_data, "wb") as wf:
        pickle.dump(remedios, wf)

    # Mover arquivo xls para diretorio data
    os.rename(nome_xls, os.path.join("data", nome_xls))
    print("Convertido com sucesso!\nTempo total:", count, "segundos")

count = 0

# Nome do arquivo .data a ser criado
nome_data = os.path.join("data", "pmc.data")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcesso interrompido.\nSaindo...")
        exit(0)
