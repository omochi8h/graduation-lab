#include<stdio.h>
int main(void){
int n;
printf("点数を入力してください\n");
scanf("%d" ,&n);
if(n>=90)printf("S");
else if(n>=80)printf("A");
else if(n>=70)printf("B");
else if(n>=60)printf("C");
	else printf("F");

return 0;
}