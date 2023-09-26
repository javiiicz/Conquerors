# Javier Carrillo
# Carné 2023097287
# Proyecto 1

civilizaciones = []
bitacora = []
turno = 0

from datetime import datetime
import time
import random

# ARCHIVO =================================

# Lee el archivo de potencias y lo pone en la variable civilizaciones
def leerPotencias():
    global civilizaciones
    civ = open("potencias.txt", "r")
    civilizaciones = eval(civ.read())
    civ.close()

# Lee el archivo de registro y lo pone en la variable bitacora
def leerRegistro():
    global bitacora
    reg = open("registro.txt", "r")
    bitacora = eval(reg.read())
    reg.close()


# Escribe la lista civilizaciones al archivo de potencias
def escribirPotencias():
    global civilizaciones
    civ = open("potencias.txt", "w")
    civ.write(str(civilizaciones))
    civ.close()

# Escribe la lista bitacora al archivo de registro
def escribirRegistro():
    global bitacora
    reg = open("registro.txt", "w")
    reg.write(str(bitacora))
    reg.close()


leerPotencias()
leerRegistro()


# FUNCIONES ===============================

# Convierte una coordenada a una representacion solo en grados
# E: una lista en formato de coordenada [1, 2, 3]
# S: un numero
def convertirAGrados(coord):
    res = 0
    res += coord[0] * 1 # Grados
    res += coord[1] / 60 # Minutos
    res += coord[2] / 3600 # Segundos
    return res


# Calcula la distancia horizontal entre dos coordenadas en km
# E: una lista con un par de puntos [[[1,1,1],[2,2,2]],[[3,3,3],[4,4,4]]]
# S: un número (km)
def calcularDistanciaHorizontal(puntos):
    res = 60000 * abs(convertirAGrados(puntos[0][0]) - convertirAGrados(puntos[1][0]))
    return res


# Calcula la distancia vertical entre dos coordenadas en km
# E: una lista con un par de puntos [[[1,1,1],[2,2,2]],[[3,3,3],[4,4,4]]]
# S: un número (km)
def calcularDistanciaVertical(puntos):
    res = 60000 * abs(convertirAGrados(puntos[0][1]) - convertirAGrados(puntos[1][1]))
    return res


# Calcula la extension de un canton
# E: una lista en formato de canton [Canton1, [[[P1],[P2]],[[P3],[P3]]]
# S: un numero (km2)
def calcularExtensionCanton(canton):
    res = calcularDistanciaHorizontal(canton[1]) * calcularDistanciaVertical(canton[1])
    return res


# Calcula la extension de un país
# E: una lista en formato de pais [País, [[Provincias, [[Cantones]]]]]
# S: un numero (km2)
def calcularExtensionPais(pais):
    res = 0
    for provincia in pais[3]:
        for canton in provincia[1]:
            res += calcularExtensionCanton(canton)
    return res


# Actualiza la información de la extensión de un país. ## SOLO SE DEBERIA USAR AL PRINCIPIO O CUANDO SE CREA UNA NUEVA POTENCIA.
# E: una lista en formato de pais [País, [[Provincias, [[Cantones]]]]]
def actualizarExtension(pais):
    pais[2] = calcularExtensionPais(pais)

# Actualiza la extension de todos los paises. ## SOLO USAR AL PRINCIPIO, NO DURANTE EL JUEGO
def actualizarExtensionTodo():
    for potencia in civilizaciones:
        for pais in potencia[7]:
            actualizarExtension(pais)

# Actualiza la información de la vida de un país. SOLO USAR AL INCIO
# E una lista en formato de pais [País, [[Provincias, [[Cantones]]]]]
# R: la extensión de un pais no puede ser 0
def actualizarVida(pais):
    pais[1] = 100.0

# Actualiza la vida de todos los paises SOLO USAR AL INICIO
def actualizarVidaTodo():
    for potencia in civilizaciones:
        for pais in potencia[7]:
            actualizarVida(pais)

# Actualiza el estado de muerte de todas las potencias a vivo. SOLO USAR AL INICIO
def actualizarMuerte():
    global civilizaciones
    for potencia in civilizaciones:
        potencia[3] = True

# Reinicia la actividad de todas las potencias a "Activo". SOLO USAR AL INICIO
def reiniciarActividad():
    global civilizaciones
    for potencia in civilizaciones:
        potencia[2] = "Activo"


# Reinicia los misiles de todas las potencias a 1000. SOLO USAR AL INICIO
def reiniciarMisiles():
    global civilizaciones
    for potencia in civilizaciones:
        potencia[1] = 1000

# Reinicia los disparos e impactos
def reiniciarDisparosImpactos():
    global civilizaciones
    for potencia in civilizaciones:
        potencia[5] = 0
        potencia[6] = 0

# Reinicia el registro. SOLO USAR AL INICIO
def reiniciarRegistro():
    global bitacora
    bitacora = []
    escribirRegistro()

# Actualiza la vida de las potencias
def actualizarVidaPotencias():
    for potencia in civilizaciones:
        res = 0
        numPaises = 0
        for pais in potencia[7]:
            numPaises += 1
            res += pais[1]
        potencia[4] = res / numPaises

# Actualiza todo # SOLO USAR AL INICIO DEL JUEGO
def actualizar():
    actualizarExtensionTodo()
    actualizarVidaTodo()
    actualizarVidaPotencias()
    actualizarMuerte()
    reiniciarMisiles()
    reiniciarRegistro()
    reiniciarDisparosImpactos()
    reiniciarActividad()
    escribirPotencias()


# Retorna True si el string es un entero
# I: String
# O: Booleano
def isInteger(string):
    try:
        int(string)
        return True
    except:
        return False


# Crea una lista en formato de cantón
# E: un string y 12 números
# S: una lista en formato de cantón [Canton1, [[[P1],[P2]],[[P3],[P3]]]
def crearCanton(nombre, grados1x, minutos1x, segundos1x, grados1y, minutos1y, segundos1y, grados2x, minutos2x, segundos2x, grados2y, minutos2y, segundos2y):
    return [nombre, [[[grados1x, minutos1x, segundos1x],[grados1y, minutos1y, segundos1y]],[[grados2x, minutos2x, segundos2x],[grados2y, minutos2y, segundos2y]]]]


# Retorna TRUE si un punto está dentro de una región
# E: una lista en formato de punto y una lista en formato de región [[1,1,1],[2,2,2]] y [[[3,3,3],[4,4,4]],[[5,5,5],[6,6,6]]]
# S: un booleano
def puntoEnRegion(punto, region):
    puntoX = convertirAGrados(punto[0])
    puntoY = convertirAGrados(punto[1])
    esquina1X = convertirAGrados(region[0][0])
    esquina1Y = convertirAGrados(region[0][1])
    esquina2X = convertirAGrados(region[1][0])
    esquina2Y = convertirAGrados(region[1][1])
    if esquina1X >= esquina2X:
        if esquina1Y >= esquina2Y:
            return (esquina2X < puntoX < esquina1X) and (esquina2Y < puntoY < esquina1Y)
        return (esquina2X < puntoX < esquina1X) and (esquina1Y < puntoY < esquina2Y)
    else:
        if esquina1Y >= esquina2Y:
            return (esquina1X < puntoX < esquina2X) and (esquina2Y < puntoY < esquina1Y)
        return (esquina1X < puntoX < esquina2X) and (esquina1Y < puntoY < esquina2Y)


# Obtiene la esquina superior izquierda e inferior derecha de un territorio.
# E: una lista en formato de canton [Canton1, [[[P1],[P2]],[[P3],[P3]]]
# S: una lista con 2 pares de coordenadas en grados [[SI],[ID]]
def obtenerEsquinas(canton):
    x1 = convertirAGrados(canton[1][0][0])
    y1 = convertirAGrados(canton[1][0][1])
    x2 = convertirAGrados(canton[1][1][0])
    y2 = convertirAGrados(canton[1][1][1])
    if x1 > x2:
        if y1 > y2:
            SI = [[x2],[y1]]
            ID = [[x1],[y2]]
        else:
            SI = [[x2],[y2]]
            ID = [[x1],[y1]]
    else:
        if y1 > y2:
            SI = [[x1],[y1]]
            ID = [[x2],[y2]]
        else:
            SI = [[x1],[y1]]
            ID = [[x2],[y2]]
    return [SI,ID]


# Retorna True si el cantón se traslapa
# E: una lista en formato de canton [Canton1, [[[P1],[P2]],[[P3],[P3]]]
# S: un booleano
def cantonTraslapa(canton):
    global civilizaciones
    esquinasCanton = obtenerEsquinas(canton)
    for potencia in civilizaciones:
        for pais in potencia[7]:
            for provincia in pais[3]:
                for canton2 in provincia[1]:
                    if canton == canton2:
                        continue
                    if (esquinasCanton[0][0] > obtenerEsquinas(canton2)[1][0]) or (esquinasCanton[1][0] < obtenerEsquinas(canton2)[0][0]):
                        return [False]
                    if (esquinasCanton[0][1] < obtenerEsquinas(canton2)[1][1]) or (esquinasCanton[1][1] > obtenerEsquinas(canton2)[0][1]):
                        return [False]
                    return [True, canton, canton2]


# Revisa si todos los territorios no se traslapan
# S: un string
def revisarTerritorios():
    global civilizaciones
    for potencia in civilizaciones:
        for pais in potencia[7]:
            for provincia in pais[3]:
                for canton in provincia[1]:
                    chequeo = cantonTraslapa(canton)
                    if chequeo[0]:
                        return "ATENCIÓN! El cantón " + str(chequeo[1]) + " traslapa con " + str(chequeo[2])
    return "No se traslapa nada :)"


# Retorna True si solo queda una potencia viva y la potencia
# S: una lista con un booleano y un string
def esJuegoTerminado():
    global civilizaciones
    hay1 = [False]
    for potencia in civilizaciones:
        if potencia[3] and hay1[0]:
            return [False]
        if potencia[3]:
            hay1 = [True, potencia[0]]
    return [True, hay1[1]]


# Calcula la cantidad de potencias
# S: un número
def numPotencias():
    global civilizaciones
    contador = 0
    for potencia in civilizaciones:
        contador += 1
    return contador


# Avanza el turno y se devuelve a 0 si ya jugaron todas las potencias
def avanzarTurno():
    global turno
    turno += 1
    if turno == numPotencias():
            turno = 0


# Realiza todas las funciones que se tienen que hacer antes de comenzar el juego
def comenzarJuego():
    if civilizaciones == []:
        print("Error. No hay civilizaciones. Favor intentarlo de nuevo.")
        menu()
        return
    actualizar()
    print("Cargando") # Un cargando fake aquí pero es para que el usuario entienda que ya va a empezar el juego
    time.sleep(1.5)
    mainLoop()


# Retorna una coordenada con formato #º #’ #’’
# E: una lista en formato de coordenada [1, 2, 3]
# S: un string
def imprimirCoordenada(coord):
    return str(coord[0]) + "º " + str(coord[1]) + "’ " + str(coord[2]) + "’’"


# Elimina un a potencia de la lista
# E: un número (índice)
def eliminar(index):
    del civilizaciones[index]
    escribirPotencias()


# Cambia el estado de la potencia establecida
# E: un string (nombre de la potencia)
def cambiarEstado(nombre):
    for potencia in civilizaciones:
        if nombre == potencia[0]:
            if potencia[2] == "Activo":
                potencia[2] = "Inactivo"
            else:
                potencia[2] = "Activo"
            registroCambio()
            escribirPotencias()


# Obtiene la fecha y hora
def getDateTime():
    dt = datetime.now()
    return str(dt)[:19]


# Añade un evento de cambio al registro
def registroCambio():
    bitacora.append([getDateTime(), "CAMBIO", civilizaciones[turno][0] + " pasó a " + civilizaciones[turno][2].lower()])
    escribirRegistro()

# Añade un evento de ataque fallido al registro
# E: una lista en formato de punto (coordenadas)
def registroAtaqueMiss(punto):
    bitacora.append([getDateTime(), "ATAQUE", civilizaciones[turno][0] + " disparó en " + str(punto) + " y no atinó."])
    escribirRegistro()

# Añade un evento de ataque realizado al registro
# E: dos strings y una lista en formato de punto, opcional un booleano
def registroAtaqueHit(potencia, pais, punto, vidaAnterior = 0, vidaPosterior = 0, decrease= False):
    if decrease:
        bitacora.append([getDateTime(), "ATAQUE", civilizaciones[turno][0] + " disparó en " + str(punto) + " y atinó a " + potencia + " en " + pais + ". " + potencia + " pasó de " + str(vidaAnterior) + " a " + str(vidaPosterior) + "."])
        escribirRegistro()
    else:
        bitacora.append([getDateTime(), "ATAQUE", civilizaciones[turno][0] + " disparó en " + str(punto) + " y atinó a " + potencia + " en " + pais + ". La vida de " + potencia + " no baja porque el territorio ya tenía 0 de vida."])
        escribirRegistro()

# Añade un evento de territorio al registro
# E: dos strings
def registroTerritorio(potencia, pais):
    bitacora.append([getDateTime(), "TERRITORIO", potencia + ", " + pais + " llegó a 0%"])
    escribirRegistro()

# Añade un evento de muerte al registro
# E: un string
def registroMuerte(potencia):
    bitacora.append([getDateTime(), "MUERTE", potencia.upper()])
    escribirRegistro()

# Retorna una lista con todos los países.
# S: una lista con listas en formato de país
def crearListaPaises():
    global civilizaciones
    res = []
    for potencia in civilizaciones:
        for pais in potencia[7]:
            res.append(pais)
    return res


# Retorna la extensión de un pais
# E: una lista en formato de pais
# S: un numero
def getExtension(pais):
    return pais[2]


# Retorna la vida de un pais
# E: una lista en formato de pais
# S: un numero
def getEActiva(pais):
    return pais[1] * pais[2] * 0.01


# Le pone padding a la derecha a un string
# E: un número y un string
# S: none type
def padding(num, string):
    while len(string) <= num:
        string += " "
    return string


# Retorna una lista con True y el nombre de un canton si un misil le pega a una región, false si no
# E: una lista en formato de punto
# S: una lista
def misilHit(punto):
    for potencia in civilizaciones:
        for pais in potencia[7]:
            for provincia in pais[3]:
                for canton in provincia[1]:
                    if puntoEnRegion(punto, canton[1]):
                        return [True, canton[0]]
    registroAtaqueMiss(punto)
    print("\nNo se le atinó a nada :(")
    return [False]


# Realiza la accion de disparar un misil
# Una lista en formato de punto [[1,1,1],[2,2,2]]
def dispararMisil(punto):
    subirDisparo()
    res = misilHit(punto)
    if res[0]:
        hitActualizar(res[1], punto)
    escribirPotencias()


# Actualiza el número de disparos realizados y rebaja un misil a la potencia
def subirDisparo():
    global civilizaciones
    civilizaciones[turno][1] -= 1
    civilizaciones[turno][5] += 1


# Actualiza todo lo que pasa después de un disparo
# E: un string y una lista en formato de punto
def hitActualizar(string, punto):
    global civilizaciones
    for potencia in civilizaciones:
        for pais in potencia[7]:
            for provincia in pais[3]:
                for canton in provincia[1]:
                    if canton[0] == string:
                        print("\nSe le atinó a " + canton[0] + ", " + provincia[0] + ", " + pais[0] + "!!!!")
                        potencia[6] += 1

                        if pais[1] >= 10:
                            pais[1] -= 10
                            vidaAnterior = potencia[4]
                            actualizarVidaPotencias()
                            vidaPosterior = potencia[4]
                            registroAtaqueHit(potencia[0], pais[0], punto, vidaAnterior, vidaPosterior, True)

                            if pais[1] == 0:
                                registroTerritorio(potencia[0], pais[0])
                            if vidaPosterior == 0:
                                registroMuerte(potencia[0])
                                print("\n SE HA MUERTO LA POTENCIA: " + potencia[0].upper())
                                potencia[3] = False

                        else:
                            registroAtaqueHit(potencia[0], pais[0], punto)
                            print(pais[0] + " ya tenía 0 de vida. No se ha rebajado nada.")


# Retorna True si una potencia con el nombre potencia existe
# E: un string
# S: un booleano
def potenciaCheck(string):
    global civilizaciones
    for potencia in civilizaciones:
        if potencia[0].lower() == string:
            return True
    return False


# Retorna True si existe un pais de la potencia con el nombre establecido
# E: dos strings
# S: un booleano
def paisCheck(strPotencia, strPais):
    global civilizaciones
    for potencia in civilizaciones:
        if potencia[0].lower() == strPotencia:
            for pais in potencia[7]:
                if pais[0].lower() == strPais:
                    return True
    return False


# Retorna la cantidad de provincias de un pais
# E: dos strings
# S: un número
def cantidadProvincias(strPotencia, strPais):
    global civilizaciones
    res = 0
    for potencia in civilizaciones:
        if potencia[0] == strPotencia:
            for pais in potencia[7]:
                if pais[0] == strPais:
                    for provincia in pais[3]:
                        res += 1
    return res

# Retorna la cantidad de cantones de un pais
# E: dos strings
# S: un número
def cantidadCantones(strPotencia, strPais):
    global civilizaciones
    res = 0
    for potencia in civilizaciones:
        if potencia[0] == strPotencia:
            for pais in potencia[7]:
                if pais[0] == strPais:
                    for provincia in pais[3]:
                        for canton in provincia[1]:
                            res += 1
    return res


# Retorna la cantidad de paises de una potencia
# E: un string
# S: un número
def cantidadPaises(strPotencia):
    global civilizaciones
    res = 0
    for potencia in civilizaciones:
        if potencia[0] == strPotencia:
            for pais in potencia[7]:
                res += 1
    return res


# Retorna la suma de la vida de todos los territorios de una potencia
# E: un string
# S: un número
def sumaVidaTerritorios(strPotencia):
    global civilizaciones
    res = 0
    for potencia in civilizaciones:
        if potencia[0] == strPotencia:
            for pais in potencia[7]:
                res += pais[1]
    return res


# Compra una cantidad determinada de misiles y rebaja la vida
# E: un string y un número
def comprarMisiles(strPotencia, cantidad):
    global civilizaciones
    compras = cantidad / 100
    cantPaises = cantidadPaises(strPotencia)
    while compras > 0:
        territorio = civilizaciones[turno][7][random.randint(0, cantPaises -1)] # Randomiza el territorio a eliminar

        while not territorio[1] >= 10: # Busca un territorio con vida para quitar
            territorio = civilizaciones[turno][7][random.randint(0, cantPaises -1)]

        civilizaciones[turno][1] += 100
        territorio[1] -= 10

        if territorio[1] == 0:
            print("\n>>> AVISO: " + territorio[0] + " ha llegado a 0%.")
            registroTerritorio(strPotencia, territorio[0])

        escribirPotencias()

        compras -= 1





# PRINTS =====================================================================================================

# Imprime la información de todas las potencias
# S: none type
def consultarPotencias():
    for potencia in civilizaciones:
        print(potencia[0], "\t", potencia[1], "misiles\t", str(potencia[4]) + "% de vida", "\t\t\t", potencia[5], "disparos\t", potencia[6], "impactos\n\nTerritorios:")

        # Territorios
        index = 1
        for pais in potencia[7]:
            print(str(index) + ".", pais[0], "\t" + str(pais[1]) + "% de vida \t", str(pais[2]) + "km2")
            imprimirProvincias(pais[3])
            print()
            index += 1
        print("---")


# Imprime solamente los nombres de las potencias
# S: none type
def consultarNombres():
    contador = 1
    for potencia in civilizaciones:
        print(str(contador) + ".", potencia[0], end = "  ")
        contador += 1
    print("\n")


# Imprime el nombre de los cantones y sus esquinas
# E: una lista en formato de canton [[Canton1, [[[P1],[P2]],[[P3],[P3]]], [Canton2, [[P1],[P2],[P3],[P4]]], ...]
# S: none type
def imprimirCantones(cantones):
    for canton in cantones:
        print (canton[0] + " que va desde " + imprimirCoordenada(canton[1][0][0]) + ", " + imprimirCoordenada(canton[1][0][1]) + " hasta " + imprimirCoordenada(canton[1][1][0]) + ", " + imprimirCoordenada(canton[1][1][1]))


# Imprime los nombres la provincias y sus cantones
# E: una lista en formato provincia [[Provincia1, [Cantones] ], [Provincia2, [Cantones] ]]
# S: none type
def imprimirProvincias(provincias):
    for provincia in provincias:
        print(provincia[0])
        imprimirCantones(provincia[1])
        print()


# Imprime el nombre de la potencia que le toca
# S: none type
def imprimirTurno():
    print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Turno de la potencia:", civilizaciones[turno][0])
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")


# Imprime el ganador del juego
# S: none type
def finJuego():
    print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n-=-=-=   FIN DEL JUEGO   -=-=-=")
    time.sleep(1)
    print("\nHA GANDO LA POTENCIA:", esJuegoTerminado()[1])
    time.sleep(1)


# Imprime el registro
# S: none type
def imprimirRegistro():
    global bitacora
    for entry in bitacora:
        print(entry[0], "\t\t", entry[1], "\t\t", entry[2])


# Imprime el ranking por extension
# S: none type
def imprimirRankingExtension():
    print("\n~~~~Ranking por Extensión Completa~~~~\n")
    listaPaises = crearListaPaises()
    listaPaises.sort(key=getExtension, reverse= True)
    contador = 1
    for pais in listaPaises:
        print(str(contador) + ". " + padding(20, pais[0]) + "\t\t Extensión: " + str(pais[2]) + " km2" )
        contador += 1


# Imprime el ranking por vida
# S: none type
def imprimirRankingExtensionActiva():
    print("\n~~~~Ranking por Extensión Activa~~~~\n")
    listaPaises = crearListaPaises()
    listaPaises.sort(key=getEActiva, reverse= True)
    contador = 1
    for pais in listaPaises:
        print(str(contador) + ". " + padding(20, pais[0]) + "\t\t Vida: " + str(pais[1]) + "\t Extensión Activa: " + str(pais[1] * pais[2] * 0.01) + " km2" )
        contador += 1


# Imprime las instrucciones del juego
def imprimirInstrucciones():
    print("\n~~~~Instrucciones~~~~\n")
    print("Este juego trata de ser la última potencia viva. En su turno, va apoder elegir distintas acciones \ndigitando números. La forma de bajar vida a otras potencias es disparando un misil en uno de sus territorios.")


# Imprime el status de un territorio
# E: dos strings
def imprimirStatusPais(strPotencia, strPais):
    global civilizaciones
    for potencia in civilizaciones:
        if potencia[0].lower() == strPotencia:
            for pais in potencia[7]:
                if pais[0].lower() == strPais:
                    cantProvincias = str(cantidadProvincias(potencia[0], pais[0]))
                    cantCantones = str(cantidadCantones(potencia[0], pais[0]))
                    print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n" + potencia[0].upper() + ": " + pais[0].upper() + ":       Porcentaje de Vida: " + str(pais[1]) + " / Extensión Completa: " + str(pais[2]) + "km2 / Extensión Activa: " + str(pais[1] * 0.01 * pais[2]) + "km2 / Cantidad de Provincias: " + cantProvincias + " / Cantidad de Cantones: " + cantCantones + "\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")




# MENUS ===========================================

# Introducción
def intro():
    print("*****************************************************************************\n*********************************CONQUERORS**********************************\n*****************************************************************************")
    print("\nBienvenido a 'Conquerors'.\nSe ha dado una guerra por la posesión de territorios, en un mundo donde \nexisten de 2 hasta n grandes potencias, que son las que pelean por destruir y posteriormente \nposeer todo el territorio posible.")
    print("\nA continuación se presentará el menu principal con las opciones de lo que se puede hacer.")
    print("Buena suerte!")
    time.sleep(1)
    menu()

# Menu Principal
def menu():
    comenzado = False
    while not comenzado:
        print("\n****MENU PRINCIPAL****\n")
        print("1. Comenzar juego.")
        print("2. Insertar una nueva potencia.")
        print("3. Eliminar una potencia existente.")
        print("4. Consultar los nombres de las potencias a jugar.")
        print("5. Instrucciones.")
        num = input("\nInserte el número de la acción deseada: ")

        if num == "1":
            comenzado = True
            comenzarJuego()
        elif num == "2":
            print("\n---Insertar Potencia---\n")
            insertarPotencia()
        elif num == "3":
            print("\n---Eliminar Potencia---\n")
            menuEliminarPotencia()
        elif num == "4":
            print("\n---Potencias en el juego---\n")
            consultarNombres()
            time.sleep(4)
        elif num == "5":
            imprimirInstrucciones()
        else:
            print("!!! Error. Opción no encontrada. Favor intentarlo otra vez. !!!")


# Menu para eliminar una potencia
def menuEliminarPotencia():
    consultarNombres()
    res = input("Digite el número de la potencia a eliminar o '0' para salir de este menu. ")

    if not isInteger(res): # Validación
        print("\nError. Lo insertado no es válido. Favor intentarlo de nuevo.\n")
        return

    elif res == "0":
        pass

    elif int(res) in range(1, numPotencias() + 1):
        eliminar(int(res) - 1)

    else:
        print("\nError. El número no está en rango.\n")


# Menu de un turno
def mainLoop():
    global civilizaciones
    while not esJuegoTerminado()[0]:
        actualizarVidaPotencias()
        imprimirTurno()
        if civilizaciones[turno][4] == 0:
            print("Esta potencia está MUERTA...")
            avanzarTurno()
        elif civilizaciones[turno][2] == "Activo":
            print("1. Consultas. (no gastan un turno)")
            print("2. Cambiar estado. (Activo / Inactivo)")
            print("3. Disparar Misil.")
            print("4. Comprar Misiles.")

            num = input("\nInserte el número de la acción deseada: ")
            if num == "1":
                menuConsultas()
                time.sleep(1)
            elif num == "2":
                cambiarEstado(civilizaciones[turno][0])
                avanzarTurno()
                time.sleep(1)
            elif num == "3":
                    if civilizaciones[turno][1] == 0:                       # Validaciión de misiles
                        print("Error, no tiene misiles para disparar.")
                    else:
                        menuMisil()
                        avanzarTurno()
                        time.sleep(1)
            elif num == "4":
                menuCompra()
                avanzarTurno()
                time.sleep(1)
            else:
                print("!!! Error. Opción no encontrada. Favor intentarlo otra vez. !!!")
        else:
            print("*** Esta potencia se encuentra INACTIVA. Sus acciones son restringidas ***")
            print("1. Consultas. (no gastan un turno)")
            print("2. Cambiar estado. (Activo / Inactivo)")
            print("3. Saltar Turno.")

            num = input("\nInserte el número de la acción deseada: ")
            if num == "1":
                menuConsultas()
            elif num == "2":
                cambiarEstado(civilizaciones[turno][0])
                avanzarTurno()
            elif num == "3":
                avanzarTurno()
            else:
                print("!!! Error. Opción no encontrada. Favor intentarlo otra vez. !!!")

    finJuego()
    menuFinal()


# Menu de Compra de Misiles
def menuCompra():
    global civilizaciones
    print("\n---Compra de Misiles---\n")

    potencia = civilizaciones[turno][0]

    while True:
        cantidad = input("Digite un número entre 100 y 1000, múltiplo de 100: ")
        if not isInteger(cantidad):
            print("\n!!! ERROR. Lo digitado no es un número. Favor intentarlo otra vez. !!!\n")
        else:
            cantidad = int(cantidad)
            vidaARestar = cantidad / 10

            if not (1000 >= cantidad >= 100) or (not cantidad % 100 == 0):
                print("\n!!! ERROR. El número no cumple con las condiciones. Favor intentarlo otra vez. !!!\n")
            elif vidaARestar >= sumaVidaTerritorios(potencia):
                print("\n!!! ERROR. Esta compra mataría a la potencia. Favor inentar una cantidad más pequeña.\n")
            else:
                break

    comprarMisiles(potencia, cantidad)


# Menu de consultas
def menuConsultas():
    print("\n---Consultas---\n")
    print("1. Consultar información de las potencias")
    print("2. Consultar el registro")
    print("3. Consultar ranking de países por extensión completa")
    print("4. Consultar ranking de países por extensión activa")
    print("5. Consultar status de un país")

    num = input("\nInserte el número de la acción deseada: ")

    if num == "1":
        consultarPotencias()
    elif num == "2":
        imprimirRegistro()
    elif num == "3":
        imprimirRankingExtension()
    elif num == "4":
        imprimirRankingExtensionActiva()
    elif num == "5":
        menuStatusPais()
    else:
        print("!!! Error. Opción no encontrada. Favor intentarlo otra vez. !!!")


# Menu para ver el status de un país
def menuStatusPais():
    print("\n~~~~Status de un Territorio~~~~\n")

    while True:
        potencia = input("Ingrese el nombre de la potencia: ").lower()
        if not potenciaCheck(potencia):
            print("Potencia no encontrada. Favor intentarlo de nuevo.")
        else:
            break

    while True:
        pais= input("Ingrese el nombre del país: ").lower()
        if not paisCheck(potencia, pais):
            print("País no encontrado. Favor intentarlo de nuevo.")
        else:
            break

    imprimirStatusPais(potencia, pais)


# Menu que sale al final de un juego
def menuFinal():
    print("\nGracias por jugar!!")
    time.sleep(1)
    print("\nCREDITOS: Elaborado por Javier Carrillo\n")
    time.sleep(1)
    print("\nSi desea jugar otra vez, puede digitar 'intro()'. Note que esto reiniciará las potencias y borrará el registro.\n")

# Menu para disparar un misil
def menuMisil():
    print("\n~~~~Disparar Un Misil~~~~\n")

    while True:
        gradosX = input("Escriba los grados del eje x. ")
        if not isInteger(gradosX): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            gradosX = int(gradosX)
            if not 180 >= gradosX >= -180:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    while True:
        minutosX = input("Escriba los minutos del eje x. ")
        if not isInteger(minutosX): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            minutosX = int(minutosX)
            if not 60 >= minutosX >= 0:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    while True:
        segundosX = input("Escriba los segundos del eje x. ")
        if not isInteger(segundosX): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            segundosX = int(segundosX)
            if not 60 >= segundosX >= 0:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    ####### Y

    while True:
        gradosY = input("Escriba los grados del eje y. ")
        if not isInteger(gradosY): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            gradosY = int(gradosY)
            if not 90 >= gradosY >= -90:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    while True:
        minutosY = input("Escriba los minutos del eje y. ")
        if not isInteger(minutosY): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            minutosY = int(minutosY)
            if not 60 >= minutosY >= 0:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    while True:
        segundosY = input("Escriba los segundos del eje y. ")
        if not isInteger(segundosY): # Validacion
            print("Error. Favor intentarlo de nuevo.\n")
        else:
            segundosY = int(segundosY)
            if not 60 >= segundosY >= 0:
                print("Error. Favor intentarlo de nuevo.\n")
            else:
                break

    dispararMisil([[gradosX, minutosX, segundosX],[gradosY, minutosY, segundosY]])


# Menu para insertar una nueva potencia---------------------
# Agrega el resultado de crearPotencia a la lista
def insertarPotencia():
    global civilizaciones
    civilizaciones.append(crearPotencia())


# Le pide al usuario el nombre de la potencia y llama a crearPais las veces que se ocupe para crear el territorio
def crearPotencia():
    global civilizaciones
    res = ["nombre", 1000, "Activo", True, 100.0, 0, 0, []]
    nombrePotencia = input("Nombre de la Potencia? ")
    for potencia in civilizaciones:
        if nombrePotencia == potencia[0]:
            print("!!! Error. El nombre está repetido. Favor intentar otra vez. !!!")
            return
    res[0] = nombrePotencia
    otro = True
    while otro:
        pais = crearPais()
        if pais == None:
            return
        res[7].append(pais)
        otroPais = input("Quiere poner otro país? (poner 'y' o 'n') ")
        if otroPais == "n":
            otro = False
    return res


# Crea un pais con provincias, cantones y sus coordenadas
def crearPais():
    nombrePais = input("Nombre del Pais? ")
    res = [nombrePais, 0, 0]
    cantidadProvincias = input("Cuantas Provincias? ")

    if not isInteger(cantidadProvincias): # Validación
        print("\nError. Lo insertado no es válido. Favor intentarlo de nuevo.\n")
        return
    cantidadProvincias = int(cantidadProvincias)

    res.append([])
    while cantidadProvincias > 0:
        resProvincias = []
        nombreProvincia = input("Nombre Provincia? ")
        resProvincias.append(nombreProvincia)
        cantidadCantones = input("Cuantos Cantones? ")

        if not isInteger(cantidadCantones): # validacion
            print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
            return
        cantidadCantones = int(cantidadCantones)

        resProvincias.append([])
        while cantidadCantones > 0:
            nombreCantones = input("Nombre Canton? ")

            grados1x = input("Primer punto. Escriba los grados del eje x. ")
            if not isInteger(grados1x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            grados1x = int(grados1x)
            minutos1x = input("Primer punto. Escriba los minutos del eje x. ")
            if not isInteger(minutos1x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            minutos1x = int(minutos1x)
            segundos1x = input("Primer punto. Escriba los segundos del eje x. ")
            if not isInteger(segundos1x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            segundos1x = int(segundos1x)

            grados1y = input("Primer punto. Escriba los grados del eje y. ")
            if not isInteger(grados1y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            grados1y = int(grados1y)
            minutos1y = input("Primer punto. Escriba los minutos del eje y. ")
            if not isInteger(minutos1y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            minutos1y = int(minutos1y)
            segundos1y = input("Primer punto. Escriba los segundos del eje y. ")
            if not isInteger(segundos1y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            segundos1y = int(segundos1y)

            grados2x = input("Segundo punto. Escriba los grados del eje x. ")
            if not isInteger(grados2x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            grados2x = int(grados2x)
            minutos2x = input("Segundo punto. Escriba los minutos del eje x. ")
            if not isInteger(minutos2x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            minutos2x = int(minutos2x)
            segundos2x = input("Segundo punto. Escriba los segundos del eje x. ")
            if not isInteger(segundos2x): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            segundos2x = int(segundos2x)

            grados2y = input("Segundo punto. Escriba los grados del eje y. ")
            if not isInteger(grados2y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            grados2y = int(grados2y)
            minutos2y = input("Segundo punto. Escriba los minutos del eje y. ")
            if not isInteger(minutos2y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            minutos2y = int(minutos2y)
            segundos2y = input("Segundo punto. Escriba los segundos del eje y. ")
            if not isInteger(segundos2y): # Validacion
                print("Error. Lo insertado no es un número. Favor intentarlo de nuevo.\n")
                return
            segundos2y = int(segundos2y)

            canton = crearCanton(nombreCantones, grados1x, minutos1x, segundos1x, grados1y, minutos1y, segundos1y, grados2x, minutos2x, segundos2x, grados2y, minutos2y, segundos2y)

            if cantonTraslapa(canton)[0]: # Validación de que no se toque con nada
                print("Error. El cantón se encuentra traslapado. Favor intentarlo de nuevo.\n")
                return

            resProvincias[1].append(canton)
            cantidadCantones -= 1
        cantidadProvincias -= 1
        res[3].append(resProvincias)
    return res


intro()
