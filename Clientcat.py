import datetime
import socket
import os
import pickle

HOST = input("IP server: ")
PORT = int(input("Puerto del server: "))
buffer_size = 1024

def mostrarTablero(data):
    columna = "    "
    for i in range(0, 4*l - 3):
        columna += "*"

    letras ="    A   B   C"
    if(l == 5):
        letras += "   D   E"
    print(letras)

    for i in range(0, l):
        print( i + 1, end='   ')
        for j in range(0, l):
            dato = " " if (data[i][j] == "") else data[i][j]
            line = " / " if (j < l - 1) else "  "
            print(dato + line,end='')
        if i < l - 1:
            print("\n" + columna)
    print("\n")

def validarJuego(jugada_cliente,l,Tablero):
    coordenadas = jugada_cliente.split(',')
    if(len(coordenadas)==2):
        if( set(coordenadas[0]).issubset(set(x_mov)) and coordenadas[0] != '' and set(coordenadas[1]).issubset(set(y_mov)) and coordenadas[1] != ''):
            if(Tablero[int( coordenadas[1] ) - 1][ord( coordenadas[0] ) - 65] == ''):
                return True
    else:
        print("Opción no disponible")
        return False
    print("Intentar de nuevo")
    return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:

    TCPClientSocket.connect((HOST,PORT))

    print("Dificultad \n1.Facil\n2.Dificil \n")
    dificultad = input("Dificultad:")
    x_mov = ['A','B','C']
    y_mov = ['1','2','3']
    if(int(dificultad) == 1):
        l=3
    elif(int(dificultad) == 2):
        l=5
        x_mov.append('D')
        x_mov.append('E')
        y_mov.append('4')
        y_mov.append('5')
    print("Nivel")
    TCPClientSocket.sendall(str.encode(dificultad))


    print("Empezando juego")
    while(True):
        data = pickle.loads(TCPClientSocket.recv(buffer_size))
        if(data[l] == 'FINAL'):

            print(data[l+1])
            print("Tiempo:"+data[l+2])
            mostrarTablero(data)
            break
        if(not data[l]):
            while(True):
         
                mostrarTablero(data)
                jugada_cliente = input("Matriz (letra,numero): ")
                if(validarJuego(jugada_cliente,l,data)):
                    TCPClientSocket.sendall(pickle.dumps(jugada_cliente))
                    break
                else:
                    print("No existe esa opción...")