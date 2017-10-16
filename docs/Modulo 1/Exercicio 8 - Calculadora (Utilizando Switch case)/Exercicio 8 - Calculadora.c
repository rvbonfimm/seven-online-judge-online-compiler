#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{ char op;
  float a,b,c;
  printf("Escolha o operador:\n");
  scanf("%c",&op);
  printf("entre com o valor de a:\n");
  scanf("%f",&a);
  printf("entre com o valor de b:\n");
  scanf("%f",&b);

  switch (op)
  {
         case '*': c = a * b;
         printf("%.2f\n", c);
         break;
         case '/': c = a /b;
         printf("%.2f\n", c);
         break;
         case '+': c = a + b;
         printf("%.2f\n", c);
         break;
         case '-': c = a - b;
         printf("%.2f\n", c);
         break;
         default: printf("op nao encontrado\n");
         }
         system("PAUSE");	
          return 0;
}
