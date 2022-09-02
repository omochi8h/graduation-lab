2
#include<stdio.h>
int main(void){
int n,m,i,sum,max,a[15];
for(i=0;i<15;i++){
a[i]=0;
}
for(i=0;sum<=200;i++){
scanf("%d",&n);
sum+=n;
a[n-1]++;
}

for(i=1;i<16;i++){
printf("%d:%d回\n",i,a[i]);
if(max<a[i]){
m=i;
max=a[i];
}
}
return 0;
}

4
#include<stdio.h>
int main(void){
int n,m,i,sum,max,a[15],b[15];
for(i=0;i<15;i++){
a[i]=0;
}
for(i=0;i<15;i++){
b[i]=0;
}
sum=0;
while(sum<=200){
scanf("%d",&n);
sum+=n;
a[n-1]++;
b[n-1]=i+1;
}

for(i=0;i<15;i++){
printf("%d:%d回\n",i+1,a[i]);
if(max<a[i]){
m=i+1;
max=a[i];
}
}

printf("最も多く入力された整数：%d\n",m);
printf("その入力回数：%d\n",max);
printf("%dが最後に入力されたのは%d回目\n",m,b[m]);
return 0;
}


1
#include<stdio.h>
int main(void){
int n,m,i,j,sum,a[15];
for(i=0;i<15;i++){
a[i]=0;
}
for(i=0;sum<=200;i++){
scanf("%d",&n);
sum+=n;
a[n-1]++;
}

for(j=1;j<16;j++){
printf("%d:%d回\n",j,a[j]);
if(max<a[j]){
m=j;
max=a[j];
}
return 0;
}

3
#include<stdio.h>
int main(void){
int n,m,i,j,sum,max,a[15];
for(i=0;i<15;i++){
a[i]=0;
}
for(i=0;sum<=200;i++){
scanf("%d",&n);
sum+=n;
a[n-1]++;
}
printf("%d\n",sum);
for(j=1;j<16;j++){
printf("%d:%d回\n",j,a[j]);
if(max<a[j]){
m=j;
max=a[j];
}
}
return 0;
}