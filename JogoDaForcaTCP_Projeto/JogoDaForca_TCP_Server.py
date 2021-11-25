import datetime
import random
from socket import *


def EnviarMensagem(receberInput, texto):
    """Manda uma mensagem para o cliente, podendo ou nao receber um input de volta na variavel sentence"""

    global sentence, temp

    if receberInput == False:
        connectionSocket.send(bytes("False", "utf-8"))
        temp = connectionSocket.recv(65000)
        connectionSocket.send(bytes(texto, "utf-8"))
        temp = connectionSocket.recv(65000)
    else:
        connectionSocket.send(bytes("True", "utf-8"))
        temp = connectionSocket.recv(65000)
        connectionSocket.send(bytes(texto, "utf-8"))
        sentence = connectionSocket.recv(65000)


def DesenharForca():
    """Faz o desenho da forca, coloca em um texto e retorna uma string"""

    global PalavraArray, jogadorLista, forcaLetras, jogoGanho
    texto = ""
    texto += "____________\n"
    texto += "           |\n"
    texto += "           |\n"
    if forcaLetras >= 1:
        texto += "          ( )\n"
    if forcaLetras == 2:
        texto += "           |\n"
    if forcaLetras == 3:
        texto += "          /|\n"
    if forcaLetras >= 4:
        texto += r"          /|\ " + "\n"
    if forcaLetras == 5:
        texto += "           |\n"
        texto += "          /\n"
    if forcaLetras >= 6:
        texto += "           |\n"
        texto += r"          / \ " + "\n"

    texto += "\n\n"

    acertouLetra = False
    for x in PalavraArray:
        for y in jogadorLista:
            if y == x:
                acertouLetra = True

        if jogoGanho == True:
            acertouLetra = True

        if acertouLetra == True:
            texto += " " + x + " "
        else:
            texto += " ___ "

        acertouLetra = False

    return texto


def AddForca():
    """Adiciona 1 ao contador de erros e manda uma mensagem ao cliente"""

    global jogoPerdido, forcaLetras
    forcaLetras += 1

    print("\nVocê errou!")
    texto = "\nVocê errou!"

    EnviarMensagem(False, texto)

    if forcaLetras >= 6:
        jogoPerdido = True


# Prepara as variaveis para fazer a conexao
serverPort = 20000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
# O argumento “listen” diz à biblioteca de soquetes que queremos enfileirar no máximo 5
# requisições deconexão (normalmente o máximo) antes de recusar começar a recusar conexões
# externas. Caso o resto do código esteja escrito corretamente, isso deverá ser o suficiente.

print("Jogo da Forca - TCP - Server\n")

random.seed((datetime.datetime.now().strftime("%f")))
palavras = ["WARHAMMER40K", "ROSA", "FOGO", "SANDALATION", "TRABALHO", "QUINTOSEMESTRE", "ISAIAS", "NACULUDU",
            "GLUBERS", "SKYRIM6"]
NumPalavraRandom = random.randint(0, len(palavras) - 1)
PalavraArray = []
for x in palavras[NumPalavraRandom]:
    PalavraArray.append(x)
print(PalavraArray, "\n")
texto = ""
recebido = None
temp = None

#Espera um cliente se conectar
connectionSocket, addr = serverSocket.accept()

forcaLetras = 0
jogadorLista = []
jogoGanho = False
jogoPerdido = False
while True:
    # Manda o desenho da forca para o cliente
    texto = DesenharForca()
    print("\n", texto)

    EnviarMensagem(False, texto)

    # Pede uma resposta para o cliente e confere se ele acertou ou nao, e se ele ganhou ou perdeu o jogo
    respostaJogador = ""
    while respostaJogador != "1" and respostaJogador != "2":
        texto = "\n1-Para chutar uma letra.\n2-Para advinhar a frase.\n"

        EnviarMensagem(True, texto)

        respostaJogador = str(sentence, "utf-8")

        print("\nRecebido: ", respostaJogador)

    if respostaJogador == "1":
        resposta = ""
        while len(resposta) != 1:
            respostas = str("\nDigite uma letra: ")
            print(respostas)
            texto = respostas

            EnviarMensagem(True, texto)

            resposta = str(sentence, "utf-8").upper()
            print("\nRecebido: ", resposta)

        # Adiciona a resposta a lista de respostas do jogador caso ele nao tenha a escolhido ainda
        if resposta not in jogadorLista:
            jogadorLista.append(resposta)

            # Confere se o jogador acertou a letra
            if resposta in PalavraArray:
                print("\nVocê acertou uma letra!")
                texto = "Você acertou uma letra!"

                EnviarMensagem(False, texto)

                # Confere se todas as letras da palavra foram descobertas
                if resposta in jogadorLista:
                    num = 0
                    for x in PalavraArray:
                        for y in jogadorLista:
                            if x == y:
                                num += 1
                    if num == len(PalavraArray):
                        jogoGanho = True
            else:
                AddForca()
        else:
            print("\nVocê ja chutou esta letra.")
            texto = "Você ja chutou esta letra."

            EnviarMensagem(False, texto)

    elif (respostaJogador == "2"):
        print("\nDigite uma palavra: ")
        texto = "Digite uma palavra: "

        EnviarMensagem(True, texto)

        resposta = str(sentence, "utf-8").upper()
        print("\nRecebido: ", resposta)

        # Confere se o jogador acertou a palavra
        if resposta == palavras[NumPalavraRandom]:
            print("\nVocê acertou a palavra inteira!")
            texto = "Você acertou a palavra inteira!"

            EnviarMensagem(False, texto)

            jogoGanho = True
        else:
            AddForca()

    #Caso o jogador tenha ganho, finaliza o jogo
    if jogoGanho:
        print("\nA palavra era: ", palavras[NumPalavraRandom], ". Você venceu!")

        texto = "A palavra era: " + palavras[NumPalavraRandom] + ". Você venceu!"

        EnviarMensagem(False, texto)
        break

    # Caso o jogador tenha perdido, finaliza o jogo
    if jogoPerdido:
        print("\nVocê perdeu!")

        texto = "Você perdeu!"

        EnviarMensagem(False, texto)
        break

# Desenha a forca no fim do jogo
texto = DesenharForca()
print(texto)

EnviarMensagem(False, texto)

#Envia uma mensagem de fim para o cliente finalizar sua conexao
connectionSocket.send(bytes("Fim", "utf-8"))
temp = connectionSocket.recv(65000)

#Finaliza a conexao
connectionSocket.close()
confirmarFinal = input("\nFim do programa.")