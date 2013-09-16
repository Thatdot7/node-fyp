#include "handlers_list.h"
#include <fcntl.h>
#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <sys/time.h>
#include <math.h>

static const char *device = "/dev/spidev0.0";
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t data_ready = PTHREAD_COND_INITIALIZER;

int main(int argc, char *argv[])
{
	int fd, i, j;
	pthread_t calc_process;

	fd = open(device, O_RDWR);
	sample_struct sample_buffer;

	pthread_create( &calc_process, NULL, calculation_thread, (void*) &sample_buffer);

	struct timeval x;

	while(1)
	{
		pthread_mutex_lock( &mutex1 );
		for ( i=0; i < SAMPLE_SIZE; i++)
		{
			gettimeofday(&x, 0);
			double y = (double)x.tv_sec + (double) x.tv_usec / 1e6;
			sample_buffer.V[i] = transfer(fd, 0);
			sample_buffer.I[i] = transfer(fd, 1);

			//sample_buffer.V[i] = (unsigned int) (500 * sin(0.5*y) + 512);
			//sample_buffer.I[i] = 513;
			usleep(100);
		}

		pthread_cond_signal( &data_ready);
		pthread_mutex_unlock( &mutex1);
		//printf("%d\t%d\n", sample_buffer.V[0], sample_buffer.I[0]);
	}
	close(fd);
	return 0;

}
