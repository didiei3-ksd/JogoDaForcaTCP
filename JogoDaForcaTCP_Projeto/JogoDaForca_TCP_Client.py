from socket import *
serverName = "localhost"

# Prepara as variaveis para fazer a conexao
serverPort = 20000
clientSocket = socket(AF_INET, SOCK_STREAM)

#Tenta se conectar ao servidor
clientSocket.connect((serverName,serverPort))
clientSocket.send(bytes("c", "utf-8"))

print("Jogo da Forca - TCP - Client")

while True:
    # Aguarda uma mensagem dizendo se a proxima mensagem exigira o retorno de um input ou nao
    modifiedSentence = clientSocket.recv(1024)
    confirmacao = str(modifiedSentence,"utf-8")

    # Confirma que recebeu e printou a mensagem para o servidor continuar suas tarefas
    clientSocket.send(bytes("R", "utf-8"))
    print("\n")
    if confirmacao == "True":
        # Caso a mensagem necessite do retorno de um input, pede um ao jogador e manda ele para o servidor
        modifiedSentence = clientSocket.recv(1024)
        text = str(modifiedSentence, "utf-8")
        clientSocket.send(bytes(input(text), "utf-8"))
    elif confirmacao == "Fim":
        # Caso a mensagem seja a de fim, sai do laco e finaliza o jogo
        break
    else:
        # Caso a mensagem nao necessite do retorno de um input, apenas printa o que recebeu na tela
        modifiedSentence = clientSocket.recv(1024)
        text = str(modifiedSentence, "utf-8")
        print(text)

        # Confirma que recebeu e printou a mensagem para o servidor continuar suas tarefas
        clientSocket.send(bytes("R", "utf-8"))

#Finaliza a conexao
clientSocket.close()
confirmarFinal = str(input("\nFim do programa."))
