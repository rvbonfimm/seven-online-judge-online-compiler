#include <stdio.h>
#include <stdlib.h>

//boletim escolar

int main() {
	char aluno;
	float n1, n2, n3, n4, media;
	scanf("%s", &aluno);
	scanf("%f",&n1);
	scanf("%f",&n2);
	scanf("%f",&n3);
	scanf("%f",&n4);
	media = (n1 + n2 + n3 + n4) / 4;
	printf("A media do aluno e: %.2f\n",media);
	
	if(media < 4) {
		printf("Reprovado\n");
	}
	else if(media >=4 && media <6){
		printf("Em recuperacao\n");
	
	} else{
		printf("Aprovado\n");
		  }
		
	system("PAUSE");
	return 0;
}
