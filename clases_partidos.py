class Partido:
    def __init__(self, home, away, fecha, estadio, id,asistencia, vendido):
        self.home = home
        self.away = away
        self.fecha = fecha
        self.estadio = estadio
        self.id = id
        self.asistencia = asistencia
        self.vendido = vendido
    def mostrar_partido(self):
        return self.home,self.away,self.fecha,self.estadio,self.id
    def partiti(self):
        print(f"{self.home.nombre} vs {self.home.nombre}")

