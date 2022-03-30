import os
import threading
from time import sleep

# Coluna em que os remedios comecam
remedios_col = 46

# Nome do arquivo .data a ser criado
nome_data = os.path.join("data", "pmc.data")

# ---------------------------------------------------------------------------------------
# NAO MODIFICAR A PARTIR DAQUI

# CONVERTE UM XML EM UM DICIONARIO PYTHON, QUE SERA GUARDADO UM ARQUIVO .DATA

def counter():
    global count
    while True:
        sleep(1)
        count += 1

def remove_text(string):
    return str(string).replace("text:", "").replace("'", "")

def main():
    import xlrd
    import pickle
    from sys import exit
    from time import sleep

    global nome_data
    global nome_xls
    global remedios_col
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

    # Subtrair 1 de remedios_col por conta de como indexes funcionam
    remedios_col -= 1
    categorias = []
    remedios = {}

    # Popular categorias que todo remedio vai possuir
    # e.g: nome, produto, pmc, etc
    for i in sh.row(remedios_col - 1):
        categorias.append(remove_text(i))

    print("Convertendo dados...")
    for fileira in range(remedios_col, sh.nrows):
        # Criar cada remedio como um value do dicionario "remedios" e atribuir
        # um dicionario vazio a ele, que possuira suas categorias
        remedios[fileira] = {}
        for categoria in range(len(categorias)):
            # Atribuir categorias a cada remedio
            remedios[fileira][categorias[categoria]] = remove_text(sh.row(fileira)[categoria])

    # Organizar remedios por ordem alfabetica do produto
    print("Organizando remedios...")
    remedios = dict(sorted(tuple(remedios.items()), key=lambda x: f"{x[1]['PRODUTO']} {x[1]['LABORATÓRIO']} {x[1]['APRESENTAÇÃO']}"))

    print("Escrevendo dados...")
    with open(nome_data, "wb") as wf:
        pickle.dump(remedios, wf)

    print("Convertido com sucesso!\nTempo total:", count, "segundos")

count = 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcesso interrompido.\nSaindo...")
        exit(0)
