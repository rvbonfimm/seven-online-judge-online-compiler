#include <stdio.h>
#include <stdlib.h>

//Cara ou coroa

int main() {
	//inicialização das variáveis
	int n, perda=0, ganho=0, resposta, i; 
	printf("Quantas vezes você quer jogar? \n"); 
	scanf("%d",&n); 
	
	for(i=0; i<n; i++){
		printf("Escolha:  0 = Cara  e 1 = Coroa: \n");
		scanf("%d", &resposta);
		while (resposta != 0 && resposta != 1){
			printf("Erro: escolha entre 0 cara e 1 coroa \n");
			scanf("%d", &resposta);
		}
		if((rand()%2)==resposta){
			ganho++;
			if (resposta==0)
				printf("Cara, voce ganhou. \n");
			else
				printf("Coroa, voce ganhou. \n");
		}
		else{
			perda++;
			if(resposta==1)
				printf("Cara, voce perdeu. \n");
			else
				printf("Coroa, voce perdeu \n");
		}
	}
	
	printf("\n Relatorio Final: ");
	printf("\n No. de jogos que voce ganhou:  %d", ganho);
	printf("\n No. de jogos que voce perdeu:  %d\n", perda);
	
	system("PAUSE");
	return 0;
}
