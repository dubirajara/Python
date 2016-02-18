import sys
import pymongo

con = pymongo.MongoClient("localhost", 27017)
db = con.vinilos
col = db.discos


def bienvenido():
    texto = """
===============================
Catalogador de Discos Vinilos
===============================
"""
    print(texto.center(50))


def seleccionar():
    print("\n(1) Menu Inicio (2) Menu busqueda (3) Menu listado (4) Salir: \n")
    select = input("> ")

    if select == "1":
        iniciar()

    elif select == "2":
        buscar()

    elif select == "3":
        listar()

    elif select == "4":
        print("\nFin del programa")
        sys.exit()

    else:
        print("la opcion que has seleccionado no es valida\n")
        seleccionar()


def iniciar():
    print("\nSelecciona una opcion:\n\n")
    print("1 - Registrar un vinilo en la BD\n")
    print("2 - Busqueda Vinilos\n")
    print("3 - Listado de Vinilos\n")
    print("4 - Salir\n")

    opcion = input("> ")

    if opcion == "1":
        registrar()

    elif opcion == "2":
        buscar()

    elif opcion == "3":
        listar()

    elif opcion == "4":
        print("\nFin del programa")
        sys.exit()

    else:
        print("la opcion que has seleccionado no es valida")
        iniciar()


def registrar():
    grupo = input("\nIntroduzca el grupo/artista: \n")
    grupo = grupo.title()
    album = input("Introduzca el album: \n")
    album = album.title()
    year = (input("Introduzca el año: \n"))
    genero = input("Introduzca el genero musical: \n")
    discografica = input("Introduzca la discografica: \n")
    obs = input("¿Comentarios?: \n")

    try:
        col.insert({'Grupo/Artista': (grupo), 'album': (album), 'Año': (year),
                    'Genero': (genero), 'Discografica': (discografica),
                    'Comentarios': (obs)})

        print("Datos Guardado con exito!\n")
        print((col.count(), "Vinilos registrado en la base de datos"))

        redata = input("\n¿Deseas registrar otro vinilo? s/n: \n")

        if redata.lower() == "s":
            registrar()
        seleccionar()

    except:
        print('No ha sido posible conectar con la base de datos')
        sys.exit()

    finally:
        print("\nFin del programa\n")


def buscar():
    print("\nSelecciona una opcion:\n\n")
    print("1 - Busqueda de vinilos por Grupo/Artista\n")
    print("2 - Busqueda Vinilos por Album\n")
    print("3 - Busqueda Vinilos por Año\n")
    print("4 - Menu Inicio\n")

    opcion_busqueda = input("> ")

    if opcion_busqueda == "1":
        print("\ndigite el nombre del grupo/artista:\n")
        busca_nombre = input("> ")
        busca_nombre = {'Grupo/Artista': {"$regex": (busca_nombre),
                        "$options": "i"}}

        for search in col.find(busca_nombre, projection={"_id": False}).sort(
                [('Grupo/Artista', pymongo.ASCENDING),
                 ('Año', pymongo.ASCENDING)]):
            print(search)
        print((col.count(busca_nombre), "Vinilos registrado"))
        query_repeat = input("\n¿Deseas hacer otra consulta? s/n: ")
        if query_repeat.lower() == "s":
            buscar()

    elif opcion_busqueda == "2":
        print("\ndigite el nombre del Album:\n")
        busca_album = input("> ")
        busca_album = {'album': {"$regex": (busca_album), "$options": "i"}}

        for search in col.find(busca_album, projection={"_id": False}).sort(
                [('Grupo/Artista', pymongo.ASCENDING),
                 ('Año', pymongo.ASCENDING)]):
            print(search)
        print((col.count(busca_album), "Vinilos registrado"))
        query_repeat = input("\n¿Deseas hacer otra consulta? s/n: ")
        print()

        if query_repeat.lower() == "s":
            buscar()

    elif opcion_busqueda == "3":
        print("\ndigite el año del disco:\n")
        busca_año = input("> ")
        busca_año = {'Año': {"$regex": (busca_año), "$options": "i"}}

        for search in col.find(busca_año, projection={"_id": False}).sort([
                ('Año', pymongo.ASCENDING),
                ('Grupo/Artista', pymongo.ASCENDING)]):
            print(search)
        print((col.count(busca_año), "Vinilos registrado en la base de datos"))
        query_repeat = input("\n¿Deseas hacer otra consulta? s/n: ")

        if query_repeat.lower() == "s":
            buscar()

    elif opcion_busqueda == "4":
        iniciar()
    else:
        print("la opcion que has seleccionado no es valida")
        buscar()
    seleccionar()


def listar():
    print("\nSelecciona una opcion:\n\n")
    print("1 - listado completo de los vinilos\n")
    print("2 - Total de vinilos por grupo\n")
    print("3 - Listar albums por grupos\n")
    print("4 - Listar albums por año\n")
    print("5 - Menu Inicio\n")

    opcion_avan = input("> ")

    if opcion_avan == "1":
        for listado in col.find(projection={"_id": False}).sort(
                                'Grupo/Artista', pymongo.ASCENDING):
            print(listado)
            print()

    elif opcion_avan == "2":
        for listado in col.aggregate(
                [{"$group": {"_id": {"Grupo": "$Grupo/Artista"},
                 "Discos": {"$sum": 1}}},
                 {"$project": {"Grupo": 1, "Discos": 1}},
                 {"$sort": {"Grupo": 1, "Discos": 1}}]):
            print(listado)
            print()

    elif opcion_avan == "3":
        for listado in col.aggregate(
                [{"$group": {"_id": {"Grupo": "$Grupo/Artista"},
                 "Albums": {"$push": "$album"}}},
                 {"$project": {"Grupo": 1, "Albums": 1}},
                 {"$sort": {"Grupo": 1}}]):
            print(listado)
            print()

    elif opcion_avan == "4":
        for listado in col.aggregate(
                [{"$group": {"_id": {"Album": "$album", "Year": "$Año",
                 "Grupo": "$Grupo/Artista"}}},
                 {"$project": {"Year": 1, "Grupo": 1, "Album": 1}},
                 {"$sort": {"Year": 1}}]):
            print(listado)
            print()

    elif opcion_avan == "5":
        iniciar()

    else:
        print("la opcion que has seleccionado no es valida")
        listar()

    print((col.count(), "Vinilos registrado en la base de datos"))
    query_repeat = input("\n¿Deseas hacer otra consulta de listado? s/n: \n")
    if query_repeat.lower() == "s":
        listar()
    seleccionar()


bienvenido()
iniciar()
