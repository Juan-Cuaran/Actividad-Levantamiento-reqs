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
    
    def AgregarProducto (self):
        nombre = input("Digite el nombre del producto ")
        precio = float(input("Digite el precio del producto "))
        ide = input("Ingrese el id del producto ")
        new_product = Producto(nombre, ide, precio)
        self.lista_productos.append(new_product)
        print(f"Producto {ide} agregado exitosamente")

    def Menu_Principal(self):
        print("\n--- MENÚ DISPONIBLE ---")
        for i, producto in enumerate(self.lista_productos, 1):
            print(f"{i}. {producto.mostrar_info()} (ID: {producto.id})")
        
    def buscar_por_id (self, producto_id):
        for producto in self.lista_productos:
            if producto.id == producto_id:
                return producto
        return None

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
                    cantidad = int(input(f"¿Cuántos {producto.nombre} desea? "))
                    if cantidad > 0:
                        pedido.añadir_producto(producto, cantidad)
                        print(f"Agregado: {cantidad} x {producto.nombre}")
                    else:
                        print("La cantidad debe ser mayor a 0")
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
            
    def main(self):
        if self.Autenticacion():
            while(True):
                print("-"*22 + "Cafeteria Campus" + "-"*22)
                print("-1.Registrar Pedido " + "-"*40)
                print("-2.Agregar Producto " + "-"*40)
                print("-3.RegistrarCarneEstudiantes " + "-"*30)
                print("-4.Ver Menu " + "-"*48)
                print("-5.Salir " + "-"*51)
                print("-"*60)

                respuesta = int(input("\nSeleccione una opcion "))
                if respuesta == 1:
                    self.registrar_pedido()
                elif respuesta ==2:
                    self.AgregarProducto()
                elif respuesta==3:
                    self.RegistrarCarneEstudiantil()
                elif respuesta == 4:
                    self.Menu_Principal()
                elif respuesta >=5:
                    print("ProcesoTerminado")
                    return
                else:
                    return 

if __name__ == "__main__":
    cafeteria = CafeteriaCampus()
    cafeteria.main()