#include<stdio.h>
int main(void){
int i,sum,max,cnt,saihinchi,inData;
int a[16],b[16];
for(i=0;i<=15;i++){
a[i]=0;
b[i]=1;
}
cnt=0;
sum=0;
do{
cnt++;
printf("整数を入力してください\n");
scanf("%d", &inData);
a[inData]++;
b[inData]=cnt;
sum+=inData;
}while(sum<200);

max=-1;
saihinchi =-1;
for (i=1; i<=15; i++){
if(a[i]>max){
max=a[i];
saihinchi = i;
}
}
printf("入力回数\n");
for(i=1;i<=15;i++){
printf("%d：%d回\n",i,a[i]);
}
printf("最も多く入力された整数：%d\n",saihinchi);
printf("その入力回数：%d\n",a[saihinchi]);
printf("%dが最後に入力されたのは%d回目\n",saihinchi,b[saihinchi]);
return 0;
}