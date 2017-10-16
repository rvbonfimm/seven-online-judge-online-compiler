#include <stdio.h>
#include <stdlib.h>

// Tabuada do 1 ao 10

int main() {
	int i, j, k;
	for (k = 0; k<=4 ; k++){
		for (i = 0 ; i <= 3; i++) 
		printf("Tabuada do %3d       ", i+4*k+1);
		
		for(i = 1; i <= 10 ; i++){
			for(j = 1+4*k; j<= 4+4*k; j++)
			printf("%3d x%3d = %3d     ", j,i,j*i); //imprime o resultado da tabuada
		}
		}
		system("PAUSE");
		return 0;
	}
	
