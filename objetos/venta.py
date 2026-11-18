from datetime import datetime


class Venta:
    def __init__(self, zapatilla, cantidad, precio_unitario, fecha=None, id_venta=None):
        self.id_venta = id_venta
        self.zapatilla = zapatilla
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        if fecha is not None and fecha != "":
            self.fecha = fecha
        else:
            fecha_actual = datetime.now()
            self.fecha = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

    def calcular_total(self):
        if self.cantidad <= 0 or self.precio_unitario <= 0:
            return 0
        total_venta = self.cantidad * self.precio_unitario
        return total_venta

    def realizar_venta(self):
        if self.zapatilla is None:
            return False
        if self.cantidad <= 0:
            return False

        tiene_stock_disponible = self.zapatilla.hay_stock(self.cantidad)
        if tiene_stock_disponible:
            descuento_aplicado = self.zapatilla.descontar_stock(self.cantidad)
            return descuento_aplicado
        else:
            return False
