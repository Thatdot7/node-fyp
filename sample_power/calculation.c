#include "handlers_list.h"
#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

extern pthread_mutex_t mutex1;
extern pthread_cond_t data_ready;
pthread_mutex_t mutex2 = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t logging_ready = PTHREAD_COND_INITIALIZER;

void *calculation_thread(void *sample)
{
	logging_struct log;
	sample_struct sample_temp;
	int i;
	int count = 0;
	double real_power;
	double energy;

	pthread_t log_process;
	pthread_create( &log_process, NULL, logging_thread, (void *) &log );

	//FILE *f = fopen("data.csv", "a+");

	struct timeval current_time;
	gettimeofday(&current_time, NULL);
	double prev_time = (double) current_time.tv_sec + (double) current_time.tv_usec /1e6;

	while(1)
	{
		pthread_mutex_lock( &mutex1 );
		pthread_cond_wait( &data_ready, &mutex1);
		memcpy(&sample_temp, sample, sizeof(sample_struct));
		pthread_mutex_unlock( &mutex1 );

		for( i=0; i < SAMPLE_SIZE; i++)
		{
			real_power += ((double) sample_temp.V[i] - 508) * 3.3 / 1024 * 252.1 * ((double) sample_temp.I[i] - 512) * 3.3 / 1024 * 11.4;
		}

		real_power = real_power / SAMPLE_SIZE;
		gettimeofday(&current_time, NULL);
		double time_stamp = (double) current_time.tv_sec + current_time.tv_usec / 1e6;
		energy = real_power * (time_stamp - prev_time);

		pthread_mutex_lock( &mutex2 );
		log.real_power[count] = real_power;
		log.energy[count] = energy;

		if (count >= PROCESSING_SIZE)
		{
			count = 0;
			//printf("BATCH SENT\n");
			pthread_cond_signal( &logging_ready);
			
		} else {
			count++;
		}
		pthread_mutex_unlock( &mutex2 );

		// Print debug statements
		//printf("Real Power = %f\tEnergy = %f\tV = %d-%d\tTime = %f\n", log.real_power[count-1], log.energy[count-1], 
		//		sample_temp.V[0], sample_temp.V[SAMPLE_SIZE-1], (time_stamp - prev_time));
		//fprintf(f, "%f, %d, %d, %f\n", time_stamp, sample_temp.V[0], sample_temp.I[0]);
		//printf("Ch1 = %d\tCh2 = %d\n", sample_temp.V[0], sample_temp.I[0]);
		
		// Setting up variables for next round
		real_power = 0;
		prev_time = time_stamp;
	}
}

