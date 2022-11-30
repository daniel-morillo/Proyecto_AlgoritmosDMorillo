class Cliente:
    def __init__(self, nombre, edad, cedula, entradas):
        self.nombre = nombre
        self.edad = edad
        self.cedula = cedula
        self.entradas = entradas
    def datazos(self):
        print(f"Cliente: {self.nombre}\nCedula: {self.cedula}\nBoletos comprados: {len(self.entradas)}")


class Boleto:
    def __init__(self, codigo, tipo, id_partido,puestos):
        self.codigo = codigo
        self.tipo = tipo
        self.id_partido = id_partido
        self.puestos = puestos