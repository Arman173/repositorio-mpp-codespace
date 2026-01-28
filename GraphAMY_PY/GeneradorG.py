import matplotlib.pyplot as plt

class GeneradorGraficas:
    def __init__(self, titulo, label_x, label_y):
        self.titulo = titulo
        self.label_x = label_x
        self.label_y = label_y
        self.grupos = {}

    def agregar_grupo(self, nombre_grupo, datos_x, datos_y, color=None, estilo='-', tipo_grafica='linea'):
        """
        tipo_grafica: 'linea' (usa plot) o 'dispersion' (usa scatter)
        """
        if len(datos_x) != len(datos_y):
            raise ValueError(f"Los datos X e Y del grupo '{nombre_grupo}' deben tener el mismo tamaño.")

        self.grupos[nombre_grupo] = {
            'x': datos_x,
            'y': datos_y,
            'color': color,
            'estilo': estilo,
            'tipo': tipo_grafica
        }

    def exportar_imagen(self, nombre_archivo="grafica_reporte.png"):
        plt.figure(figsize=(10, 6))
        plt.grid(True, linestyle='--', alpha=0.7)

        for nombre, datos in self.grupos.items():
            if datos['tipo'] == 'linea':
                plt.plot(
                    datos['x'], 
                    datos['y'], 
                    label=nombre, 
                    color=datos['color'], 
                    linestyle=datos['estilo'],
                    marker='o', # Marcador opcional, puedes quitarlo si son muchos datos
                    linewidth=2
                )
            elif datos['tipo'] == 'dispersion':
                plt.scatter(
                    datos['x'], 
                    datos['y'], 
                    label=nombre, 
                    color=datos['color'],
                    marker='o', # O 'x', '^', etc.
                    s=50 # Tamaño del punto
                )

        plt.title(self.titulo, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel(self.label_x, fontsize=12)
        plt.ylabel(self.label_y, fontsize=12)
        plt.legend(fontsize=10, shadow=True, fancybox=True)
        plt.tight_layout()

        try:
            plt.savefig(nombre_archivo, dpi=300)
            plt.close()
            return True, f"Gráfica guardada exitosamente en: {nombre_archivo}"
        except Exception as e:
            plt.close()
            return False, str(e)