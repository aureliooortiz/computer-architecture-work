#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>

#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>

// Função que cada thread vai executar
void *tarefa_nucleo(void *arg) {
	int nucleo_id;
	cpu_set_t cpuset;
	pthread_t atual;
	
	nucleo_id = *(int *)arg;

	// Configura a afinidade para o núcleo específico
	CPU_ZERO(&cpuset);
	CPU_SET(nucleo_id, &cpuset);

	// Pega o ID da thread atual e aplica a afinidade
	atual = pthread_self();
	pthread_setaffinity_np(atual, sizeof(cpu_set_t), &cpuset);
	
	printf("Thread rodando no núcleo %d\n", nucleo_id);
	
	// ... Seu código de processamento pesado aqui ...
	
	return NULL;
}

int main() {
	pthread_t thread1, thread2;
	int core0;
	int core1;
	
	core0 = 0;
	core1 = 1;
	// Cria a thread 1 e a thread 2
	pthread_create(&thread1, NULL, tarefa_nucleo, &core0);
	pthread_create(&thread2, NULL, tarefa_nucleo, &core1);

	// Aguarda o término das threads
	pthread_join(thread1, NULL);
	pthread_join(thread2, NULL);

	return 0;
}

