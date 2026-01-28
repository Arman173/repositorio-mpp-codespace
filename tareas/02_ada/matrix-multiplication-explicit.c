#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define DEFAULT_DIM 1000

// Estructura para representar una matriz
typedef struct {
    int **data;
    int rows;
    int cols;
} Matrix;

void createMatrix(Matrix *m, int rows, int cols) {
    m->rows = rows;
    m->cols = cols;
    m->data = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        m->data[i] = (int *)malloc(cols * sizeof(int));
    }
}

void freeMatrix(Matrix *m) {
    for (int i = 0; i < m->rows; i++) {
        free(m->data[i]);
    }
    free(m->data);
}

void initializeMatrix(Matrix *m) {
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            m->data[i][j] = rand() % 5 + 1; // Valores aleatorios entre 1 y 5
        }
    }
}

void printMatrix(Matrix *m) {
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            printf("%d ", m->data[i][j]);
        }
        printf("\n");
    }
}

// Sacamos la lógica a una función y le aplicamos el atributo
// -------------------------------------------------------------
__attribute__((optimize("unroll-loops")))
void multiplicarMatrices(Matrix *A, Matrix *B, Matrix *C) {
    int i, j, k;
    
    // Optimizacion extra: Guardamos punteros locales para evitar
    // indirecciones constantes a A->data, B->data, etc.
    int **dataA = A->data;
    int **dataB = B->data;
    int **dataC = C->data;

    for (i = 0; i < A->rows; i++) {
        for (j = 0; j < B->cols; j++) {
            int suma = 0; // Usamos variable temporal (registro)
            for (k = 0; k < A->cols; k++) {
                suma += dataA[i][k] * dataB[k][j];
            }
            dataC[i][j] = suma;
        }
    }
}

int main(int argc, char* argv[]) {
    // creamos las matrices A, B y C
    Matrix A, B, C;

    // obtenemos la dimension como argumento
    // en caso contrario usamos el por defecto
    int DIM = DEFAULT_DIM;
    if (argc > 1) {
        DIM = atoi(argv[1]);
    }

    // generamos las matrices con dimension por defecto
    createMatrix(&A, DIM, DIM);
    createMatrix(&B, DIM, DIM);
    createMatrix(&C, DIM, DIM);

    // inicializamos las matrices
    initializeMatrix(&A);
    initializeMatrix(&B);

    // imprimimos las matrices A y B
    // printMatrix(&A);
    // printf("\n");
    // printMatrix(&B);
    // printf("\n");

    // estructura para medir el tiempo
    struct timespec inicio, fin;
    
    // Obtener tiempo inicial ---------------------------------------
    clock_gettime(CLOCK_MONOTONIC, &inicio);
    
    // ---- Algoritmo de multiplicación de matrices ----
    multiplicarMatrices(&A, &B, &C);
    // -------- FIN --------
    
    // Obtener tiempo final ----------------------------------------
    clock_gettime(CLOCK_MONOTONIC, &fin);

    // imprimimos el resultado
    // printMatrix(&C);
    // printf("\n");
    
    // Calcular diferencia
    long long duracion_ns = (fin.tv_sec - inicio.tv_sec) * 1000000000 + 
                       (fin.tv_nsec - inicio.tv_nsec);
    
    printf("Multiplicacion de matriz cuadrada de dimension %d\n", DIM);
    printf("Tiempo: %.3f ms\n", duracion_ns / 1000000.0);

    // limpiamos las matrices
    freeMatrix(&A);
    freeMatrix(&B);
    freeMatrix(&C);
    
    return 0;
}