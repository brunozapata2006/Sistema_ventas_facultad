import sys
import os

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

from objetos.zapatilla import Zapatilla
from objetos.menu import Menu


def menu():
    zapatillas_iniciales = [
        Zapatilla("Nike", "Air Force 1", 42, 145000, 12, id_zapatilla=1),
        Zapatilla("Nike", "Air Max 90", 41, 165000, 8, id_zapatilla=2),
        Zapatilla("Nike", "Dunk Low", 40, 155000, 10, id_zapatilla=3),
        Zapatilla("Nike", "Air Jordan 1 Mid", 43, 195000, 5, id_zapatilla=4),
        Zapatilla("Nike", "Pegasus 40", 42, 150000, 14, id_zapatilla=5),
        Zapatilla("Nike", "Blazer Mid 77", 39, 135000, 9, id_zapatilla=6),
        Zapatilla("Nike", "Air Max 270", 44, 175000, 6, id_zapatilla=7),
        Zapatilla("Nike", "Cortez Classic", 38, 120000, 11, id_zapatilla=8),
        Zapatilla("Adidas", "Ultraboost Light", 42, 180000, 9, id_zapatilla=9),
        Zapatilla("Adidas", "Superstar", 40, 130000, 15, id_zapatilla=10),
        Zapatilla("Adidas", "Stan Smith", 41, 125000, 13, id_zapatilla=11),
        Zapatilla("Adidas", "Samba OG", 39, 148000, 7, id_zapatilla=12),
        Zapatilla("Adidas", "Gazelle", 38, 142000, 10, id_zapatilla=13),
        Zapatilla("Adidas", "Forum Low", 43, 138000, 8, id_zapatilla=14),
        Zapatilla("Adidas", "NMD R1", 42, 160000, 6, id_zapatilla=15),
        Zapatilla("Adidas", "Campus 00s", 40, 145000, 11, id_zapatilla=16),
        Zapatilla("Puma", "Suede Classic", 41, 105000, 14, id_zapatilla=17),
        Zapatilla("Puma", "RS-X Efekt", 42, 135000, 7, id_zapatilla=18),
        Zapatilla("Puma", "Palermo", 39, 118000, 12, id_zapatilla=19),
        Zapatilla("Puma", "Cali Dream", 38, 115000, 10, id_zapatilla=20),
        Zapatilla("Puma", "Slipstream", 43, 128000, 8, id_zapatilla=21),
        Zapatilla("Puma", "Velocity Nitro 2", 42, 140000, 9, id_zapatilla=22),
        Zapatilla("New Balance", "574 Core", 41, 132000, 11, id_zapatilla=23),
        Zapatilla("New Balance", "9060", 42, 185000, 5, id_zapatilla=24),
        Zapatilla("New Balance", "327", 39, 138000, 13, id_zapatilla=25),
        Zapatilla("New Balance", "550", 43, 158000, 7, id_zapatilla=26),
        Zapatilla("New Balance", "1080 v13", 42, 190000, 6, id_zapatilla=27),
        Zapatilla("New Balance", "480", 40, 122000, 10, id_zapatilla=28),
        Zapatilla("Vans", "Old Skool", 40, 95000, 18, id_zapatilla=29),
        Zapatilla("Vans", "Sk8-Hi", 42, 108000, 11, id_zapatilla=30),
        Zapatilla("Vans", "Authentic", 38, 88000, 16, id_zapatilla=31),
        Zapatilla("Vans", "Knu Skool", 41, 115000, 9, id_zapatilla=32),
        Zapatilla("Vans", "Slip-On Checker", 39, 92000, 14, id_zapatilla=33),
        Zapatilla("Converse", "Chuck Taylor All Star", 39, 89000, 20, id_zapatilla=34),
        Zapatilla("Converse", "Chuck 70 Hi", 41, 112000, 12, id_zapatilla=35),
        Zapatilla("Converse", "Run Star Hike", 38, 128000, 8, id_zapatilla=36),
        Zapatilla("Converse", "One Star Pro", 42, 105000, 9, id_zapatilla=37),
        Zapatilla("Reebok", "Classic Leather", 42, 102000, 13, id_zapatilla=38),
        Zapatilla("Reebok", "Club C 85", 40, 108000, 15, id_zapatilla=39),
        Zapatilla("Reebok", "Nano X3", 43, 155000, 6, id_zapatilla=40),
        Zapatilla("Reebok", "Zig Kinetica", 41, 138000, 7, id_zapatilla=41),
        Zapatilla("Asics", "Gel-Nimbus 25", 42, 188000, 7, id_zapatilla=42),
        Zapatilla("Asics", "Gel-Kayano 30", 43, 192000, 5, id_zapatilla=43),
        Zapatilla("Asics", "Japan S", 40, 118000, 11, id_zapatilla=44),
        Zapatilla("Asics", "Gel-1130", 41, 135000, 9, id_zapatilla=45),
        Zapatilla("Fila", "Disruptor II", 38, 96000, 12, id_zapatilla=46),
        Zapatilla("Fila", "Renno", 41, 104000, 10, id_zapatilla=47),
        Zapatilla("Under Armour", "Charged Assert 10", 42, 115000, 14, id_zapatilla=48),
        Zapatilla("Under Armour", "HOVR Phantom 3", 43, 152000, 8, id_zapatilla=49),
        Zapatilla("Topper", "X-Forcer", 41, 78000, 16, id_zapatilla=50),
    ]

    gestor_menu = Menu(zapatillas_iniciales)

    while True:
        print("\nMenú principal de operaciones de gestión:")
        print("1. Registrar Zapatilla")
        print("2. Ver Zapatillas")
        print("3. Buscar Zapatillas por Marca")
        print("4. Registrar Venta")
        print("5. Ver Ventas")
        print("6. Borrar Venta")
        print("7. Salir")

        opcion_elegida = gestor_menu.pedir_numero_entero("Ingrese una opción (1-7): ", 1)

        if opcion_elegida == 1:
            gestor_menu.registrar_zapatilla()
        elif opcion_elegida == 2:
            gestor_menu.mostrar_zapatillas()
        elif opcion_elegida == 3:
            gestor_menu.buscar_zapatillas_por_marca()
        elif opcion_elegida == 4:
            gestor_menu.registrar_venta()
        elif opcion_elegida == 5:
            gestor_menu.ver_ventas()
        elif opcion_elegida == 6:
            gestor_menu.borrar_venta()
        elif opcion_elegida == 7:
            print("\nSaliendo de la aplicación")
            break
        else:
            print("ERROR !!! no existe la opción ingresada...")


if __name__ == "__main__":
    menu()
