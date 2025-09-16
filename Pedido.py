from producto import Producto
from enum import Enum, auto
import datetime
import json

class Tipo_cliente (Enum):
    ESTUDIANTE = auto()
    PROFESORES = auto()
    OTROS = auto()

class Pedido:
    def __init__(self):
        self.lista_productos = []
        self.tipo_cliente = None
        self.carne_valido = False

    def añadir_producto(self, producto: Producto, cantidad: int):
        encontrado = False
        for item in self.lista_productos:
            if item["producto"].id == producto.id: 
                item["cantidad"] += cantidad
                encontrado = True
                break
        if not encontrado:
            self.lista_productos.append({"producto":producto, "cantidad": cantidad})


    def eliminar_producto(self, producto_id: str , producto_nombre:str):
        self.lista_productos = [
            item for item in self.lista_productos 
            if item["producto"].id != producto_id or item["producto"].nombre != producto_nombre
        ]

    def ValidarCarneEstudiantil (self, codigo:str):
        if len(codigo) == 8 and codigo.isdigit():
            self.carne_valido = True
            self.tipo_cliente = Tipo_cliente.ESTUDIANTE
            return True
        return False
    
    def CalcularTotal (self, Tipo_cliente:Tipo_cliente):
        total = 0
        for i in self.lista_productos:
            precio= i["producto"].precio
            total+=precio*i["cantidad"]
            
        if Tipo_cliente == Tipo_cliente.ESTUDIANTE and self.carne_valido == True:
            total*=0.9
        return total
    
    def EmitirResumenFinal(self, ValorPagado:int):
        print("-"*60)
        print("CAFETERÍA CAMPUS")
        print("RESUMEN DE PEDIDO")
        print(datetime.date.today().strftime("%Y-%m-%d"))
            
        subtotal = 0
        for item in self.lista_productos:
            producto = item["producto"]
            cantidad = item["cantidad"]
            precio_unitario = producto.precio
            precio_linea = precio_unitario * cantidad
            subtotal += precio_linea
                
            print(f"{producto.nombre} x {cantidad} = {precio_linea}")
        print(f"\nSubtotal: ${subtotal:.2f}")
            
        if self.tipo_cliente == Tipo_cliente.ESTUDIANTE and self.carne_valido == True:
            descuento = subtotal * 0.1
            total_final = subtotal - descuento
            print(f"Descuento estudiante (10%): -${descuento:.2f}")
        else:
            total_final = subtotal
        
        if ValorPagado >= total_final:
            vueltas = ValorPagado-total_final
                
        print("-"*60)
        print(f"TOTAL A PAGAR: ${total_final:.2f}")
        print(f"VUELTAS: ${vueltas:.2f}")
        print("-"*60)
        
    def guardar_registros_json (self):
        """Metodo para guardar los registros en json"""
        fecha_actual = datetime.date.today().strftime("%Y-%m-%d")
        archivo = f"Registro_{fecha_actual}.json"

        datos_venta ={
            "Time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Tipo_cliente":self.tipo_cliente.name,
            "Productos":[],
            "total":self.CalcularTotal(self.tipo_cliente)
        }
        for i in self.lista_productos:
            datos_producto = {
                "Nombre": i["producto"].nombre,
                "Precio": i["producto"].precio,
                "id": i["producto"].id,
                "Cantidad": i["cantidad"],
                "subtotal_producto": i["producto"].precio * i["cantidad"]
            }

            datos_venta["Productos"].append(datos_producto)

        #Guardar en json el primer registro
        try: 
            with open(archivo, "r", encoding="utf-8") as f:
                registros = json.load(f)
        except FileNotFoundError:
                registros =[]

        #Agregar las nuevas listas con append y añadirlas al json
        registros.append(datos_venta)
        with open(archivo, "w", encoding="utf-8") as f:
                json.dump(registros, f, indent=4, ensure_ascii=False)

 
