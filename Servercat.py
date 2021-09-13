import datetime
import socket
import os
import pickle
import random

HOST = input("IP Server: ")
PORT = int(input("Puerto del server: "))
buffer_size = 1024

def comienzaTablero(lineas):
    for i in range(0, lineas):
        aux = []
        for j in range(0, lineas):
            aux.append('')
        Tablero.append(aux)
def mostrarTablero():
    linea = ""
    for i in range(0, 4 * l - 3):
        linea += "*"

    for i in range(0, l):
        for j in range(0, l):
            dato = " " if (Tablero[i][j] == "") else Tablero[i][j]
            barra = " / " if (j < l - 1) else "  "
            print(dato + barra, end='')
        if i < l - 1:
            print("\n" + linea)
    print("\n")


def validarJuego(jugada_cliente, l):
    coordenadas = jugada_cliente.split(',')  # Convertimos nuestro string a una lista
    if (len(coordenadas) == 2):
        if (set(coordenadas[0]).issubset(set(x_mov)) and coordenadas[0] != '' and set(coordenadas[1]).issubset(
                set(y_mov)) and coordenadas[1] != ''):
            return iniciarMatriz(int(coordenadas[1]) - 1, ord(coordenadas[0]) - 65, l)
    else:
        return False


def iniciarMatriz(x, y, l):
    if (Tablero[x][y] == ''):
        Tablero[x][y] = "X" if (turno_Servidor) else "O"
        pos = y + 1 + l * x
        if (pos in posLibres):
            posLibres.remove(pos)
        return validarTabla(x, y, l)
    else:
        return False


def validarTabla(x, y, l):
    if (turno_Servidor):
        sym = "X"
    else:
        sym = "O"
    filaRecorrida = True

    for j in range(0, l):
        if (Tablero[x][j] != sym):
            filaRecorrida = False
            break

    for i in range(0, l):
        if (Tablero[i][y] != sym):
            filaRecorrida = False
            break

    for i in range(0, l):
        if (Tablero[i][i] != sym):
            filaRecorrida = False
            break

    for i in range(0, l):
        if (Tablero[i][l - 1 - i] != sym):
            filaRecorrida = False
            break

    if (not filaRecorrida and len(posLibres) > 0):
        return True

    if (turno_Servidor and filaRecorrida):
        res = "Server gana"
        print("Server gana")
    elif (not turno_Servidor and filaRecorrida):
        res = "Has ganado"
        print("Has ganado")
    if (not filaRecorrida):
        res = "Empate"
        print("Empate")

    hora_fin = datetime.datetime.now()
    tiempo_final = hora_fin - hora_inicio

    data = []
    data = Tablero.copy()
    data.append("FIN")
    data.append(res)
    data.append(str(tiempo_final))
    Client_conn.sendall(pickle.dumps(data))
    global juego_Finalizado
    juego_Finalizado = True
    return juego_Finalizado


def Jugando(l):
    jugada_Servidor = random.choice(posLibres)
    x = (l if (jugada_Servidor % l == 0) else jugada_Servidor % l) - 1
    y = int((jugada_Servidor - 1) / l)
    if (not iniciarMatriz(y, x, l)):
        Jugando(l)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("Server TCP esperando...")

    while True:
        Client_conn, Client_addr = TCPServerSocket.accept()
        with Client_conn:
            print("Interconexiòn completa", Client_addr)
            dificultad = Client_conn.recv(buffer_size)
            print("Dificultad: ", dificultad)
            hora_inicio = datetime.datetime.now()
            posLibres = []
            x_mov = ['A', 'B', 'C']
            y_mov = ['1', '2', '3']
            if (int(dificultad) == 1):
                l = 3
            elif (int(dificultad) == 2):
                l = 5
                x_mov.append('D')
                x_mov.append('E')
                y_mov.append('4')
                y_mov.append('5')
            for i in range(1, l * l + 1):
                posLibres.append(i)
            Tablero = []
            comienzaTablero(l)
            numCeldas = 0
            juego_Finalizado = 0
            turno_Servidor = 0
            while (not juego_Finalizado):

                mostrarTablero()
                if (turno_Servidor):
                    Jugando(l)
                    turno_Servidor = not turno_Servidor
                    numCeldas += 1
                else:
                    data = []
                    data = Tablero.copy()
                    data.append(turno_Servidor)
                    Client_conn.sendall(pickle.dumps(data))
                    jugada_cliente = Client_conn.recv(buffer_size)
                    if (validarJuego(pickle.loads(jugada_cliente), l)):
                        mostrarTablero()
                        turno_Servidor = not turno_Servidor
                        numCeldas += 1