from os import system, name

def main():
    import pickle
    import os
    from sys import exit
    from converter import nome_data
    from time import sleep

    if not os.path.exists(nome_data):
        print("Arquivo .data nao encontrado. Execute \"converter.py\" primeiro.")
        sleep(4)
        return 1;
    
    with open(nome_data, "rb") as rf:
        remedios = pickle.load(rf)

    nome = ""
    while True:
        resultados = []
        print("-"*100)
        nome = input("Remedio: ").strip().upper()
        system('cls' if name == 'nt' else 'clear')
        if nome == "SAIR":
            break
        
        if "." in nome:
            for remedio in remedios:
                if nome.replace(".", "") == remedios[remedio]['PRODUTO']:
                    resultados.append(remedio)
        else:
            for remedio in remedios:
                if nome in remedios[remedio]['PRODUTO']:
                    resultados.append(remedio)
        print("\nResultados:")
        
        for r in resultados:
            mg = " ".join(remedios[r]['APRESENTAÇÃO'].split()[:2])
            print("-"*100)
            print(
                f"\nNome: {remedios[r]['PRODUTO']} {mg} ({remedios[r]['LABORATÓRIO']})\n"
                f"Substancia: {remedios[r]['SUBSTÂNCIA']}\n"
                f"Apresentacao: {remedios[r]['APRESENTAÇÃO']}\n"
                f"Tipo de Produto: {remedios[r]['TIPO DE PRODUTO (STATUS DO PRODUTO)']}\n"
                f"PMC: {remedios[r]['PMC 17%']}\n"
                )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaindo...")
