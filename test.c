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
printf("��������͂��Ă�������\n");
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
printf("���͉�\n");
for(i=1;i<=15;i++){
printf("%d�F%d��\n",i,a[i]);
}
printf("�ł��������͂��ꂽ�����F%d\n",saihinchi);
printf("���̓��͉񐔁F%d\n",a[saihinchi]);
printf("%d���Ō�ɓ��͂��ꂽ�̂�%d���\n",saihinchi,b[saihinchi]);
return 0;
}