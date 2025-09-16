author = "Juan Esteban Cuaran"

class Producto:

    def __init__(self, nombre:str, __id:str, precio:float):
        self.nombre = nombre
        self.id = __id
        self.precio = precio


    @property
    def get_nombre (self):
        return self.nombre
    
    @property
    def get_id (self):
        return self.id
    
    @property
    def get_precio (self):
        return self.precio

    def mostrar_info (self):
        return f'{self.nombre}  -  {self.precio:.2f}'
    

