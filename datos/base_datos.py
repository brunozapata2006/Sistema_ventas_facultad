import mysql.connector
from objetos.zapatilla import Zapatilla
from objetos.venta import Venta


class BaseDatosMySQL:
    def __init__(self):
        self.servidor = "localhost"
        self.usuario = "root"
        self.contrasenia = "ifts9"
        self.nombre_base_datos = "iftsnueve"
        self.esta_conectado = self.inicializar_mysql()

    def conectar_base_datos(self):
        conexion = mysql.connector.connect(
            host=self.servidor,
            user=self.usuario,
            password=self.contrasenia,
            database=self.nombre_base_datos
        )
        return conexion

    def inicializar_mysql(self):
        try:
            conexion_servidor = mysql.connector.connect(
                host=self.servidor,
                user=self.usuario,
                password=self.contrasenia
            )
            cursor_servidor = conexion_servidor.cursor()
            consulta_crear_db = "CREATE DATABASE IF NOT EXISTS " + self.nombre_base_datos
            cursor_servidor.execute(consulta_crear_db)
            cursor_servidor.close()
            conexion_servidor.close()

            conexion_db = self.conectar_base_datos()
            cursor_db = conexion_db.cursor()
            consulta_tabla_zapatillas = """
                CREATE TABLE IF NOT EXISTS zapatillas (
                    id INT PRIMARY KEY,
                    marca VARCHAR(50) NOT NULL,
                    modelo VARCHAR(50) NOT NULL,
                    talle INT NOT NULL,
                    precio INT NOT NULL,
                    stock INT NOT NULL
                )
            """
            cursor_db.execute(consulta_tabla_zapatillas)

            consulta_tabla_ventas = """
                CREATE TABLE IF NOT EXISTS ventas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_zapatilla INT NOT NULL,
                    cantidad INT NOT NULL,
                    precio_unitario INT NOT NULL,
                    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_zapatilla) REFERENCES zapatillas(id)
                )
            """
            cursor_db.execute(consulta_tabla_ventas)

            cursor_db.close()
            conexion_db.close()
            print("Conectado a MySQL. Base de datos lista !!!")
            return True
        except Exception:
            print("AVISO: MySQL no está activo. El sistema funcionará sin base de datos (en memoria).")
            return False

    def sincronizar_zapatillas(self, lista_zapatillas_iniciales):
        if not self.esta_conectado:
            return lista_zapatillas_iniciales

        if lista_zapatillas_iniciales is None or len(lista_zapatillas_iniciales) == 0:
            return []

        try:
            conexion = self.conectar_base_datos()
            cursor = conexion.cursor()

            consulta_basura = "SELECT COUNT(*) FROM zapatillas WHERE marca IN ('1', '11', '') OR modelo IN ('1', '5', '11', '')"
            cursor.execute(consulta_basura)
            resultado_basura = cursor.fetchone()
            cantidad_basura = resultado_basura[0]

            if cantidad_basura > 0:
                cursor.execute("DELETE FROM ventas")
                cursor.execute("DELETE FROM zapatillas")

            consulta_insertar = "INSERT IGNORE INTO zapatillas (id, marca, modelo, talle, precio, stock) VALUES (%s, %s, %s, %s, %s, %s)"
            for zapatilla_actual in lista_zapatillas_iniciales:
                valores_zapatilla = (
                    zapatilla_actual.id_zapatilla,
                    zapatilla_actual.marca,
                    zapatilla_actual.modelo,
                    zapatilla_actual.talle,
                    zapatilla_actual.precio,
                    zapatilla_actual.stock
                )
                cursor.execute(consulta_insertar, valores_zapatilla)

            conexion.commit()

            consulta_traer = "SELECT id, marca, modelo, talle, precio, stock FROM zapatillas ORDER BY id ASC"
            cursor.execute(consulta_traer)
            filas_zapatillas = cursor.fetchall()

            cursor.close()
            conexion.close()

            lista_zapatillas_db = []
            for fila_zapatilla in filas_zapatillas:
                id_zapatilla = fila_zapatilla[0]
                marca = fila_zapatilla[1]
                modelo = fila_zapatilla[2]
                talle = fila_zapatilla[3]
                precio = fila_zapatilla[4]
                stock = fila_zapatilla[5]

                objeto_zapatilla = Zapatilla(
                    marca,
                    modelo,
                    talle,
                    precio,
                    stock,
                    id_zapatilla
                )
                lista_zapatillas_db.append(objeto_zapatilla)

            return lista_zapatillas_db
        except Exception:
            print("AVISO: No se pudo sincronizar con MySQL. Se usarán los datos locales.")
            self.esta_conectado = False
            return lista_zapatillas_iniciales

    def guardar_zapatilla(self, zapatilla_nueva):
        if not self.esta_conectado:
            return False

        if zapatilla_nueva is None:
            return False

        try:
            conexion = self.conectar_base_datos()
            cursor = conexion.cursor()

            consulta_insertar_zapatilla = "INSERT INTO zapatillas (id, marca, modelo, talle, precio, stock) VALUES (%s, %s, %s, %s, %s, %s)"
            valores_zapatilla = (
                zapatilla_nueva.id_zapatilla,
                zapatilla_nueva.marca,
                zapatilla_nueva.modelo,
                zapatilla_nueva.talle,
                zapatilla_nueva.precio,
                zapatilla_nueva.stock
            )
            cursor.execute(consulta_insertar_zapatilla, valores_zapatilla)

            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Exception:
            print("AVISO: Error al guardar la zapatilla en MySQL. Quedó registrada solo en memoria.")
            self.esta_conectado = False
            return False

    def guardar_venta(self, venta_nueva):
        if not self.esta_conectado:
            return None

        if venta_nueva is None or venta_nueva.zapatilla is None:
            return None

        try:
            conexion = self.conectar_base_datos()
            cursor = conexion.cursor()

            consulta_insertar_venta = "INSERT INTO ventas (id_zapatilla, cantidad, precio_unitario) VALUES (%s, %s, %s)"
            valores_venta = (
                venta_nueva.zapatilla.id_zapatilla,
                venta_nueva.cantidad,
                venta_nueva.precio_unitario
            )
            cursor.execute(consulta_insertar_venta, valores_venta)
            nuevo_id_venta = cursor.lastrowid

            consulta_actualizar_stock = "UPDATE zapatillas SET stock = %s WHERE id = %s"
            valores_stock = (
                venta_nueva.zapatilla.stock,
                venta_nueva.zapatilla.id_zapatilla
            )
            cursor.execute(consulta_actualizar_stock, valores_stock)

            conexion.commit()
            cursor.close()
            conexion.close()
            return nuevo_id_venta
        except Exception:
            print("AVISO: Error al guardar en MySQL. La venta quedó registrada solo en memoria.")
            self.esta_conectado = False
            return None

    def traer_ventas(self, lista_zapatillas):
        if not self.esta_conectado:
            return []

        if lista_zapatillas is None or len(lista_zapatillas) == 0:
            return []

        try:
            conexion = self.conectar_base_datos()
            cursor = conexion.cursor()

            consulta_traer_ventas = "SELECT id, id_zapatilla, cantidad, precio_unitario, fecha FROM ventas ORDER BY id ASC"
            cursor.execute(consulta_traer_ventas)
            filas_ventas = cursor.fetchall()

            cursor.close()
            conexion.close()

            lista_ventas_db = []
            for fila_venta in filas_ventas:
                id_venta = fila_venta[0]
                id_zapatilla_buscada = fila_venta[1]
                cantidad = fila_venta[2]
                precio_unitario = fila_venta[3]
                fecha = str(fila_venta[4])

                zapatilla_encontrada = None
                for zapatilla_actual in lista_zapatillas:
                    if zapatilla_actual.id_zapatilla == id_zapatilla_buscada:
                        zapatilla_encontrada = zapatilla_actual
                        break

                if zapatilla_encontrada is not None:
                    objeto_venta = Venta(
                        zapatilla_encontrada,
                        cantidad,
                        precio_unitario,
                        fecha,
                        id_venta
                    )
                    lista_ventas_db.append(objeto_venta)

            return lista_ventas_db
        except Exception:
            print("AVISO: No se pudieron traer las ventas desde MySQL.")
            self.esta_conectado = False
            return []

    def borrar_venta(self, id_venta_borrar, zapatilla_afectada):
        if not self.esta_conectado:
            return

        if id_venta_borrar is None or id_venta_borrar <= 0:
            return

        try:
            conexion = self.conectar_base_datos()
            cursor = conexion.cursor()

            consulta_borrar_venta = "DELETE FROM ventas WHERE id = %s"
            cursor.execute(consulta_borrar_venta, (id_venta_borrar,))

            if zapatilla_afectada is not None:
                consulta_restaurar_stock = "UPDATE zapatillas SET stock = %s WHERE id = %s"
                valores_stock = (
                    zapatilla_afectada.stock,
                    zapatilla_afectada.id_zapatilla
                )
                cursor.execute(consulta_restaurar_stock, valores_stock)

            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception:
            print("AVISO: Error al borrar en MySQL. La venta se eliminó solo de la memoria.")
            self.esta_conectado = False
