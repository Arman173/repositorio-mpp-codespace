#include <iostream>
#include <vector>
 
using namespace std;
 
 
__attribute__((optimize("unroll-loops")))
void procesar_datos(vector<double>& datos, double factor) {
    // Esta directiva le dice al compilador que aplique desenrollado de bucle
    // para exponer más instrucciones independientes al hardware.
 
    for (size_t i = 0; i < datos.size(); ++i) {
        datos[i] = (datos[i] * factor) + 0.5;
    }
}
 
int main() {
    const size_t N = 100000000;
    vector<double> datos(N, 1.0);
    procesar_datos(datos, 2.5);
    cout << "Proceso terminado" << endl;
    return 0;
}