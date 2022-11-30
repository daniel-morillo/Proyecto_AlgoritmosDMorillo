class Equipo:
    def __init__(self,nombre,fifa,grupo, id):
        self.nombre = nombre
        self.fifa = fifa
        self.grupo = grupo
        self.id = id

    def mostrar_equipo(self):
        return self.nombre,self.fifa,self.grupo,self.id
