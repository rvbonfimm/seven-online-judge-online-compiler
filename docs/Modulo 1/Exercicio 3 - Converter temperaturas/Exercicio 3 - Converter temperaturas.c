#include <stdio.h>
#include <stdlib.h>

// Converter temperaturas

int main(int argc, char *argv[]) {
	float ftemp; //temperatura em Fahrenheit
	float ctemp; //temperatura em Celsius
	scanf("%f", &ctemp);
	ftemp = ctemp * 9/5 + 32;
	printf ("A temperatura em graus Fahrenheit e %.2f\n", ftemp);
	system("PAUSE");
	return 0;
}
