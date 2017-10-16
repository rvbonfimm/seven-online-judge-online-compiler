#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

//Quadrado de um numero

int main() {
	int i, n, soma=0;
	
	scanf("%d", &n);
	
	if (n < 0) n = -n;
	
	for(i = 1; n > 0; n--){
		soma += i;
		i += 2;
	}
	printf("O quadrado de %d e\n",&n, &soma);
	system("PAUSE");
	return 0;
}
