class Estadio:
    def __init__(self, nombre, ubicacion, capacidad, id):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        self.puestos_general = capacidad[0]
        self.puestos_vip = capacidad[1]
        self.id = id
    def mostrar_estadio(self):
        return self.nombre,self.ubicacion,self.capacidad,self.id

class Restaurant:
    def __init__(self,nombre,estadio_id, productos):
        self.nombre = nombre
        self.estadio_id = estadio_id
        self.productos = productos

class Producto:
    def __init__(self, nombre, clasificacion, precio,restaurant_dispo,cantidad):
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.precio = precio
        self.restaurant_dispo = restaurant_dispo
        self.inventario = cantidad
    def mostrar_producto(self):
        print(f"Nombre del producto: {self.nombre}\nClasificacion: {self.clasificacion}\nPrecio: {self.precio}\nCantidad en el Inventario {self.inventario}\n")

class Alimento(Producto):
    def __init__(self, nombre, clasificacion, precio, restaurant_dispo, cantidad,adicional):
        super().__init__(nombre, clasificacion, precio, restaurant_dispo, cantidad)
        self.adicional = adicional

class Bebida(Producto):
    def __init__(self, nombre, clasificacion, precio, restaurant_dispo, cantidad,alcohol):
        super().__init__(nombre, clasificacion, precio, restaurant_dispo, cantidad)
        self.adicional = alcohol

class Producto_comprado(Producto):
    def __init__(self, nombre, clasificacion, precio, restaurant_dispo,cantidad, precio_total):
        super().__init__(nombre, clasificacion, precio, restaurant_dispo, cantidad)
        self.cantidad = cantidad
        self.precio_total = precio_total
    def mostrar_producto_comprado(self):
        print(f"Nombre del producto: {self.nombre}\nClasificacion: {self.clasificacion}\nPrecio Unitario: {self.precio}\nCantidad: {self.cantidad}\nPrecio Total: {self.precio_total}\n")

class Producto_conteo:
    def __init__(self, nombre, comprado):
        self.nombre = nombre
        self.comprado = comprado

