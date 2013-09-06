#include "handlers_list.h"
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <sqlite3.h>
#include <sys/time.h>

extern pthread_mutex_t mutex2;
extern pthread_cond_t logging_ready;

int count;

static int callback(void *return_msg, int argc, char **argv, char **azColName)
{
	count = atoi(argv[0]);
	return 0;
}

void *logging_thread(void *logging_array)
{
	logging_struct log_data;
	int i;
	float real_power, energy;

	sqlite3 *db;
	char *sql;
	char sql_update[400];
	char *zErrMsg = 0;
	int rc;

	rc = sqlite3_open("/home/pi/node-fyp/sample_power/test.db", &db);

	while(1)
	{
		pthread_mutex_lock( &mutex2 );
		pthread_cond_wait( &logging_ready, &mutex2 );
		memcpy(&log_data, logging_array, sizeof(logging_struct));
		pthread_mutex_unlock( &mutex2 );

		real_power = 0;
		energy = 0;

		for( i=1; i<PROCESSING_SIZE; i++)
		{
			real_power += log_data.real_power[i];
			energy += log_data.energy[i];
		}

		real_power = real_power / (PROCESSING_SIZE);


		sql = "SELECT counter FROM row_counters WHERE (table_name = 'real_time_record');";
		rc = sqlite3_exec(db, sql, callback, NULL, &zErrMsg);

		if (rc != SQLITE_OK)
		{
			printf("SQL error: %s\n", zErrMsg);
			sqlite3_free(zErrMsg);
		}

		sprintf(sql_update, "UPDATE real_time_record SET time = datetime(CURRENT_TIMESTAMP), real_power = %f, energy = %f WHERE rowID = %d;", real_power, energy, count);
		rc = sqlite3_exec(db, sql_update, NULL, NULL, NULL);

		if(count > 9999){
			count = 0;
		}

		sprintf(sql_update, "UPDATE row_counters SET counter = %d WHERE (table_name = 'real_time_record');", (count+1));
		rc = sqlite3_exec(db, sql_update, NULL, NULL, NULL);
	}
	
}


