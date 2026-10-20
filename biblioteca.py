
import tkinter as tk
from tkinter import ttk, messagebox

class Libro:
    def __init__(self, titulo, autor, categoria, cantidad):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.cantidad = cantidad

    def __str__(self):
        return f"{self.titulo} | {self.autor} | {self.categoria} | Disponibles: {self.cantidad}"

class Prestamo:
    def __init__(self, titulo, categoria):
        self.titulo = titulo
        self.categoria = categoria

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaPrestamos:
    def __init__(self):
        self.inicio = None

    def agregar(self, prestamo):
        nuevo = Nodo(prestamo)

        if self.inicio is None:
            self.inicio = nuevo
            return

        actual = self.inicio

        while actual.siguiente is not None:
            actual = actual.siguiente

        actual.siguiente = nuevo

    def buscar(self, titulo):
        actual = self.inicio

        while actual is not None:
            if actual.dato.titulo.lower() == titulo.lower():
                return actual.dato
            actual = actual.siguiente

        return None

    def eliminar(self, titulo):
        actual = self.inicio

        if actual is None:
            return False

        if actual.dato.titulo.lower() == titulo.lower():
            self.inicio = actual.siguiente
            return True

        while actual.siguiente is not None:
            if actual.siguiente.dato.titulo.lower() == titulo.lower():
                actual.siguiente = actual.siguiente.siguiente
                return True

            actual = actual.siguiente

        return False

    def recorrer(self):
        prestamos = []
        actual = self.inicio

        while actual is not None:
            prestamos.append(actual.dato)
            actual = actual.siguiente

        return prestamos

    def contar(self):
        total = 0
        actual = self.inicio

        while actual is not None:
            total += 1
            actual = actual.siguiente

        return total

class Biblioteca:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Biblioteca")
        self.ventana.geometry("950x620")
        self.ventana.configure(bg="#f0f2f5")

        self.libros = []

        self.prestamos = ListaPrestamos()

        self.categorias = [
            "Novela",
            "Ciencia",
            "Historia",
            "Tecnologia",
            "Arte"
        ]

        self.cantidad_prestamos = [0] * len(self.categorias)

        self.crear_interfaz()
        self.cargar_datos()
        self.mostrar_libros()

    def crear_interfaz(self):
        tk.Label(
            self.ventana,
            text="SISTEMA DE BIBLIOTECA",
            font=("Arial", 20, "bold"),
            bg="#283593",
            fg="white",
            pady=15
        ).pack(fill="x")

        formulario = tk.Frame(self.ventana, bg="#f0f2f5")
        formulario.pack(pady=12)

        tk.Label(formulario, text="Titulo:", bg="#f0f2f5").grid(row=0, column=0, padx=5, pady=5)
        self.txt_titulo = tk.Entry(formulario, width=25)
        self.txt_titulo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Autor:", bg="#f0f2f5").grid(row=1, column=0, padx=5, pady=5)
        self.txt_autor = tk.Entry(formulario, width=25)
        self.txt_autor.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Categoria:", bg="#f0f2f5").grid(row=2, column=0, padx=5, pady=5)
        self.cmb_categoria = ttk.Combobox(
            formulario,
            values=self.categorias,
            state="readonly",
            width=22
        )
        self.cmb_categoria.grid(row=2, column=1, padx=5, pady=5)
        self.cmb_categoria.current(0)

        tk.Label(formulario, text="Cantidad:", bg="#f0f2f5").grid(row=3, column=0, padx=5, pady=5)
        self.txt_cantidad = tk.Entry(formulario, width=25)
        self.txt_cantidad.grid(row=3, column=1, padx=5, pady=5)

        botones = tk.Frame(self.ventana, bg="#f0f2f5")
        botones.pack(pady=5)

        acciones = [
            ("Registrar", self.registrar),
            ("Buscar", self.buscar),
            ("Modificar", self.modificar),
            ("Eliminar", self.eliminar),
            ("Ordenar", self.ordenar),
            ("Prestar", self.prestar),
            ("Devolver", self.devolver),
            ("Ver prestamos", self.ver_prestamos),
            ("Ver categorias", self.ver_categorias),
            ("Limpiar", self.limpiar)
        ]

        for i, (texto, accion) in enumerate(acciones):
            tk.Button(
                botones,
                text=texto,
                command=accion,
                width=14
            ).grid(row=i // 5, column=i % 5, padx=4, pady=4)

        self.lista = tk.Listbox(
            self.ventana,
            width=105,
            height=13,
            font=("Consolas", 10)
        )
        self.lista.pack(padx=15, pady=10, fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", self.seleccionar)

        self.lbl_resumen = tk.Label(
            self.ventana,
            text="",
            font=("Arial", 11, "bold"),
            bg="#f0f2f5"
        )
        self.lbl_resumen.pack(pady=8)

    def cargar_datos(self):
        self.libros.append(Libro("El principito", "Antoine de Saint-Exupery", "Novela", 3))
        self.libros.append(Libro("Cosmos", "Carl Sagan", "Ciencia", 2))
        self.libros.append(Libro("Historia de Costa Rica", "Autor de prueba", "Historia", 4))
        self.libros.append(Libro("Python desde cero", "Autor de prueba", "Tecnologia", 5))

    def encontrar_libro(self, titulo):
        for libro in self.libros:
            if libro.titulo.lower() == titulo.strip().lower():
                return libro

        return None

    def leer_datos(self):
        titulo = self.txt_titulo.get().strip()
        autor = self.txt_autor.get().strip()
        categoria = self.cmb_categoria.get()
        cantidad_texto = self.txt_cantidad.get().strip()

        if not titulo or not autor or not categoria or not cantidad_texto:
            messagebox.showwarning("Aviso", "Complete todos los campos.")
            return None

        try:
            cantidad = int(cantidad_texto)
        except ValueError:
            messagebox.showwarning("Aviso", "La cantidad debe ser un numero entero.")
            return None

        if cantidad < 0:
            messagebox.showwarning("Aviso", "La cantidad no puede ser negativa.")
            return None

        return titulo, autor, categoria, cantidad

    def registrar(self):
        datos = self.leer_datos()

        if datos is None:
            return

        titulo, autor, categoria, cantidad = datos

        if self.encontrar_libro(titulo):
            messagebox.showwarning("Aviso", "Ese libro ya existe.")
            return

        self.libros.append(Libro(titulo, autor, categoria, cantidad))
        self.mostrar_libros()
        self.limpiar()
        messagebox.showinfo("Biblioteca", "Libro registrado correctamente.")

    def buscar(self):
        titulo = self.txt_titulo.get().strip()

        if not titulo:
            messagebox.showwarning("Aviso", "Escriba el titulo que desea buscar.")
            return

        libro = self.encontrar_libro(titulo)

        if libro is None:
            messagebox.showinfo("Busqueda", "No se encontro el libro.")
            return

        self.mostrar_seleccion(libro)

    def modificar(self):
        libro = self.encontrar_libro(self.txt_titulo.get())

        if libro is None:
            messagebox.showwarning("Aviso", "Escriba el titulo de un libro existente.")
            return

        datos = self.leer_datos()

        if datos is None:
            return

        titulo, autor, categoria, cantidad = datos
        otro = self.encontrar_libro(titulo)

        if otro is not None and otro is not libro:
            messagebox.showwarning("Aviso", "Ya existe otro libro con ese titulo.")
            return

        libro.titulo = titulo
        libro.autor = autor
        libro.categoria = categoria
        libro.cantidad = cantidad

        self.mostrar_libros()
        messagebox.showinfo("Biblioteca", "Libro modificado correctamente.")

    def eliminar(self):
        libro = self.encontrar_libro(self.txt_titulo.get())

        if libro is None:
            messagebox.showwarning("Aviso", "Seleccione un libro existente.")
            return

        if self.prestamos.buscar(libro.titulo):
            messagebox.showwarning("Aviso", "El libro tiene prestamos activos.")
            return

        self.libros.remove(libro)
        self.mostrar_libros()
        self.limpiar()
        messagebox.showinfo("Biblioteca", "Libro eliminado correctamente.")

    def ordenar(self):
        self.libros.sort(key=lambda libro: libro.titulo.lower())
        self.mostrar_libros()

    def prestar(self):
        libro = self.encontrar_libro(self.txt_titulo.get())

        if libro is None:
            messagebox.showwarning("Aviso", "Seleccione un libro del catalogo.")
            return

        if libro.cantidad <= 0:
            messagebox.showwarning("Aviso", "No hay ejemplares disponibles.")
            return

        libro.cantidad -= 1
        self.prestamos.agregar(Prestamo(libro.titulo, libro.categoria))

        indice = self.categorias.index(libro.categoria)
        self.cantidad_prestamos[indice] += 1

        self.mostrar_libros()
        messagebox.showinfo("Biblioteca", "Prestamo registrado.")

    def devolver(self):
        titulo = self.txt_titulo.get().strip()
        prestamo = self.prestamos.buscar(titulo)

        if prestamo is None:
            messagebox.showwarning("Aviso", "No hay un prestamo activo de ese libro.")
            return

        self.prestamos.eliminar(titulo)
        libro = self.encontrar_libro(titulo)

        if libro:
            libro.cantidad += 1

        indice = self.categorias.index(prestamo.categoria)
        self.cantidad_prestamos[indice] -= 1

        self.mostrar_libros()
        messagebox.showinfo("Biblioteca", "Devolucion registrada.")

    def ver_prestamos(self):
        self.lista.delete(0, tk.END)
        prestamos = self.prestamos.recorrer()

        if not prestamos:
            self.lista.insert(tk.END, "No hay prestamos activos.")
            return

        for prestamo in prestamos:
            self.lista.insert(tk.END, f"{prestamo.titulo} | {prestamo.categoria}")

    def ver_categorias(self):
        texto = ""

        for i in range(len(self.categorias)):
            texto += f"{self.categorias[i]}: {self.cantidad_prestamos[i]} prestamos activos\n"

        messagebox.showinfo("Prestamos por categoria", texto)

    def mostrar_libros(self):
        self.lista.delete(0, tk.END)

        if not self.libros:
            self.lista.insert(tk.END, "El catalogo esta vacio.")
        else:
            for libro in self.libros:
                self.lista.insert(tk.END, str(libro))

        self.lbl_resumen.config(
            text=f"Libros registrados: {len(self.libros)} | Prestamos activos: {self.prestamos.contar()}"
        )

    def mostrar_seleccion(self, libro):
        self.txt_titulo.delete(0, tk.END)
        self.txt_titulo.insert(0, libro.titulo)

        self.txt_autor.delete(0, tk.END)
        self.txt_autor.insert(0, libro.autor)

        self.cmb_categoria.set(libro.categoria)

        self.txt_cantidad.delete(0, tk.END)
        self.txt_cantidad.insert(0, str(libro.cantidad))

    def seleccionar(self, evento):
        seleccion = self.lista.curselection()

        if not seleccion:
            return

        texto = self.lista.get(seleccion[0])
        titulo = texto.split(" | ")[0]
        libro = self.encontrar_libro(titulo)

        if libro is not None:
            self.mostrar_seleccion(libro)

    def limpiar(self):
        self.txt_titulo.delete(0, tk.END)
        self.txt_autor.delete(0, tk.END)
        self.txt_cantidad.delete(0, tk.END)
        self.cmb_categoria.current(0)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Biblioteca(ventana)
    ventana.mainloop()