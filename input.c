#include<stdio.h>
int main(void){
int n;
printf("点数を入力してください\n");
scanf("%d" ,&n);
if(n>=90)printf("S\n");
else if(n>=80)printf("A\n");
else if(n>=70)printf("B\n");

	else if(n>=60)printf("C\n");
	else printf("F\n");

return 0;
}