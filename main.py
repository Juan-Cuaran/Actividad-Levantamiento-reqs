from producto import Producto
from Pedido import Pedido, Tipo_cliente
import json

class CafeteriaCampus:

    def __init__(self):
        self.lista_carnets =[]
        self.lista_productos =[]

    def Autenticacion (self):
        CLAVE ="12345678"
        intentos = 0
        while (intentos <3):
            password = input("Digite la clave de acceso del sistema ")
            if password == CLAVE:
                print("Usuario autenticado")
                return True
            else:
                intentos +=1
                print("Clave incorrecta, intentelo de nuevo ")
        print("Acceso denegado")
        return False

    def RegistrarCarneEstudiantil(self):
        carnet = input("Ingrese el codigo del carne estudiantil que desea registrar: ")
        if len(carnet) == 8 and carnet.isdigit():
            if carnet not in self.lista_carnets:
                self.lista_carnets.append(carnet)
                print("Carné registrado exitosamente.")
            else:
                print("Este carné ya está registrado.")
        else:
            print("El código del carné debe tener exactamente 8 dígitos.")

    def AgregarProducto (self):
        nombre = input("Digite el nombre del producto ")
        precio = float(input("Digite el precio del producto "))
        ide = input("Ingrese el id del producto (máximo 8 dígitos) ")

        if not ide.isdigit() or len(ide) > 8:
            print("El ID debe ser numérico y tener como máximo 8 dígitos.")
            print("Producto no agregado")
            return

        new_product = Producto(nombre, ide, precio)
        self.lista_productos.append(new_product)
        print(f"Producto {ide} agregado exitosamente")

    def Menu_Principal(self):
        print("\n--- MENÚ DISPONIBLE ---")
        if not self.lista_productos:
            print("No hay productos disponibles.")
            return
        for i, producto in enumerate(self.lista_productos, 1):
            print(f"{i}. {producto.mostrar_info()} (ID: {producto.id})")
        
    def buscar_por_id (self, producto_id):
        for producto in self.lista_productos:
            if producto.id == producto_id:
                return producto
        return None

    def ActualizarProducto(self):
        if not self.lista_productos:
            print("No hay productos disponibles para actualizar.")
            return
        
        print("\n--- PRODUCTOS DISPONIBLES ---")
        self.Menu_Principal()
        
        producto_id = input("\nIngrese el ID del producto que desea actualizar: ")
        producto = self.buscar_por_id(producto_id)
        
        if not producto:
            print("Producto no encontrado.")
            return
        
        print(f"\nProducto seleccionado: {producto.mostrar_info()}")
        print("¿Qué desea actualizar?")
        print("1. Nombre del producto")
        print("2. Precio del producto")
        
        opcion = int(input("Seleccione una opción (1 o 2): "))    
        if opcion == 1:
            nuevo_nombre = input(f"Nombre actual: {producto.nombre}\nIngrese el nuevo nombre: ")
            if nuevo_nombre.strip():
                producto.nombre = nuevo_nombre
                print(f"Nombre actualizado exitosamente a: {nuevo_nombre}")
            else:
                print("El nombre no puede estar vacío.")
                    
        elif opcion == 2:
            nuevo_precio = float(input(f"Precio actual: ${producto.precio}\nIngrese el nuevo precio: "))
            if nuevo_precio > 0:
                producto.precio = nuevo_precio
                print(f"Precio actualizado exitosamente a: ${nuevo_precio}")
            else:
                print("El precio debe ser mayor a 0.")
        else:
            print("Opción no válida.")

    def GestionarMenu(self):
        while True:
            print("\n--- GESTIÓN DE MENÚ ---")
            print("1. Ver menú actual")
            print("2. Actualizar productos")
            print("3. Volver al menú principal")
            opcion = int(input("Seleccione una opción: "))            
            if opcion == 1:
                self.Menu_Principal()
            elif opcion == 2:
                self.ActualizarProducto()
            elif opcion == 3:
                break
            else:
                    print("Opción no válida. Seleccione 1, 2 o 3.")

    def registrar_pedido(self):
        pedido = Pedido()
        print("Seleccione el tipo de cliente")
        print("1. Estudiante")
        print("2. Profesor")
        print("3. Otros")

        opcion_cliente = int(input("Opción: "))
        if opcion_cliente == 1:
            pedido.tipo_cliente = Tipo_cliente.ESTUDIANTE
            code = input("Digite el código del Estudiante: ")
            if code in self.lista_carnets:
                pedido.ValidarCarneEstudiantil(code)
                print("Descuento aplicado")
            else:
                print("Carné no registrado. No se aplicará descuento.")
        elif opcion_cliente == 2:
            pedido.tipo_cliente = Tipo_cliente.PROFESORES
        elif opcion_cliente == 3:
            pedido.tipo_cliente = Tipo_cliente.OTROS

        while True:
            self.Menu_Principal()
            print("1. Agregar Producto ")
            print("2. Finalizar compra ")

            r = int(input("Opción: "))

            if r == 1:
                producto_id = input("Digite el ID del producto: ")
                producto = self.buscar_por_id(producto_id)
                
                if producto:
                    cantidad = int(input(f"¿Cuántos {producto.nombre} desea? (máximo 99) "))
                    if 1 <= cantidad <= 99:
                        pedido.añadir_producto(producto, cantidad)
                        print(f"Agregado: {cantidad} x {producto.nombre}")
                    else:
                        print("La cantidad debe estar entre 1 y 99")
                else:
                    print("Producto no encontrado")
            elif r == 2:
                if pedido.lista_productos:
                    total = pedido.CalcularTotal(pedido.tipo_cliente)
                    print(f"\nTotal a pagar: ${total:.2f}")
                    valor_pagado = float(input("Ingrese el valor pagado: "))
                    if valor_pagado >= total:
                        pedido.EmitirResumenFinal(valor_pagado)
                        pedido.guardar_registros_json()
                        print("Pedido procesado exitosamente!")
                        break
                    else:
                        print("El valor pagado es insuficiente")
                else:
                    print("No hay productos en el pedido")
            else:
                print("Opción no válida")

    def mostrar_historial(self):
        try:
            with open('ventas_ddmmaa.json', 'r') as archivo:
                datos = json.load(archivo)
                print("=== HISTORIAL DEL DÍA ===")
                for pedido in datos['pedidos']:
                    print(f"Pedido - {pedido['hora']}")
                    print(f"Cliente: {pedido['tipo_cliente']}")
                    for item in pedido['items']:
                        print(f"- {item['cantidad']}x {item['producto']} (${item['subtotal']})")
                    print(f"Total: ${pedido['total']}")
                    print("-" * 20)
        except FileNotFoundError:
            print("No hay historial disponible para hoy")
            
    def main(self):
        if self.Autenticacion():
            while(True):
                print("-"*22 + "Cafeteria Campus" + "-"*22)
                print("-1.Registrar Pedido " + "-"*40)
                print("-2.Agregar Producto " + "-"*40)
                print("-3.RegistrarCarneEstudiantes " + "-"*30)
                print("-4.Gestionar Menú " + "-"*41)
                print("-5.Historial " + "-"*51)
                print("-"*60)

                try:
                    respuesta = int(input("\nSeleccione una opcion "))
                    if respuesta == 1:
                        self.registrar_pedido()
                    elif respuesta == 2:
                        self.AgregarProducto()
                    elif respuesta == 3:
                        self.RegistrarCarneEstudiantil()
                    elif respuesta == 4:
                        self.GestionarMenu()
                    elif respuesta == 5:
                        self.mostrar_historial()
                    elif respuesta >= 6:
                        print("ProcesoTerminado")
                        return
                    else:
                        print("Opción no válida")
                except ValueError:
                    print("Por favor, ingrese un número válido.")

if __name__ == "__main__":
    cafeteria = CafeteriaCampus()
    cafeteria.main()
