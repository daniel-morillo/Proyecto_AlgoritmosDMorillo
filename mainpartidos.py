import requests
import json
from clases_equipos import Equipo
from clases_estadios import Estadio, Producto, Alimento, Bebida, Restaurant, Producto_comprado, Producto_conteo
from clases_partidos import Partido
from clase_cliente import Cliente, Boleto
import itertools 

boletos_emitidos = []
clientes_totales = []
obj_partidos = []
partidos = []
obj_estadios = []
estadios = []
equipos = []
obj_equipos = []
restaurants = []
productos_totales = []
productos_obj = []
restaurants_obj = []
todos_productos = []

def matchcard(equipo_local,equipo_visitante,estadio_jugar,hora_fecha,id_jugar): #Esta funcion imprime los partidos de manera ordenada
    print("-"*60)
    print((equipo_local + " vs " + equipo_visitante).center(60," "))
    print((estadio_jugar).center(60," "))
    print((hora_fecha).center(60," "))
    print((id_jugar).center(60," "))
    print("-"*60)

def perfect(num):  #Funcion de numeros perfectos
    divisores_sumados = 0
    for i in range(1,num - 1):
        if num % i == 0:
            divisores_sumados += i
    if divisores_sumados == num:
        return True
    else:
        return False

def crear_estadio(nombre,ubicacion,capacidad,id):   #Crea el estadio
    nuevo_estadio = Estadio(nombre,ubicacion,capacidad,id)
    estadios.append(nuevo_estadio.mostrar_estadio())
    obj_estadios.append(nuevo_estadio)
    return nuevo_estadio

def crear_equipo(nombre,fifa,grupo,id):   #Crea el equipo
    nuevo_equipo = Equipo(nombre,fifa,grupo,id)
    equipos.append(nuevo_equipo.mostrar_equipo())
    obj_equipos.append(nuevo_equipo)
    return nuevo_equipo
    
def colmillos(numero):   #Primera parte de los numeros vampiros (obtiene los colmillos para poder realizar la siguiente accion)
    numero_permutado = itertools.permutations(numero, len(numero))
    for lista_numeros in numero_permutado:
        pegado = ''.join(lista_numeros)
        x , y = pegado[:int(len(pegado)/2)], pegado[int(len(pegado)/2):]
        if x[-1] == '0' and y[-1] == '0':
            continue
        if int(x) * int(y) == int(numero):
            return x,y
    return False

def vampiro(numero_prueba): #Segund aparte, si obtiene colmillos de la funcion anterior, este numero es vampiro
    prueba_string = str(numero_prueba)
    if len(prueba_string) % 2 == 1:
        return False
    colmillos_prueba = colmillos(prueba_string)
    if not colmillos_prueba:
        return False
    return True
    

def main():
    
    vips_totales = 0
    gastado_vipers = 0
    #Obtener información de las APIs
    url_equipos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/teams.json"
    getear_equipos = requests.get(url_equipos)

    if getear_equipos.status_code == 200:
        contenido_equipos = getear_equipos.content
        archivo_equipos = open("equipos.json","wb")
        archivo_equipos.write(contenido_equipos)
        archivo_equipos.close()

    url_estadios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/stadiums.json"
    getear_estadios = requests.get(url_estadios)

    if getear_estadios.status_code == 200:
        contenido_estadios = getear_estadios.content
        archivo_estadios = open("estadios.json","wb")
        archivo_estadios.write(contenido_estadios)
        archivo_estadios.close()
    
    url_partidos = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-1/api-proyecto/main/matches.json"
    getear_partidos = requests.get(url_partidos)

    if getear_partidos.status_code == 200:
        contenido_partidos = getear_partidos.content
        archivo_partidos = open("partidos.json","wb")
        archivo_partidos.write(contenido_partidos)
        archivo_partidos.close()

    #Crear los respectivos objetos 
    arc_equipos = open("equipos.json")
    data_equipos = json.load(arc_equipos)
    arc_partidos = open("partidos.json")
    data_partidos = json.load(arc_partidos)
    arc_estadios = open("estadios.json")
    data_estadios = json.load(arc_estadios)

    for i in range(0,len(data_equipos)):
        nombre = data_equipos[i]["name"]
        fifa = data_equipos[i]["fifa_code"]
        grupo = data_equipos[i]["group"]
        id = data_equipos[i]["id"]
        crear_equipo(nombre,fifa,grupo,id)

    
    for i in range(0,len(data_estadios)):
        nombre_estadio = data_estadios[i]["name"]
        ubicacion = data_estadios[i]["location"]
        capacidad = data_estadios[i]["capacity"]
        id_estadio = data_estadios[i]["id"]
        crear_estadio(nombre_estadio,ubicacion,capacidad,id_estadio)
        
    for i in data_partidos:
        for equipo in obj_equipos:
            if equipo.nombre == i["home_team"]:
                local = equipo
            elif equipo.nombre == i["away_team"]:
                visitante = equipo
        fecha = i["date"]
        for estadio in obj_estadios:
            if estadio.id == i["stadium_id"]:
                valid_estadio = estadio
        id_match = i["id"]
        nuevo_partido = Partido(local,visitante,fecha,valid_estadio,id_match,0,0)
        obj_partidos.append(nuevo_partido)
        mostrar_local = nuevo_partido.home.nombre
        mostrar_visitante = nuevo_partido.away.nombre
        mostrar_fecha = nuevo_partido.fecha
        mostrar_estadio = nuevo_partido.estadio.mostrar_estadio()
        mostrar_id = nuevo_partido.id
        partidazo = f"{mostrar_local} vs {mostrar_visitante} el {mostrar_fecha} en {mostrar_estadio} codigo: {mostrar_id}"
        partidos.append(partidazo)

    #Gestion de restaurantes
    for i in data_estadios:
        restaurantes = i["restaurants"]
        for restaurants in restaurantes:
            for key,value in restaurants.items():
                if key == "products":
                    for producto in value:
                        restaurante_disponible = restaurants.get("name")
                        name = producto.get("name")
                        precio_unidad = producto.get("price")
                        clasificacion = producto.get("type")
                        inventario = producto.get("quantity")
                        if clasificacion == "beverages":
                            if producto.get("name") == "Beer":
                                nuevo_producto = Bebida(name,clasificacion,precio_unidad,restaurante_disponible,inventario,True)
                            else:
                                nuevo_producto = Bebida(name,clasificacion,precio_unidad,restaurante_disponible,inventario,False)
                        elif clasificacion == "food":
                            adicional = producto.get("adicional")
                            nuevo_producto = Alimento(name,clasificacion,precio_unidad,restaurante_disponible,inventario,adicional)
                        productos_obj.append(nuevo_producto)
                        ver_producto = f"{name} disponible en: {restaurante_disponible} tipo: {clasificacion} precio: {precio_unidad}"
                        productos_totales.append(ver_producto)
    for i in data_estadios:
        productos_restaurant = []
        restaurants = i["restaurants"]
        for restaurant in restaurants:
            for producto in productos_obj:
                if producto.restaurant_dispo == restaurant.get("name"):
                    productos_restaurant.append(producto)
            nuevo_restaurant = Restaurant(restaurant.get("name"),i["id"],productos_restaurant)
            restaurants_obj.append(nuevo_restaurant)
    

                




    #MENU
    print("-"*100)
    print("BIENVENIDO".center(100,"♦"))
    print("-"*100)
    while True:
        print("-----------------------------------------------------------------------")
        opcion = input("\nIntroduce una de las opciones validas a continuacion:\n1-Informacion de Equipos, Estadios y Partidos\n2-Venta de entradas\n3-Informacion de Restaurantes y Productos\n4-Comprar Refrigerios\n5-Gestor de Entradas y Asistencia\n6-Estadisticas\n7-Salir\n-->")
        print("-----------------------------------------------------------------------")
        if opcion.isnumeric():
            #MODULO 1
            if int(opcion) == 1:
                print("-"*60)
                print("Bienvenido a la seccion de informacion de partidos".center(60,"↓"))
                print("-"*60)
                opcion2 = input("Introduce una de las opciones validas a continuacion:\n1-Todos los Partidos de un Pais\n2-Todos los Partidos de un Estadio\n3-Todos los Partidos de una Fecha\n-->")
                print("-"*60)
                if opcion2.isnumeric():
                    if int(opcion2) == 1:
                        print("-"*60)
                        pais_selected = input("De cual pais quieres ver sus partidos?\n-->") #Seleccionar un pais en ingles
                        for match in obj_partidos:
                            if match.home.nombre == pais_selected.capitalize() or match.away.nombre == pais_selected.capitalize():
                                mostrar_local = match.home.nombre
                                mostrar_visitante = match.away.nombre
                                mostrar_fecha = match.fecha
                                mostrar_estadio = match.estadio.nombre
                                mostrar_id = match.id
                                matchcard(mostrar_local,mostrar_visitante,mostrar_estadio,mostrar_fecha,mostrar_id)
                    elif int(opcion2) ==2:  #Seleccionar el id del estadio
                        print("-"*60)
                        estadio_selected = int(input("Introduce el ID del estadio del cual quieras ver sus partidos\n-->"))
                        for match in obj_partidos:
                            if match.estadio.id == estadio_selected:
                                mostrar_local = match.home.nombre
                                mostrar_visitante = match.away.nombre
                                mostrar_fecha = match.fecha
                                mostrar_estadio = match.estadio.nombre
                                mostrar_id = match.id
                                matchcard(mostrar_local,mostrar_visitante,mostrar_estadio,mostrar_fecha,mostrar_id)
                                
                    elif int(opcion2) ==3:  #Filtro señalando fecha y hora
                        print("-"*60)
                        fecha_selected = input("Introduce la fecha de los partidos que quieras ver en formato: DD/MM/AAAA HH:MM \n-->")
                        for match in obj_partidos:
                            if match.fecha == fecha_selected:
                                mostrar_local = match.home.nombre
                                mostrar_visitante = match.away.nombre
                                mostrar_fecha = match.fecha
                                mostrar_estadio = match.estadio.nombre
                                mostrar_id = match.id
                                matchcard(mostrar_local,mostrar_visitante,mostrar_estadio,mostrar_fecha,mostrar_id)
            #MODULO 2
            if int(opcion) == 2:
                print("-"*60)
                print("Bienvenido a la seccion de venta de entradas".center(60,"♦"))
                print("-"*60)
                descuento = 0
                precio_total = 0
                nombre_cliente = input("Por favor introduce tu nombre\n-->")
                print("-"*60)
                cedula_cliente = input("Introduce tu numero de cedula o ID\n-->")
                print("-"*60)
                entradas_cliente = []
                if cedula_cliente.isnumeric():
                    cedula_cliente = int(cedula_cliente) 
                    edad_cliente = input("Introduce tu edad\n-->")
                    print("-"*60)
                    while True:  #Este while true es para que el cliente pueda comprar mas de una entrada
                        for partido in partidos:
                            print(f"{partido}\n")
                        partido_compra = input("Introduce el codigo de partido que quieras comprar")
                        print("-"*60)
                        if partido_compra.isnumeric():
                            for match in obj_partidos:
                                if match.id == partido_compra:
                                    mostrar_local = match.home.nombre
                                    mostrar_visitante = match.away.nombre
                                    mostrar_fecha = match.fecha
                                    mostrar_estadio = match.estadio.nombre
                                    mostrar_id = match.id
                                    matchcard(mostrar_local,mostrar_visitante,mostrar_estadio,mostrar_fecha,mostrar_id)
                                    puestos_vip_estadio = match.estadio.puestos_vip
                                    puestos_gral_estadio = match.estadio.puestos_general
                            iva = 0.16
                            print(f"Entradas Generales disponibles: {puestos_gral_estadio}\n")
                            print(f"Entradas VIP disponibles: {puestos_vip_estadio}\n")
                            vip = input("Selecciona: \n1-Entrada VIP\n2-Entrada General\n-->")
                            print("-"*60)
                            while not vip == "1" and not vip == "2":
                                vip = input("Selecciona: \n1-Entrada VIP\n2-Entrada General\n-->")
                            cantidad_entradas = input("Cuantos puestos de ese tipo quieres comprar?\n")
                            print("-"*60)
                            while not cantidad_entradas.isnumeric():
                                cantidad_entradas = input("Cuantos puestos de ese tipo quieres comprar?\n")
                            
                            if int(vip) == 1:
                                while not int(cantidad_entradas) <= puestos_vip_estadio:
                                    cantidad_entradas = input("Cuantos puestos de ese tipo quieres comprar?\n")
                                precio = 120 * int(cantidad_entradas)
                                entrada_cliente = "VIP"
                            elif int(vip) ==2:
                                while not int(cantidad_entradas) <= puestos_gral_estadio:
                                    cantidad_entradas = input("Cuantos puestos de ese tipo quieres comprar?\n")
                                precio = 50 * int(cantidad_entradas)
                                entrada_cliente = "General"
                            precio_total += precio + precio*iva
                            if vampiro(cedula_cliente) == True:
                                descuento = precio * 0.5
                            precio_total -= descuento
                            print("-"*60)
                            print(f"Cliente: {nombre_cliente}\nNumero de Cedula del Cliente: {cedula_cliente}\nAsientos: {cantidad_entradas}\nDescuento Aplicado: {descuento}\nTotal a Pagar:{precio_total}") #Esto es una factura previa
                            print("-"*60)
                            if input("Presiona Y para continuar, para cancelar pulsa cualquier otro caracter") == "Y":
                                print("-"*60)
                                print("COMPRA EXITOSA, LO ESPERAMOS!\n")
                                print("-"*60)
                                codigo_bol = str(cedula_cliente)+str(partido_compra)
                                nuevo_boleto = Boleto(codigo_bol,entrada_cliente,int(partido_compra),int(cantidad_entradas))
                                entradas_cliente.append(nuevo_boleto)
                                boletos_emitidos.append(nuevo_boleto)
                                print("-"*60)
                                print(f"Cliente: {nombre_cliente}\nNumero de Cedula del Cliente: {cedula_cliente}\nAsientos: {cantidad_entradas}\nDescuento Aplicado: {descuento}\nTotal Pagado:{precio_total}\n\nCodigo de partido: {codigo_bol}\n") #Esto si es la factura factura
                                print("-"*60)
                            if input("Presiona Y para continuar comprando, para cancelar pulsa cualquier otro caracter") != "Y":
                                nuevo_cliente = Cliente(nombre_cliente,edad_cliente,cedula_cliente,entradas_cliente)
                                clientes_totales.append(nuevo_cliente)
                                cont_vip = 0
                                for entrada in nuevo_cliente.entradas:
                                    if entrada.tipo == "VIP":
                                        cont_vip += 1
                                        gastado_vipers += precio_total
                                        for partido in obj_partidos:
                                            if int(entrada.id_partido) == int(partido.id):
                                                partido.estadio.puestos_vip -= int(cantidad_entradas)
                                if cont_vip > 0:
                                    vips_totales += 1
                                    if entrada.tipo == "General":
                                        for partido in obj_partidos:
                                            if int(entrada.id_partido) == int(partido.id):
                                                partido.estadio.puestos_general -= int(cantidad_entradas)

                                break


                            
            #MODULO 3 (Ver productos de restaurantes)
            if int(opcion) == 3:
                estadio_rest = input("Introduce el ID del partido al que vayas a asisitir\n-->")
                while not estadio_rest.isnumeric():
                    estadio_rest = input("ERROR Introduce el ID del partido al que vayas a asisitir\n-->")
                for match in obj_partidos:
                    if estadio_rest == match.id:
                        for restaurante in restaurants_obj:
                            if restaurante.estadio_id == match.estadio.id:
                                for producto in restaurante.productos:
                                    print("-"*30)
                                    producto.mostrar_producto()
                                    print("-"*30)
                                if input("Presiona f si quieres añadir un filtro a tu compra, para continuar usa cualquier otra tecla").capitalize() == "F":
                                    filtro = input("Selecciona una de las siguientes opciones:\n1-Buscar por nombre\n2-Buscar por tipo\n3-Buscar por rango de precio\n-->")  #Filtros para busqueda
                                    while not filtro.isnumeric():
                                        filtro = input("Selecciona una de las siguientes opciones:\n1-Buscar por nombre\n2-Buscar por tipo\n-Buscar por rango de precio\n-->")
                                    if int(filtro) == 1:
                                        error_filtro = 0
                                        filtro_nombre = input("Introduce el nombre de lo que quieras buscar\n-->")
                                        for producto in restaurante.productos:
                                            if filtro_nombre.capitalize() == producto.nombre.capitalize():
                                                print("-"*40)
                                                producto.mostrar_producto()
                                                print("-"*40)
                                                error_filtro += 1
                                        if error_filtro == 0:
                                            print("-"*30)
                                            print("Lo sentimos no tenemos ningun producto con ese nombre")
                                            print("-"*30)

                                    elif int(filtro) == 2:
                                        filtro_tipo = input("Selecciona una opcion:\n1--Comida\n2--Bebida\n-->")
                                        while not filtro_tipo.isnumeric:
                                            filtro_tipo = input("Selecciona una opcion:\n1--Comida\n2--Bebida\n-->")
                                        if int(filtro_tipo) == 1:
                                            for producto in restaurante.productos:
                                                if producto.clasificacion == "food":
                                                    print("-"*40)
                                                    producto.mostrar_producto()
                                                    print("-"*40)
                                        if int(filtro_tipo) == 2:
                                            for producto in restaurante.productos:
                                                if producto.clasificacion == "beverages":
                                                    print("-"*40)
                                                    producto.mostrar_producto()
                                                    print("-"*40)
                                    elif int(filtro) == 3:
                                        minimo = input("Introduce el costo minimo del producto\n-->")
                                        maximo = input("Introduce el costo maximo del producto\n-->")
                                        while not minimo.isnumeric() and maximo.isnumeric():
                                            minimo = input("Introduce el costo minimo del producto\n-->")
                                            maximo = input("Introduce el costo maximo del producto\n-->")
                                        for producto in restaurante.productos:
                                            if producto.precio <= float(maximo) and producto.precio >= float(minimo):
                                                print("-"*40)
                                                producto.mostrar_producto()
                                                print("-"*40)
            #Modulo 4 (Venta de restaurantes)
            elif int(opcion) == 4:
                carrito = []
                validar_cedula = input("Introduce tu cedula\n")
                while not validar_cedula.isnumeric():
                    validar_cedula = input("Introduce tu cedula\n")
                for cliente in clientes_totales:
                    if int(cliente.cedula) == int(validar_cedula):
                        for entrada in cliente.entradas:
                            if entrada.tipo == "VIP":
                                print(" Bienvenido a la Seccion de Venta de Produtos ".center(60,"♦"))
                                validar_edad = cliente.edad
                                estadio_rest = int(entrada.id_partido)

                                for match in obj_partidos:
                                    if estadio_rest == int(match.id):
                                        for restaurante in restaurants_obj:
                                            if restaurante.estadio_id == match.estadio.id:
                                                print("-"*40)
                                                print(f"Bienvenido a {restaurante.nombre} en el estadio {match.estadio.nombre}")
                                                print("-"*40)
                                                if input("Desea comprar algo?\n1-Si\n2-No") == "1":
                                                    while True:
                                                        if int(validar_edad) < 18:
                                                            for producto in restaurante.productos:
                                                                if producto.nombre != "Beer":
                                                                    producto.mostrar_producto()
                                                        else: 
                                                            for producto in restaurante.productos:
                                                                producto.mostrar_producto()
                                                        compra = input("Introduce el nombre del producto que quieras adquirir\n-->")
                                                        cantidad = input("Cuantas unidades de este producto deseas?\n-->")
                                                        while not cantidad.isnumeric():
                                                            cantidad = input("Cuantas unidades de este producto deseas?\n-->")
                                                        for producto in restaurante.productos:
                                                            if compra.capitalize() == producto.nombre:
                                                                if int(cantidad) > int(producto.inventario):
                                                                    print("Lo sentimos no tenemos esa cantidad de producto :(\n")
                                                                else:
                                                                    precio_mult = int(cantidad) * producto.precio
                                                                    nueva_compra = Producto_comprado(compra,producto.clasificacion,producto.precio,restaurante.nombre,cantidad,precio_mult)
                                                                    carrito.append(nueva_compra)
                                                        monto = 0
                                                        descuento = 0
                                                        monto_pagar = 0
                                                        for compra in carrito:
                                                            monto += compra.precio_total
                                                        if perfect(int(validar_cedula)):
                                                            descuento += monto * 0.15
                                                            descuento = round(descuento,2)
                                                        for compra in carrito:
                                                            compra.mostrar_producto_comprado()
                                                        monto_pagar = monto - descuento
                                                        print(f"Monto total: {monto}\n")
                                                        print(f"Descuento: {descuento}\n")
                                                        print(f"Monto a Pagar: {monto_pagar}\n")  #Factura previa
                                                        if input("Presione p para pagar, presione otra tecla para cancelar\n") == "p":
                                                            gastado_vipers += monto_pagar
                                                            print(" FACTURA ".center(40,"♦"))  #Factura real
                                                            print(f"Monto total: {monto}\n")
                                                            print(f"Descuento: {descuento}\n")
                                                            print(f"Monto a Pagar: {monto_pagar}\n")
                                                            print(" PAGO EXITOSO ".center(40,"♦"))
                                                            print("\n")
                                                            for restaurante in restaurants_obj:
                                                                for compra in carrito:
                                                                    for producto in restaurante.productos:
                                                                        if compra.restaurant_dispo == restaurante.nombre and compra.nombre == producto.nombre:  #Aqui se restan objetos del inventario de cada producto
                                                                            producto.inventario -= int(compra.cantidad)
                                                            if input("Presiona c para seguir comprando, presiona otra tecla para terminar con la compra\n") != "c":
                                                                break
                    else:                     
                        print("\nLo siento, primero compra una entrada VIP\n")
            #Modulo 5 (Autorización de boletos)
            elif int(opcion) == 5:
                print("Bienvenido a la autorizacion de boletos".center(60,"♦"))
                print("-"*60)
                boleto_examinar = input("Introduce el codigo de tu boleto\n-->")
                for boleto in boletos_emitidos:
                    if boleto_examinar == str(boleto.codigo):
                        partido_espectado = str(boleto.id_partido) 
                        for partido in obj_partidos:
                            if partido_espectado == str(partido.id):
                                partido.asistencia += boleto.puestos
                        print("-"*60)
                        print("BIENVENIDO, que disfrute el partido".center(60,"♦"))
                        print("-"*60)
                        boletos_emitidos.remove(boleto)
                    else:
                        print("Lo sentimos, el boleto no está autorizado\n")
            #Modulo 6 (Stats)
            elif int(opcion) == 6:
                cliente_top1 = Cliente("sierra",20,200,[])
                cliente_top2 = Cliente("hotel",20,200,[])
                cliente_top3 = Cliente("india",20,200,[])
                #Promedio de gastos de vips
                if vips_totales > 0:
                    print(f"El gasto promedio de un cliente vip es de: {gastado_vipers/vips_totales}")
                mayor_asistencia = Partido("Italia","Venezuela",12,49,49,0,0)  #Este partido es fake, es para que el if dentro del for pueda iterar normalmente
                asistencia_top2 = Partido("Italia","Venezuela",12,49,49,0,0)  #Este partido es fake, es para que el if dentro del for pueda iterar normalmente
                asistencia_top3 = Partido("Italia","Venezuela",12,49,49,0,0)  #Este partido es fake, es para que el if dentro del for pueda iterar normalmente
                for partido in obj_partidos:
                    if partido.asistencia > mayor_asistencia.asistencia:
                        mayor_asistencia = partido
                if mayor_asistencia.asistencia != 0:
                    print(f"El partido con mayor asistencia fue {mayor_asistencia.home.nombre} vs {mayor_asistencia.away.nombre} con {mayor_asistencia.asistencia} espectadores")

                #Partido más vendido
                for boleto in boletos_emitidos:
                    for partido in obj_partidos:
                        if int(boleto.id_partido) == int(partido.id):
                            partido.vendido += int(boleto.puestos)
                partido_mas_vendido = obj_partidos[0]
                for partido in obj_partidos:
                    if partido.vendido > partido_mas_vendido.vendido:
                        partido_mas_vendido = partido
                if partido_mas_vendido.vendido > 0:
                    print(f"El partido mas vendido fue {partido_mas_vendido.home.nombre} vs {partido_mas_vendido.away.nombre} con {partido_mas_vendido.vendido} puestos vendidos\n")
                #Top 3 partidos más vendidos
                for cliente in clientes_totales:
                    entradas_totales = 0
                    for entrada in cliente.entradas:
                        entradas_totales += entrada.puestos
                    if entradas_totales > len(cliente_top1.entradas):
                        cliente_top3 = cliente_top2
                        cliente_top2 = cliente_top1
                        cliente_top1 = cliente
                    elif entradas_totales <= len(cliente_top1.entradas) and entradas_totales >= len(cliente_top2):
                        cliente_top3 = cliente_top2
                        cliente_top2 = cliente
                    elif entradas_totales <= len(cliente_top2.entradas) and entradas_totales >= len(cliente_top3):
                        cliente_top3 = cliente
                if len(cliente_top1.entradas) > 0 :
                    print("-"*60)
                    print(f"El cliente con mas entradas compradas es: ")
                    cliente_top1.datazos()
                    print("-"*60)
                if len(cliente_top2.entradas) > 0 and cliente_top1 != cliente_top2:
                    print("-"*60)
                    print(f"El segundo cliente con mas entradas compradas es: ")
                    cliente_top2.datazos()
                    print("-"*60)
                if len(cliente_top3.entradas) > 0 and cliente_top2 != cliente_top3:
                    print("-"*60)
                    print(f"El tercer cliente con mas entradas compradas es: ")
                    cliente_top3.datazos()
                    print("-"*60)
                
                #Top partidos más vistos
                asistencia_top1 = mayor_asistencia
                for partido in obj_partidos:
                    if partido.asistencia >= asistencia_top1.asistencia:
                        asistencia_top3 = asistencia_top2
                        asistencia_top2 = asistencia_top1
                        asistencia_top1 = partido
                    elif partido.asistencia <= asistencia_top1.asistencia and partido.asistencia >= asistencia_top2.asistencia:
                        asistencia_top3 = asistencia_top2
                        asistencia_top2 = partido
                    elif partido.asistencia <= asistencia_top2.asistencia and partido.asistencia >= asistencia_top3.asistencia:
                        asistencia_top3 = partido
                if asistencia_top1.asistencia > 0:
                    print("-"*60)
                    print("El partido con mas asistencia fue: ")
                    asistencia_top1.partiti()
                    print(f"Con {asistencia_top1.asistencia} espectadores")
                    print("-"*60)
                if asistencia_top2.asistencia > 0:
                    print("-"*60)
                    print(f"El segundo partido con mas asistencia fue: ")
                    asistencia_top2.partiti()
                    print(f"Con {asistencia_top2.asistencia} espectadores")
                    print("-"*60)
                if asistencia_top3.asistencia > 0:
                    print("-"*60)
                    print(f"El tercer partido con mas asistencia fue: ")
                    asistencia_top3.partiti()
                    print(f"Con {asistencia_top3.asistencia} espectadores")
                    print("-"*60)
                
                #Productos más comprados (No tengo la más mínima idea de por que no funcionó)
                producto_top1 = Producto_conteo("alpha",0)#Productos fake para ser reconocidos por el bucle for sin problema
                producto_top2 = Producto_conteo("beta",0)
                producto_top3 = Producto_conteo("delta",0)
                for producto in productos_obj:
                    new_product = Producto_conteo(producto.nombre,25 - int(producto.inventario))
                    
                    for product in todos_productos:
                        if product.nombre == new_product.nombre:
                            product.comprado += new_product.comprado
                        else:
                            todos_productos.append(new_product)
                
                for product in todos_productos:
                    if product.comprado >= producto_top1.comprado:
                        producto_top3 = producto_top2
                        producto_top2 = producto_top1
                        producto_top1 = product
                    elif product.comprado <= producto_top1.comprado and product.comprado >= producto_top2.comprado:
                        producto_top3 = producto_top2
                        producto_top2 = product
                    elif product.comprado <= producto_top2.comprado and producto.comprado >= producto_top3.comprado:
                        producto_top3 = product
                if producto_top1.comprado > 0:
                    print("-"*60)
                    print(f"El producto mas comprado fue {producto_top1.nombre} con {producto_top1.comprado} productos")
                    print("-"*60)
                if producto_top2.comprado > 0:
                    print("-"*60)
                    print(f"El segundo producto mas comprado fue {producto_top2.nombre} con {producto_top2.comprado} productos")
                    print("-"*60)
                if producto_top3.comprado > 0:
                    print("-"*60)
                    print(f"El tercer producto mas comprado fue {producto_top1.nombre} con {producto_top3.comprado} productos")
                    print("-"*60)
                #Aqui lo que traté de hacer es apoyarme de esos productos falsos como en las stats anteriores, además como el inventariio de todos los objetos es 25, traté de que su cantidad sea la resta de 25 - lo que hay en el inventario e iterar de esa manera :(

            #Salida
            elif int(opcion) == 7:
                print("-"*60)
                print(" ESPERAMOS VOLVER A VERLO ".center(60,"♦"))
                print("-"*60)

                    
main()