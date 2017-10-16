#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//Calculadora 4 operações

int main() {
	float x, y, soma, subtracao, multiplicacao, divisao;
	char op;
	scanf ("%f", &x);
	scanf ("%f", &y);
	scanf ("%s", &op);

	if (op == '+'){
		soma = x + y;
		printf ("O resultado da soma e: %.2f", soma);
	
	} if (op == '-'){
		subtracao = x - y;
		printf ("O resultado da subtracao e: %.2f", subtracao);
		
	} if (op == '*'){
		multiplicacao = x * y;
		printf ("O resultado da multiplicacao e: %.2f", multiplicacao);
		
	} if (op == '/'){
		divisao = x / y;
		printf ("O resultado da divisao e: %.2f", divisao);
	}

}
