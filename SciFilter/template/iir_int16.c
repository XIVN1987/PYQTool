#include <stdint.h>

#define Ncoef  <n_coef>

int16_t iir(int16_t NewSample)
{
	int16_t coefA[Ncoef+1] = {
		<coef_a>
	};

	int16_t coefB[Ncoef+1] = {
		<coef_b>
	};

	static int16_t x[Ncoef+1];	//input samples
	static int32_t y[Ncoef+1];	//output samples

	//shift the old samples
	for(int i = Ncoef; i > 0; i--) {
		x[i] = x[i-1];
		y[i] = y[i-1];
	}

	//Calculate the new output
	x[0] = NewSample;
	y[0] = coefB[0] * x[0];
	for(int i = 1; i <= Ncoef; i++)
		y[0] += coefB[i] * x[i] - coefA[i] * y[i];
	
	return y[0] >> 15;
}
