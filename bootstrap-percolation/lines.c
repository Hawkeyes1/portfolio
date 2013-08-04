#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 500
#define samplesize 10000
#define theta 8
#define pcrit 0.003162277660168379
#define da 0.1
#define randmax 4294967295LL
#define pointmax 10


void randomize(int arr[N][N], double p);
int timestep(int arr[N][N], int threshold);
int spans(int arr[N][N], int threshold);
double prob(int threshold, double p, int samples);
void report(void);
void linesinfo(int arr[N][N], int rowdata[pointmax]);

double my_rand(void);
void seedCMWC(void);
unsigned long CMWC(void);
unsigned long Q[4096],c=362436;
	
int main(void) {
    seedCMWC();
    double p;
    int arr[N][N],rows[N],i;
    printf("ROWS - 1 THROUGH %d\n",pointmax-1);
    for(p=0;p<.01;p+=0.0001) {
        randomize(arr,p);
        linesinfo(arr,rows);
        printf("%.4f ",p);
        for(i=1;i<pointmax;i++) {
            printf("%5d ",rows[i]);
            }
        printf("\n");
        }
	return 0;
	}

unsigned long CMWC(void){
	unsigned long long t, a=18782LL,b=4294967295LL;
	unsigned long j=4095;
	unsigned long x,r=b-1;
	j=(j+1)&4095;
	t=a*Q[j]+c;
	c=(t>>32); t=(t&b)+c;
	if(t>r) {c++; t=t-b;}
	return(Q[j]=r-t);
	}

void seedCMWC(void) {
	int i;
	srand(time(0));
	c = rand()%18782;
	for(i=0;i<4096;i++) {
		Q[i] = rand();int spans(int arr[N][N], int threshold);
		}
	}

double my_rand(void) {
	return(((double) CMWC()) / randmax);
	}

void randomize(int arr[N][N], double p) {
    int i,j;
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
            arr[i][j]=0;
            if(my_rand()<=p)
                arr[i][j]=1;
            }
        }
    }
    
int timestep(int arr[N][N], int threshold) {
    int i,j,rowcount[N],colcount[N],changed=0;
    for(i=0;i<N;i++) {
        rowcount[i] = colcount[i] = 0;
        }
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
            if(arr[i][j]) {
                rowcount[i]++;
                colcount[j]++;
                }
            }
        }
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
            if(!arr[i][j] && (rowcount[i]+colcount[j]>=threshold)) 
                arr[i][j]=changed=1;
            else
                continue;
            }
        }
    return changed;
    }
   
int spans(int arr[N][N], int threshold) {
    while(timestep(arr,threshold))
        continue;
    int i,j;
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
            if(!arr[i][j])
                return 0;
            else continue;
            }
        }
    return 1;
    }
    
double prob(int threshold, double p, int samples) {
    int arr[N][N],i,successes=0;
    for(i=0;i<samples;i++) {
        randomize(arr,p);
        successes+=spans(arr,threshold);
        }
    return successes/((float) samples);
    }
    
void report(void) {
    printf("N=%d, theta=%d, samplesize=%d, pcrit=%f.\n",N,theta,samplesize,pcrit);
    }

void linesinfo(int arr[N][N], int rowdata[pointmax]) {
    int i,j,rowcount[N];
    for(i=0;i<N;i++) {
        rowcount[i]=0;
        }
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
            if(arr[i][j]==1) {
                rowcount[i]+=1;
                }
            }
        }
    for(i=0;i<pointmax;i++) {
        rowdata[i]=0;
        }
    for(j=0;j<pointmax;j++) {
        for(i=0;i<N;i++) {
            if (rowcount[i] >= j) {
                rowdata[j] += 1;
                }
            }
        }
    }
 

    
            
        
        
