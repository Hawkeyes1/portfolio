#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 200
#define samplesize 100
#define theta 3
#define pcrit .000025
#define da 0.05
#define randmax 4294967295LL


// Global data for algorithm and RNG
static char arr[N][N][N];
static int rowIJ[N][N];
static int rowJK[N][N];
static int rowKI[N][N];
static unsigned long Q[4096],c=362436;

// Percolation functions
void randomize(double p);
int timestep(void);
int spans(void);
double prob(double p);
void report(void);

// RNG functions
double my_rand(void);
void seedCMWC(void);
unsigned long CMWC(void);

	
int main(void) {
    // Check p-values in a range about pcrit, and stop when 3 values in a row
    // average >= .99
    //
    // Note - we might cut down on running time by starting a = .5 or something
    // since it seems that both theory and computers give ~0 spanning probability
    // in this region.
    seedCMWC();
    double a=0.,curr=0.,prev1=0.,prev2=0.;
    report();
    while((curr+prev1+prev2)<2.97) {
        prev2=prev1;
        prev1=curr;
        a += da;
        curr = prob(a*pcrit);
        printf("%.2f %.5f\n",a,curr);
        }
	return 0;
	}

// I don't understand this RNG but it gives good results.  TO DO: look at the
// literature to see what's happening.
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

void randomize(double p) {
    // Turn points on with probability p.
    int i,j,k;
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
			for(k=0;k<N;k++) {
                if(my_rand()<=p) arr[i][j][k]=1;
                else arr[i][j][k]=0;
           		}
        	}
    	}
    }

int timestep() {

    // Use rowIJ, etc. to keep track of how many points are on each line.  Then
    // go through and turn on the appropriate points.  Keep track of whether
    // anything was changed, so we know when to stop.
    int i,j,k,changed=0;
    for(i=0;i<N;i++) {
		for(j=0;j<N;j++) {
     	   rowIJ[i][j]=rowJK[i][j]=rowKI[i][j]=0;
        	}
		}
    
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
			for(k=0;k<N;k++) {
            	if(arr[i][j][k]) {
                	rowIJ[i][j]++;
                	rowJK[j][k]++;
               		rowKI[k][i]++; 
				   }
				}   
		    }
        }
    
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
			for(k=0;k<N;k++) {
        	    if(!arr[i][j][k] && rowIJ[i][j] + rowJK[j][k] + rowKI[k][i] >= theta) 
            	    arr[i][j][k]=changed=1;
          	  	}
       	 	}
		}
    return changed;
    }
   
int spans() {
    while(timestep())
        continue;
    // After that while loop, no further percolation occurs, so just check the grid.
    int i,j,k;
    for(i=0;i<N;i++) {
        for(j=0;j<N;j++) {
			for(k=0;k<N;k++) {
        	    if(!arr[i][j][k])
                return 0;
            else continue;
            	}
        	}
		}
    return 1;
    }
    
double prob(double p) {
    int i,successes=0;
    for(i=0;i<samplesize;i++) {
        randomize(p);
        successes+=spans();
        }
    return ( (double) successes)/samplesize;
    }
    
void report(void) {
    printf("#N=%d, theta=%d, samplesize=%d, pcrit=%f.\n",N,theta,samplesize,pcrit);
    }

 

    
            
        
        
