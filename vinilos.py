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
    print("")
    print("(1) Menu Inicio (2) Menu busqueda (3) Menu listado (4) Salir : ")
    print("")
    select = input("> ")

    if select == "1":
        iniciar()

    elif select == "2":
        buscar()

    elif select == "3":
        listar()

    elif select == "4":
        print("")
        print("Fin del programa")
        sys.exit()

    else:
        print("la opcion que has seleccionado no es valida")
        print("")
        seleccionar()


def iniciar():
    print("")
    print("Selecciona una opcion:")
    print("")
    print("1 - Registrar un vinilo en la BD")
    print("")
    print("2 - Busqueda Vinilos")
    print("")
    print("3 - Listado de Vinilos")
    print("")
    print("4 - Salir")
    print("")

    opcion = input("> ")

    if opcion == "1":
        print("")
        registrar()

    elif opcion == "2":
        print("")
        buscar()

    elif opcion == "3":
        print("")
        listar()

    elif opcion == "4":
        print("")
        print("Fin del programa")
        sys.exit()

    else:
        print("la opcion que has seleccionado no es valida")
        iniciar()


def registrar():
    print("")
    grupo = input("Introduzca el grupo/artista: ")
    grupo = grupo.title()
    print("")
    album = input("Introduzca el album: ")
    album = album.title()
    print("")
    year = (input("Introduzca el año: "))
    print("")
    genero = input("Introduzca el genero musical: ")
    print("")
    discografica = input("Introduzca la discografica: ")
    print("")
    obs = input("¿Comentarios?: ")
    print("")

    try:
        col.insert({'Grupo/Artista': (grupo), 'album': (album), 'Año': (year), 'Genero': (genero),
                    'Discografica': (discografica), 'Comentarios': (obs)})

        print("Datos Guardado con exito!")
        print("")
        print((col.count(), "Vinilos registrado en la base de datos"))
        print("")

        redata = input("¿Deseas registrar otro vinilo? s/n: ")
        print("")

        if redata.lower() == ("s"):
            registrar()
        seleccionar()

    except:
        print("'No ha sido posible conectar con la base de datos'")
        sys.exit()

    finally:
        print("")
        print("Fin del programa")
        print("")


def buscar():
    print("")
    print("Selecciona una opcion:")
    print("")
    print("1 - Busqueda de vinilos por Grupo/Artista")
    print("")
    print("2 - Busqueda Vinilos por Album")
    print("")
    print("3 - Busqueda Vinilos por Año")
    print("")
    print("4 - Menu Inicio")
    print("")

    opcion_busqueda = input("> ")

    if opcion_busqueda == "1":
        print("")
        print("digite el nombre del grupo/artista")
        print("")
        busca_nombre = input("> ")
        busca_nombre = {'Grupo/Artista': {"$regex": (busca_nombre), "$options": "i"}}

        for search in col.find(busca_nombre, projection={"_id": False}).sort(
                [('Grupo/Artista', pymongo.ASCENDING), ('Año', pymongo.ASCENDING)]):
            print(search)
            print("")
        print((col.count(busca_nombre), "Vinilos registrado en la base de datos"))
        print("")
        query_repeat = input("¿Deseas hacer otra consulta? s/n: ")
        print("")
        if query_repeat.lower() == ("s"):
            buscar()

    elif opcion_busqueda == "2":
        print("")
        print("digite el nombre del Album")
        print("")
        busca_album = input("> ")
        busca_album = {'album': {"$regex": (busca_album), "$options": "i"}}

        for search in col.find(busca_album, projection={"_id": False}).sort(
                [('Grupo/Artista', pymongo.ASCENDING), ('Año', pymongo.ASCENDING)]):
            print(search)
            print("")
        print((col.count(busca_album), "Vinilos registrado en la base de datos"))
        print("")
        query_repeat = input("¿Deseas hacer otra consulta? s/n: ")
        print("")

        if query_repeat.lower() == ("s"):
            buscar()

    elif opcion_busqueda == "3":
        print("")
        print("digite el año del disco")
        print("")
        busca_año = input("> ")
        busca_año = {'Año': {"$regex": (busca_año), "$options": "i"}}

        for search in col.find(busca_año, projection={"_id": False}).sort(
                [('Año', pymongo.ASCENDING), ('Grupo/Artista', pymongo.ASCENDING)]):
            print(search)
            print("")
        print((col.count(busca_año), "Vinilos registrado en la base de datos"))
        print("")
        query_repeat = input("¿Deseas hacer otra consulta? s/n: ")
        print("")

        if query_repeat.lower() == ("s"):
            buscar()

    elif opcion_busqueda == "4":
        iniciar()


    else:
        print("la opcion que has seleccionado no es valida")
        buscar()
    seleccionar()


def listar():
    print("")
    print("Selecciona una opcion:")
    print("")
    print("1 - listado completo de los vinilos")
    print("")
    print("2 - Total de vinilos por grupo")
    print("")
    print("3 - Listar albums por grupos")
    print("")
    print("4 - Listar albums por año")
    print("")
    print("5 - Menu Inicio")
    print("")

    opcion_avan = input("> ")

    if opcion_avan == "1":
        for listado in col.find(projection={"_id": False}).sort('Grupo/Artista', pymongo.ASCENDING):
            print(listado)
            print("")


    elif opcion_avan == "2":
        for listado in col.aggregate([{"$group": {"_id": {"Grupo": "$Grupo/Artista"}, "Discos": {"$sum": 1}}},
                                      {"$project": {"Grupo": 1, "Discos": 1}},
                                      {"$sort": {"Grupo": 1, "Discos": 1}}]):
            print(listado)
            print("")

    elif opcion_avan == "3":
        for listado in col.aggregate([{"$group": {"_id": {"Grupo": "$Grupo/Artista"}, "Albums": {"$push": "$album"}}},
                                      {"$project": {"Grupo": 1, "Albums": 1}},
                                      {"$sort": {"Grupo": 1}}]):
            print(listado)
            print("")


    elif opcion_avan == "4":
        for listado in col.aggregate(
                [{"$group": {"_id": {"Album": "$album", "Year": "$Año", "Grupo": "$Grupo/Artista"}}},
                 {"$project": {"Year": 1, "Grupo": 1, "Album": 1}},
                 {"$sort": {"Year": 1}}]):
            print(listado)
            print("")

    elif opcion_avan == "5":
        iniciar()

    else:
        print("la opcion que has seleccionado no es valida")
        listar()

    print("")
    print((col.count(), "Vinilos registrado en la base de datos"))
    print("")
    query_repeat = input("¿Deseas hacer otra consulta de listado? s/n: ")
    print("")
    if query_repeat.lower() == ("s"):
        listar()
    seleccionar()


bienvenido()
iniciar()
print("")
print("Gracias y Hasta Luego")
