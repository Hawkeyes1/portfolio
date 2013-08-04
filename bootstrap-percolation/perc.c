#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 100
#define samplesize 100
#define theta 2
#define pcrit 0.0001
#define da 0.1
#define randmax 4294967295LL


void randomize(int arr[N][N], double p);
int timestep(int arr[N][N], int threshold);
int spans(int arr[N][N], int threshold);
double prob(int threshold, double p, int samples);
void report(void);

double my_rand(void);
void seedCMWC(void);
unsigned long CMWC(void);
unsigned long Q[4096],c=362436;
	
int main(void) {
    seedCMWC();
    double a=0,curr=0,prev1=0,prev2=0;
    report();
    while((curr+prev1+prev2)/3<0.99) {
        prev2=prev1;
        prev1=curr;
        a += da;
        curr = prob(theta,a*pcrit,samplesize);
        printf("%.2f %.5f\n",a,curr);
        }
	return 0;
	}

// Taken from a mailing list post by George Marsaglia.  This 
// generator seems to work well.  I probably could have used the built in
// one and been fine.
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
		Q[i] = rand();
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
    // Update arr in place according to one time step of the percolation
    // rules; return 1 iff it changed.
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
    // return 1 iff arr eventually becomes completely occupied,
    // after following the percolation rules.
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
    // estimate probability of spanning with the given parameters
    int arr[N][N],i,successes=0;
    for(i=0;i<samples;i++) {
        randomize(arr,p);
        successes+=spans(arr,threshold);
        }
    return successes/((float) samples);
    }
    
void report(void) {
    printf("#N=%d, theta=%d, samplesize=%d, pcrit=%f.\n",N,theta,samplesize,pcrit);
    }

 

    
            
        
        
