#include <stdint.h>

#define Ntap  <n_tap>

int16_t fir(int16_t NewSample)
{
	int16_t coef[Ntap] = { 
		<coef_b>
	};

	static int16_t x[Ntap];		//input samples
	int32_t y = 0;				//output sample

	//shift the old samples
	for(int i = Ntap-1; i > 0; i--)
		x[i] = x[i-1];

	//Calculate the new output
	x[0] = NewSample;
	for(int i = 0; i < Ntap; i++)
		y += coef[i] * x[i];
	
	return y >> 15;
}
