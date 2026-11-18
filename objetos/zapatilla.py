class Zapatilla:
    def __init__(self, marca, modelo, talle, precio, stock, id_zapatilla=None):
        self.id_zapatilla = id_zapatilla
        self.marca = marca
        self.modelo = modelo
        self.talle = talle
        self.precio = precio
        self.stock = stock

    def hay_stock(self, cantidad_solicitada):
        if cantidad_solicitada <= 0:
            return False
        if self.stock >= cantidad_solicitada:
            return True
        else:
            return False

    def descontar_stock(self, cantidad_vendida):
        if cantidad_vendida > 0 and self.stock >= cantidad_vendida:
            self.stock = self.stock - cantidad_vendida
            return True
        else:
            return False

    def aumentar_stock(self, cantidad_devuelta):
        if cantidad_devuelta > 0:
            self.stock = self.stock + cantidad_devuelta
            return True
        else:
            return False

    def ver_datos(self):
        print(
            self.id_zapatilla,
            self.marca,
            self.modelo,
            self.talle,
            self.precio,
            self.stock,
            sep=" - "
        )
