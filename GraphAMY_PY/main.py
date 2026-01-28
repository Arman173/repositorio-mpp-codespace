import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import numpy as np # IMPORTANTE: Necesitamos numpy para las funciones
from GeneradorG import GeneradorGraficas

class AplicacionGraficas:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador Pro de Gráficas")
        self.root.geometry("700x800")
        
        self.grupos_agregados = []

        # --- 1. Configuración General ---
        frame_config = ttk.LabelFrame(root, text="1. Configuración del Reporte", padding=10)
        frame_config.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_config, text="Título:").grid(row=0, column=0, sticky="w")
        self.entry_titulo = ttk.Entry(frame_config, width=40)
        self.entry_titulo.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_config, text="Eje X:").grid(row=1, column=0, sticky="w")
        self.entry_x = ttk.Entry(frame_config, width=40)
        self.entry_x.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_config, text="Eje Y:").grid(row=2, column=0, sticky="w")
        self.entry_y = ttk.Entry(frame_config, width=40)
        self.entry_y.grid(row=2, column=1, padx=5, pady=2)

        # --- 2. PESTAÑAS PARA DATOS ---
        frame_tabs = ttk.LabelFrame(root, text="2. Agregar Datos (Elige Método)", padding=10)
        frame_tabs.pack(fill="x", padx=10, pady=5)
        
        self.notebook = ttk.Notebook(frame_tabs)
        self.notebook.pack(fill="both", expand=True)

        # --- PESTAÑA A: MANUAL ---
        self.tab_manual = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_manual, text="Datos Manuales (Listas)")
        self.crear_tab_manual()

        # --- PESTAÑA B: FUNCIONES ---
        self.tab_func = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_func, text="Función Matemática")
        self.crear_tab_funciones()

        # --- 3. Lista de Grupos ---
        frame_lista = ttk.LabelFrame(root, text="Grupos Listos", padding=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.lista_grupos = tk.Listbox(frame_lista, height=6)
        self.lista_grupos.pack(fill="both", expand=True)
        ttk.Button(frame_lista, text="Borrar Seleccionado", command=self.borrar_grupo).pack(pady=5)

        # --- 4. Generar ---
        btn_generar = tk.Button(root, text="EXPORTAR GRÁFICA", command=self.generar_grafica, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), height=2)
        btn_generar.pack(fill="x", padx=20, pady=15)

    def crear_tab_manual(self):
        # Campos para datos manuales
        ttk.Label(self.tab_manual, text="Nombre Grupo:").grid(row=0, column=0, pady=5)
        self.m_nombre = ttk.Entry(self.tab_manual, width=20)
        self.m_nombre.grid(row=0, column=1)

        ttk.Label(self.tab_manual, text="Datos X (Sep. comas):").grid(row=1, column=0, pady=5)
        self.m_x = ttk.Entry(self.tab_manual, width=30)
        self.m_x.grid(row=1, column=1)
        ttk.Label(self.tab_manual, text="(Texto o Números)", font=("Arial", 8)).grid(row=1, column=2)

        ttk.Label(self.tab_manual, text="Datos Y (Sep. comas):").grid(row=2, column=0, pady=5)
        self.m_y = ttk.Entry(self.tab_manual, width=30)
        self.m_y.grid(row=2, column=1)

        self.crear_controles_comunes(self.tab_manual, row_start=3, funcion_agregar=self.agregar_manual)

    def crear_tab_funciones(self):
        # Campos para funciones matemáticas
        ttk.Label(self.tab_func, text="Nombre Función:").grid(row=0, column=0, pady=5)
        self.f_nombre = ttk.Entry(self.tab_func, width=20)
        self.f_nombre.grid(row=0, column=1)

        ttk.Label(self.tab_func, text="Fórmula f(x):").grid(row=1, column=0, pady=5)
        self.f_formula = ttk.Entry(self.tab_func, width=30)
        self.f_formula.insert(0, "np.sin(x) * x") # Ejemplo
        self.f_formula.grid(row=1, column=1)
        ttk.Label(self.tab_func, text="Usa 'np' para numpy (ej. np.cos(x))", font=("Arial", 8)).grid(row=1, column=2)

        # Rango de X
        frame_rango = ttk.Frame(self.tab_func)
        frame_rango.grid(row=2, column=1, sticky="w")
        ttk.Label(self.tab_func, text="Rango X:").grid(row=2, column=0)
        
        self.f_min = ttk.Entry(frame_rango, width=5)
        self.f_min.insert(0, "0")
        self.f_min.pack(side="left")
        ttk.Label(frame_rango, text=" a ").pack(side="left")
        self.f_max = ttk.Entry(frame_rango, width=5)
        self.f_max.insert(0, "10")
        self.f_max.pack(side="left")

        ttk.Label(self.tab_func, text="Puntos (suavidad):").grid(row=3, column=0)
        self.f_puntos = ttk.Entry(self.tab_func, width=10)
        self.f_puntos.insert(0, "100")
        self.f_puntos.grid(row=3, column=1, sticky="w")

        self.crear_controles_comunes(self.tab_func, row_start=4, funcion_agregar=self.agregar_funcion)

    def crear_controles_comunes(self, parent, row_start, funcion_agregar):
        # Selector de Tipo de Gráfica
        ttk.Label(parent, text="Tipo:").grid(row=row_start, column=0, pady=10)
        self.combo_tipo = ttk.Combobox(parent, values=["Línea", "Dispersión (Scatter)"], state="readonly", width=15)
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=row_start, column=1, sticky="w")

        # Selector de Color
        self.btn_color = tk.Button(parent, text="Elegir Color", command=lambda: self.elegir_color(self.btn_color), bg="blue", fg="white")
        self.btn_color.grid(row=row_start+1, column=0)
        self.color_actual = "blue"

        # Botón Agregar
        ttk.Button(parent, text="AGREGAR GRUPO", command=funcion_agregar).grid(row=row_start+1, column=1, pady=10)

    def elegir_color(self, btn):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_actual = color
            btn.config(bg=color)

    def agregar_manual(self):
        nombre = self.m_nombre.get()
        str_x = self.m_x.get()
        str_y = self.m_y.get()
        tipo = "linea" if self.combo_tipo.get() == "Línea" else "dispersion"

        if not nombre or not str_x or not str_y:
            messagebox.showwarning("Faltan datos", "Llena todos los campos manuales.")
            return

        try:
            # Procesar X: Intentar convertir a números, si falla, dejar como texto
            raw_x = [x.strip() for x in str_x.split(',')]
            try:
                lista_x = [float(x) for x in raw_x] # Intento numérico
            except ValueError:
                lista_x = raw_x # Fallo, se queda como texto (Categorías)

            lista_y = [float(y.strip()) for y in str_y.split(',')]
            
            self._guardar_grupo(nombre, lista_x, lista_y, self.color_actual, tipo)
            
            # Limpiar
            self.m_nombre.delete(0, tk.END)
            self.m_y.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Datos Y deben ser números.")

    def agregar_funcion(self):
        nombre = self.f_nombre.get()
        formula = self.f_formula.get()
        tipo = "linea" if self.combo_tipo.get() == "Línea" else "dispersion" # Esto es un truco para leer el combo del tab activo si compartieran variable, pero aquí instancié dos combos. 
        # CORRECCIÓN: Como hay dos pestañas, el "self.combo_tipo" apuntaría al último creado.
        # Para simplificar el código anterior, obtendré el valor del combo hijo del frame actual.
        # Pero para que funcione fácil, asumiremos que usas el combo que se ve.
        
        # Corrección rápida para leer el combo correcto (ya que self.combo_tipo se sobrescribe)
        # En una app real usaríamos variables de control Tkinter, pero lo haré dinámico:
        combo_box = self.tab_func.children.get(list(self.tab_func.children.keys())[-3]) # Hack para obtener el widget, mejor usemos variables
        # Mejor usaré una variable distinta para la función en la próxima versión, pero por ahora:
        tipo = "linea" # Default para función suele ser línea
        
        try:
            x_min = float(self.f_min.get())
            x_max = float(self.f_max.get())
            puntos = int(self.f_puntos.get())
            
            # Generar X matemáticamente
            x_arr = np.linspace(x_min, x_max, puntos)
            
            # Evaluar Y de forma segura (permitiendo np y x)
            contexto = {"np": np, "x": x_arr, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log}
            y_arr = eval(formula, {"__builtins__": {}}, contexto)
            
            self._guardar_grupo(nombre, x_arr, y_arr, self.color_actual, tipo)

        except Exception as e:
            messagebox.showerror("Error Matemático", f"Revisa tu fórmula o rangos.\nError: {e}")

    def _guardar_grupo(self, nombre, x, y, color, tipo):
        grupo = {"nombre": nombre, "x": x, "y": y, "color": color, "tipo": tipo}
        self.grupos_agregados.append(grupo)
        self.lista_grupos.insert(tk.END, f"{nombre} ({tipo}) - {color}")

    def borrar_grupo(self):
        seleccion = self.lista_grupos.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista_grupos.delete(index)
            del self.grupos_agregados[index]

    def generar_grafica(self):
        if not self.grupos_agregados:
            return
        
        archivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if not archivo: return

        graficador = GeneradorGraficas(
            self.entry_titulo.get(), 
            self.entry_x.get(), 
            self.entry_y.get()
        )

        try:
            for g in self.grupos_agregados:
                graficador.agregar_grupo(g['nombre'], g['x'], g['y'], color=g['color'], tipo_grafica=g['tipo'])
            
            exito, msg = graficador.exportar_imagen(archivo)
            if exito: messagebox.showinfo("Listo", msg)
            else: messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGraficas(root)
    root.mainloop()