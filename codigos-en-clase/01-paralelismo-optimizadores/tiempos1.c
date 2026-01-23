#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#define DIM 2000
double x[DIM][DIM], y[DIM][DIM];

int main()
{
   int i, j, tiempo;
   struct timeval ini, fin;

   for(i=0; i<DIM; i++)
     for(j=0; j<DIM; j++)
     {
          x[i][j] = 1.0;
          y[i][j] = 2.0;
     }

   gettimeofday(&ini,NULL);
   for(i=0; i<DIM; i++)
     for(j=0; j<DIM; j++)
       x[i][j] = x[i][j]+2*y[i][j];
   gettimeofday(&fin,NULL);
   tiempo = 1e6*(fin.tv_sec - ini.tv_sec) + (fin.tv_usec - ini.tv_usec);
   printf("Tiempo filas: %.3f ms \n", tiempo/1000.0);

   gettimeofday(&ini,NULL);
   for(j=0; j<DIM; j++)
     for(i=0; i<DIM; i++)
       x[i][j] = x[i][j]+2*y[i][j];
   gettimeofday(&fin,NULL);
   tiempo = 1e6*(fin.tv_sec - ini.tv_sec) + (fin.tv_usec - ini.tv_usec);
   printf("Tiempo columnas: %.3f ms \n", tiempo/1000.0);

}
