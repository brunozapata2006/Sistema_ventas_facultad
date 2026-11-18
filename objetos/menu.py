from objetos.zapatilla import Zapatilla
from objetos.venta import Venta
from datos.base_datos import BaseDatosMySQL


class Menu:
    def __init__(self, zapatillas_iniciales):
        self.base_datos = BaseDatosMySQL()
        if zapatillas_iniciales is None:
            self.lista_zapatillas = []
        else:
            self.lista_zapatillas = self.base_datos.sincronizar_zapatillas(zapatillas_iniciales)

        self.lista_ventas = self.base_datos.traer_ventas(self.lista_zapatillas)

    def generar_id_venta(self):
        if len(self.lista_ventas) == 0:
            return 1

        id_mayor = 0
        for venta_actual in self.lista_ventas:
            if venta_actual.id_venta is not None and venta_actual.id_venta > id_mayor:
                id_mayor = venta_actual.id_venta

        nuevo_id = id_mayor + 1
        return nuevo_id

    def buscar_zapatilla_por_id(self, id_zapatilla_buscada):
        if id_zapatilla_buscada is None or id_zapatilla_buscada <= 0:
            return None

        for zapatilla_actual in self.lista_zapatillas:
            if zapatilla_actual.id_zapatilla == id_zapatilla_buscada:
                return zapatilla_actual
        return None

    def buscar_venta_por_id(self, id_venta_buscada):
        if id_venta_buscada is None or id_venta_buscada <= 0:
            return None

        for venta_actual in self.lista_ventas:
            if venta_actual.id_venta == id_venta_buscada:
                return venta_actual
        return None

    def pedir_numero_entero(self, mensaje, valor_minimo):
        texto_ingresado = input(mensaje).strip()
        while not texto_ingresado.isdigit() or int(texto_ingresado) < valor_minimo:
            print("ERROR !!! debe ingresar un número entero mayor o igual a", valor_minimo)
            texto_ingresado = input(mensaje).strip()

        numero_valido = int(texto_ingresado)
        return numero_valido

    def pedir_texto_no_vacio(self, mensaje):
        texto_ingresado = input(mensaje).strip()
        while texto_ingresado == "":
            print("ERROR !!! el campo no puede estar vacío")
            texto_ingresado = input(mensaje).strip()

        return texto_ingresado

    def verificar_stock_general(self):
        if len(self.lista_zapatillas) == 0:
            return False

        for zapatilla_actual in self.lista_zapatillas:
            if zapatilla_actual.stock > 0:
                return True
        return False

    def registrar_zapatilla(self):
        id_ingresado = self.pedir_numero_entero("Ingrese el ID para la nueva zapatilla: ", 1)
        zapatilla_existente = self.buscar_zapatilla_por_id(id_ingresado)

        while zapatilla_existente is not None:
            print("ERROR !!! ya existe una zapatilla con el ID", id_ingresado)
            id_ingresado = self.pedir_numero_entero("Ingrese otro ID disponible: ", 1)
            zapatilla_existente = self.buscar_zapatilla_por_id(id_ingresado)

        marca_ingresada = self.pedir_texto_no_vacio("Ingrese la Marca: ")
        modelo_ingresado = self.pedir_texto_no_vacio("Ingrese el Modelo: ")
        talle_ingresado = self.pedir_numero_entero("Ingrese el Talle: ", 1)
        precio_ingresado = self.pedir_numero_entero("Ingrese el Precio en pesos (sin centavos): ", 1)
        stock_ingresado = self.pedir_numero_entero("Ingrese el Stock: ", 0)

        nueva_zapatilla = Zapatilla(
            marca_ingresada,
            modelo_ingresado,
            talle_ingresado,
            precio_ingresado,
            stock_ingresado,
            id_ingresado
        )

        self.base_datos.guardar_zapatilla(nueva_zapatilla)
        self.lista_zapatillas.append(nueva_zapatilla)
        print("Zapatilla registrada con ID:", nueva_zapatilla.id_zapatilla)
        nueva_zapatilla.ver_datos()

    def mostrar_zapatillas(self):
        if len(self.lista_zapatillas) == 0:
            print("ERROR !!! no hay zapatillas disponibles para mostrar")
            return

        print("\nLista completa de zapatillas:")
        print("ID - Marca - Modelo - Talle - Precio - Stock")
        print("----------------------------------------------------------------------")
        for zapatilla_actual in self.lista_zapatillas:
            zapatilla_actual.ver_datos()

    def buscar_zapatillas_por_marca(self):
        if len(self.lista_zapatillas) == 0:
            print("ERROR !!! no hay zapatillas registradas para buscar")
            return

        marca_buscada = self.pedir_texto_no_vacio("Ingrese la marca a buscar (ej: Nike, Adidas, Puma): ")
        marca_buscada_minuscula = marca_buscada.lower()

        zapatillas_coincidentes = []
        for zapatilla_actual in self.lista_zapatillas:
            marca_actual_minuscula = zapatilla_actual.marca.lower()
            if marca_buscada_minuscula in marca_actual_minuscula:
                zapatillas_coincidentes.append(zapatilla_actual)

        if len(zapatillas_coincidentes) == 0:
            print("ERROR !!! no se encontraron zapatillas de la marca:", marca_buscada)
            return

        print("\nResultados encontrados para la marca '" + marca_buscada + "':")
        print("ID - Marca - Modelo - Talle - Precio - Stock")
        print("----------------------------------------------------------------------")
        for zapatilla_filtrada in zapatillas_coincidentes:
            zapatilla_filtrada.ver_datos()

    def registrar_venta(self):
        if not self.verificar_stock_general():
            print("ERROR !!! no hay zapatillas con stock disponible para vender")
            return

        self.mostrar_zapatillas()
        id_zapatilla = self.pedir_numero_entero("Ingrese el ID de la zapatilla a vender: ", 1)
        zapatilla_seleccionada = self.buscar_zapatilla_por_id(id_zapatilla)

        if zapatilla_seleccionada is None:
            print("ERROR !!! no existe una zapatilla con ese ID")
            return

        if zapatilla_seleccionada.stock <= 0:
            print("ERROR !!! la zapatilla seleccionada no tiene stock disponible")
            return

        cantidad_a_vender = self.pedir_numero_entero("Ingrese la cantidad a vender: ", 1)
        nueva_venta = Venta(zapatilla_seleccionada, cantidad_a_vender, zapatilla_seleccionada.precio)

        if not nueva_venta.realizar_venta():
            print("ERROR !!! stock insuficiente. Stock disponible:", zapatilla_seleccionada.stock)
            return

        id_generado_mysql = self.base_datos.guardar_venta(nueva_venta)
        if id_generado_mysql is not None:
            nueva_venta.id_venta = id_generado_mysql
        else:
            nueva_venta.id_venta = self.generar_id_venta()

        self.lista_ventas.append(nueva_venta)
        total_calculado = nueva_venta.calcular_total()
        print("Venta registrada !!!")
        print("ID Zapatilla vendida:", zapatilla_seleccionada.id_zapatilla, "-", zapatilla_seleccionada.marca, zapatilla_seleccionada.modelo)
        print("Total de la venta:", total_calculado)
        print("Stock restante:", zapatilla_seleccionada.stock)

    def ver_ventas(self):
        if len(self.lista_ventas) == 0:
            print("ERROR !!! no hay ventas registradas para mostrar")
            return

        print("\nLista de ventas:")
        print("ID Venta - Fecha - ID Zapatilla - Marca - Modelo - Talle - Cantidad - Precio unitario - Total")
        print("-----------------------------------------------------------------------------------------------")
        for venta_actual in self.lista_ventas:
            if venta_actual.zapatilla is not None:
                total_venta = venta_actual.calcular_total()
                print(
                    venta_actual.id_venta,
                    venta_actual.fecha,
                    venta_actual.zapatilla.id_zapatilla,
                    venta_actual.zapatilla.marca,
                    venta_actual.zapatilla.modelo,
                    venta_actual.zapatilla.talle,
                    venta_actual.cantidad,
                    venta_actual.precio_unitario,
                    total_venta,
                    sep=" - "
                )

    def borrar_venta(self):
        if len(self.lista_ventas) == 0:
            print("ERROR !!! no hay ventas registradas para borrar")
            return

        self.ver_ventas()
        id_venta = self.pedir_numero_entero("Ingrese el ID de la venta a borrar: ", 1)
        venta_encontrada = self.buscar_venta_por_id(id_venta)

        if venta_encontrada is None:
            print("ERROR !!! no existe una venta con ese ID")
            return

        if venta_encontrada.zapatilla is not None:
            venta_encontrada.zapatilla.aumentar_stock(venta_encontrada.cantidad)

        self.base_datos.borrar_venta(id_venta, venta_encontrada.zapatilla)
        self.lista_ventas.remove(venta_encontrada)
        print("Venta borrada y stock restaurado !!!")
