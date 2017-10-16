#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MAX 1000
#define NUM 77 
 
int main(){
  int i,j;
  int limite;
  char ehprimo[MAX];
  int cont=1;
  int primos[NUM];

  for(i=2;i<MAX;i++) ehprimo[i]=1;
  limite = (int)sqrt(MAX);
  for(i=2;i<limite;i++){
    if(ehprimo[i]){
      for(j=i*i;j<MAX;j=j+i)
        ehprimo[j] = 0;
    }
  }

  for(i=2;i<MAX;i++){
    if(ehprimo[i]){
      printf("%d %d\n",cont,i);
      primos[cont]=i;
      cont++;
    }
  }
  printf("%d\n",cont);   
  system("PAUSE");

}
