#include <stdio.h>

void printVector(int* v, size_t n) {
    for (size_t i = 0; i < n; i++) {
        printf("%d ", v[i]);
    }
    printf("\n");
}

void producto_escalar_vectorial(int a, int* v, size_t n) {
    for (size_t i = 0; i < n; i++) {
        v[i] *= a;
    }
}

int main(void)
{
    int a[4] = {1, 2, 3, 4};

    printVector(a, 4);
    producto_escalar_vectorial(2, a, 4);
    printVector(a, 4);

    return 0;
}