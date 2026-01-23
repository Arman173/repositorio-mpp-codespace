#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define DIM 2000
double x[DIM][DIM], y[DIM][DIM];

int main()
{
   int i, j;
   uint64_t tiempo;
   struct timespec ini, fin;

   for(i=0; i<DIM; i++)
     for(j=0; j<DIM; j++)
     {
          x[i][j] = 1.0;
          y[i][j] = 2.0;
     }

   clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&ini);
   for(i=0; i<DIM; i++)
     for(j=0; j<DIM; j++)
       x[i][j] = x[i][j]+2*y[i][j];
   clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&fin);
   tiempo = 1e9*(fin.tv_sec - ini.tv_sec) + (fin.tv_nsec - ini.tv_nsec);
   printf("Tiempo filas: %.3f ms \n", tiempo/1000000.0);

   clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&ini);
   for(j=0; j<DIM; j++)
     for(i=0; i<DIM; i++)
       x[i][j] = x[i][j]+2*y[i][j];
   clock_gettime(CLOCK_PROCESS_CPUTIME_ID,&fin);
   tiempo = 1e9*(fin.tv_sec - ini.tv_sec) + (fin.tv_nsec - ini.tv_nsec);
   printf("Tiempo columnas: %.3f ms \n", tiempo/1000000.0);

}
