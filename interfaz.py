import tkinter as tk
from tkinter import ttk, messagebox
from main import CafeteriaCampus
from Pedido import Pedido, Tipo_cliente
from producto import Producto


class CafeteriaGUI:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("1200x800")
        self.ventana.title("CAFETERIA CAMPUS")
        self.ventana.configure(bg="lightblue")
        self.pedido = None
        self.cafeteria = CafeteriaCampus()
    
    def GUI (self):
        frame_h = tk.Frame(self.ventana, bg="cyan", height=80)
        frame_h.pack()

        label_h = tk.Label(self.ventana, text="CAFETERIA CAMPUS", font=('Arial', 40, "bold"), bg="cyan")
        label_h.pack()
        
        self.entrada = tk.Entry(self.ventana, font=("Consolas", 20), justify="center")
        self.entrada.pack()

        boton_cliente = tk.Button(self.ventana, text="Seleccione el tipo de cliente")
        boton_cliente.config(fg="White", bg ="light grey",font=("Arial", 20), command=self.Seleccionar_cliente())

    def Seleccionar_cliente (self):
        self.pedido = Pedido()
        respuesta = int(self.entrada.get())

        if respuesta == 1:
            self.pedido.tipo_cliente = Tipo_cliente.ESTUDIANTE
        




 


    