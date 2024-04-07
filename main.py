from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from clas_lexema import Lexema
from clas_error import Error

class AnalizadorLexico:
    def __init__(self, textAreaInicial, textAreaFinal):
        self.textAreaInicial = textAreaInicial
        self.textAreaFinal = textAreaFinal
        self.lexemas = []
        self.errores = []

    def analizar(self):
        self.lexemas.clear()
        self.errores.clear()
        palabra = ""
        fila = 1
        columna = 0
        texto = self.textAreaInicial.get("1.0", "end")
        i = 0

        while i < len(texto):
            char = texto[i]
            columna += 1

            if char.isalnum():
                while i < len(texto) and texto[i].isalnum():
                    palabra += texto[i]
                    i += 1

                if palabra.lower() in ['encabezado', 'titulo', 'fondo', 'parrafo', 'texto', 'codigo', 'negrita', 'subrayado', 'tachado', 'cursiva', 'salto', 'tabla', 'titulopagina', 'texto', 'posicion', 'tamaño', 'color', 'fuente', 'cantidad', 'filas', 'columnas', 'elemento']:
                    self.lexemas.append(Lexema("PALABRA_RESERVADA", palabra.lower(), columna, fila))
                elif palabra.isdigit():
                    self.lexemas.append(Lexema("NUMERO", palabra, columna, fila))
                else:
                    self.lexemas.append(Lexema("PALABRA", palabra, columna, fila))
                palabra = ""

            elif char in [':']:
                self.lexemas.append(Lexema("DOS PUNTO", char, columna, fila))
            elif char in [';']:
                self.lexemas.append(Lexema("PUNTO Y COMA", char, columna, fila))
            elif char in ['{']:
                self.lexemas.append(Lexema("LLAVE ABRIR", char, columna, fila))
            elif char in ['}']:
                self.lexemas.append(Lexema("LLAVE CERRAR", char, columna, fila))  
            elif char in [',']:
                self.lexemas.append(Lexema("COMA", char, columna, fila))  
            elif char in ['"']:
                self.lexemas.append(Lexema("COMILLAS", char, columna, fila))
            elif char in [' ', '\n', '\t', '\r']:
                if char == '\n':
                    fila += 1
                columna = 0
            else:
                self.errores.append(Error(char, columna, fila))

            i += 1

        self.generar_reporte_html()
        self.imprimir_lexemas_y_errores()
    
    def imprimir_lexemas_y_errores(self):
        self.textAreaFinal.delete("1.0", END)
        self.textAreaFinal.insert(END, "#############################\n")
        self.textAreaFinal.insert(END, "Lexemas:\n")
        for lexema in self.lexemas:
            self.textAreaFinal.insert(END, f"{lexema.tipo}: {lexema.valor}\n")
        self.textAreaFinal.insert(END, "#############################\n")
        self.textAreaFinal.insert(END, "Errores:\n")
        for error in self.errores:
            self.textAreaFinal.insert(END, f"{error.mensaje}\n")

    def generar_reporte_html(self):
        contenido = "<!DOCTYPE html>\n<html>\n<head>\n<title>Reporte de Tokens y Errores</title>\n</head>\n<body>\n"
        contenido += "<h1>Reporte de Tokens y Errores</h1>\n"
        contenido += "<h2>Lexemas</h2>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Tipo</th><th>Valor</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, lexema in enumerate(self.lexemas):
            contenido += f"<tr><td>{i+1}</td><td>{lexema.tipo}</td><td>{lexema.valor}</td><td>{lexema.columna}</td><td>{lexema.fila}</td></tr>\n"
        contenido += "</table>\n"

        # Agregamos los errores
        contenido += "<h2>Errores</h2>\n"
        contenido += "<table border='1'>\n<tr><th>#</th><th>Mensaje</th><th>Columna</th><th>Fila</th></tr>\n"
        for i, error in enumerate(self.errores):
            contenido += f"<tr><td>{i+1}</td><td>{error.mensaje}</td><td>{error.columna}</td><td>{error.fila}</td></tr>\n"
        contenido += "</table>\n"

        contenido += "</body>\n</html>"

        with open("reporte.html", "w") as f:
            f.write(contenido)
    
class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.construir_interfaz()

    def construir_interfaz(self):
        frm = ttk.Frame(self.root, width=600, height=400)
        frm.grid()
        ttk.Label(frm, text="Proyecto 1").grid(column=0, row=0)
        ttk.Button(frm, text="Salir", command=self.root.destroy).grid(column=0, row=1)
        ttk.Button(frm, text="Abrir Datos Personales", command=self.abrir_segunda_ventana).grid(column=0, row=2)
        ttk.Button(frm, text="Abrir Text Area", command=self.abrir_tercera_ventana).grid(column=0, row=3)

    def abrir_segunda_ventana(self):
        SegundaVentana(self.root)

    def abrir_tercera_ventana(self):
        TerceraVentana(self.root)

class SegundaVentana:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Datos Personales")
        self.construir_interfaz()

    def construir_interfaz(self):
        color = '#FF9115'
        frm = ttk.Frame(self.root, width=600, height=400)
        frm.grid()
        ttk.Label(frm, text="Nombre: José Yaquian").grid(column=0, row=0)
        ttk.Label(frm, text="Carnet: 202201185").grid(column=0, row=1)
        ttk.Label(frm, text="Curso: Lenguajes Formales y de Programación").grid(column=0, row=2)
        ttk.Button(frm, text="Regresar", command=self.root.destroy).grid(column=0, row=3)

class TerceraVentana:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Compilador")
        self.construir_interfaz()

    def construir_interfaz(self):
        frm = ttk.Frame(self.root, width=1000, height=1200)
        frm.grid()
        self.textAreaInicial = Text(frm, width=50, height=25)
        self.textAreaInicial.grid(column=1, row=1)
        ttk.Button(frm, text="Obtener Data", command=self.cargar_archivo).grid(column=3, row=0)
        ttk.Button(frm, text="Compilar", command=self.compilar).grid(column=3, row=1)
        ttk.Button(frm, text="Regresar", command=self.root.destroy).grid(column=3, row=3)
        self.textAreaFinal = Text(frm, width=50, height=25)
        self.textAreaFinal.grid(column=5, row=1)

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt *.html")])
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.textAreaInicial.delete("1.0", END)
            self.textAreaInicial.insert(END, contenido)

    def compilar(self):
        analizador = AnalizadorLexico(self.textAreaInicial, self.textAreaFinal)
        analizador.analizar()
        analizador.generar_reporte_html()

def main():
    root = Tk()
    VentanaPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()
