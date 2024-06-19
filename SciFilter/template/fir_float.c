#include <stdint.h>

#define Ntap  <n_tap>

float fir(float NewSample)
{
	float coef[Ntap] = {
		<coef_b>
	};

	static float x[Ntap];	//input samples
	float y = 0;			//output sample

	//shift the old samples
	for(int i = Ntap-1; i > 0; i--)
		x[i] = x[i-1];

	//Calculate the new output
	x[0] = NewSample;
	for(int i = 0; i < Ntap; i++)
		y += coef[i] * x[i];
	
	return y;
}
