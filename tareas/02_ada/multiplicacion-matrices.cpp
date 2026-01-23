/*
    PROGRAMA PARA MULTIPLICAR 2 MATRICES DE N-dimensiones
*/
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <sys/time.h>

#define DEFAULT_DIM 1000;

using namespace std;

int randomIntInRange(int min, int max) {
    return min + rand() % (max - min + 1);
}

void showMatrixN(vector<vector<int>> m, int N) {
    cout << endl;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cout << m[i][j] << " ";
        }
        cout << endl;
    }
}

void generateRandomMatrixN(vector<vector<int>> &m, int N) {
    m.resize(N);
    for (int i = 0; i < N; i++) {
        m[i].resize(N);
        for (int j = 0; j < N; j++) {
            m[i][j] = randomIntInRange(1, 5);
        }
    }
}

int main(int argc, char* argv[]) {
    // Seed the random number generator ONCE at the beginning of the program
    srand(static_cast<unsigned int>(time(NULL)));

    // variables para medir el tiempo
    int tiempo;
    struct timeval ini, fin;

    // creacion de los vectores a usar
    vector<vector<int>> A, B, C;

    // obtenemos la dimension como argumento
    // en caso contrario usamos el por defecto
    int DIM = DEFAULT_DIM;
    if (argc > 1) {
        DIM = stoi(argv[1]);
    }
    // generamos los vectores para la multiplicacion
    generateRandomMatrixN(A, DIM);
    generateRandomMatrixN(B, DIM);
    C.resize(DIM);
    for (int i = 0; i < DIM; i++)
        C[i].resize(DIM);

    // empezamos a medir
    gettimeofday(&ini,NULL);

    // aplicamos la multiplicacion de matrices
    for (int i = 0; i < DIM; i++) {
        for (int j = 0; j < DIM; j++) {
            for (int k = 0; k < DIM; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    // multiplicacion terminada

    // terminamos de medir
    gettimeofday(&fin,NULL);

    // imprimimos el tiempo en la terminal
    tiempo = 1e6*(fin.tv_sec - ini.tv_sec) + (fin.tv_usec - ini.tv_usec);
    printf("Tiempo de la multiplicacion: %.3f ms \n", tiempo/1000.0);

    // mostramos los resultados de la multiplicacion
    // showMatrixN(A, DIM);
    // cout << endl;
    // showMatrixN(B, DIM);
    // cout << endl;
    // showMatrixN(C, DIM);

    return 0;
}