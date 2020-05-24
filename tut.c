#include <stdio.h>
#include <math.h>

int Sigmoid(int in){
	int aft = 1.0/(1.0 + exp(-in));
	int x;
	return aft ;
}

int main(void){
	int in = 0;
	int out = Sigmoid(in) ;    /* Out = Sigmoid(In) */
	return 0;
}