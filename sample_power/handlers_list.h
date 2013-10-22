#define SAMPLE_SIZE 10
#define PROCESSING_SIZE 100

typedef struct {
	unsigned int V[SAMPLE_SIZE];
	unsigned int I[SAMPLE_SIZE];
} sample_struct;


typedef struct {
	double real_power[PROCESSING_SIZE];
	double energy[PROCESSING_SIZE];
} logging_struct;

unsigned int transfer(int fd, int adc_channel);
void *calculation_thread(void *sample);
void *logging_thread(void *logging_array);
