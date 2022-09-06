#include<stdio.h>
int main(void){
int n;
printf("点数を入力してください\n");
scanf("%d" ,&n);
if(n>=90)printf("S\n");
if(n>=80 & n<90)printf("A\n");
if(n>=70 & n<80)printf("B\n");
if(n>=60 & n<70)printf("C\n");
else printf("F\n");

return 0;
}