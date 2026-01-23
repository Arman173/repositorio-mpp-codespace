#include <iostream>
#include <vector>
#include <chrono> 
 
 
 
//__attribute__((optimize("unroll-loops")))
 
#pragma GCC push_options
#pragma GCC optimize ("unroll-loops")
 
void procesar_datos(std::vector<double>& datos, double factor) {
    for (size_t i = 0; i < datos.size(); ++i) {
        datos[i] = (datos[i] * factor) + 0.5;
    }
}
#pragma GCC pop_options
 
 
 
int main() {
    const size_t N = 100000000;
    std::vector<double> datos(N, 1.0);
 
    // 1. Capturar tiempo de inicio
    auto inicio = std::chrono::high_resolution_clock::now();
 
    procesar_datos(datos, 2.5);
 
    // 2. Capturar tiempo de fin
    auto fin = std::chrono::high_resolution_clock::now();
 
    // 3. Calcular la duración
    std::chrono::duration<double, std::milli> tiempo = fin - inicio;
 
    std::cout << "Tiempo de ejecución: " << tiempo.count() << " ms" << std::endl;
    return 0;
}