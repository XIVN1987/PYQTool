#include <stdint.h>

#define Ncoef  <n_coef>

float iir(float NewSample
{
	float coefA[Ncoef+1] = {
		<coef_a>
	};

	float coefB[Ncoef+1] = {
		<coef_b>
	};

	static float x[Ncoef+1];	//input samples
	static float y[Ncoef+1];	//output samples

	//shift the old samples
	for(int i = Ncoef; i > 0; i--) {
		x[i] = x[i-1];
		y[i] = y[i-1];
	}

	//Calculate the new output
	x[0] = NewSample;
	y[0] = coefA[0] * x[0];
	for(int i = 1; i <= Ncoef; i++)
		y[0] += coefA[i] * x[i] - coefB[i] * y[i];
	
	return y[0];
}
