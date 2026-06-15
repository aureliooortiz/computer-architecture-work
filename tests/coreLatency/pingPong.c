#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <limits.h>
#include <x86intrin.h>

volatile int flag = 0; // Garante que o compilador não aplique otimizações
//struct timespec t1, t2;
unsigned long long t1, t2;

void defAfinidade (int nucleoID) {
	cpu_set_t cpuSet;
	pthread_t atual;
	
	CPU_ZERO(&cpuSet);
	CPU_SET(nucleoID, &cpuSet);
	
	atual = pthread_self();
	pthread_setaffinity_np(atual, sizeof(cpu_set_t), &cpuSet);
}

void *nucA (void *arg) {
	int nucleoID;

	nucleoID = *(int *)arg;
	defAfinidade(nucleoID);

	t1 = __rdtsc();
	atomic_store(&flag, 1);
	
	return NULL;
}

void *nucB (void *arg) {
	int nucleoID;
	
	nucleoID = *(int *)arg;
	defAfinidade(nucleoID);
	
	while(atomic_load(&flag) == 0);
	t2 = __rdtsc();
	
	return NULL;
}

int main() {
	pthread_t thread1, thread2;
	int core0;
	int core1;
	double dt;
	
	core0 = 0;
	core1 = 1;
	pthread_create(&thread1, NULL, nucA, &core0);
	pthread_create(&thread2, NULL, nucB, &core1);

	// Aguarda o término das threads
	pthread_join(thread1, NULL);
	pthread_join(thread2, NULL);
	
	printf("%llu\n%llu\n", t1, t2);
	
	return 0;
}
