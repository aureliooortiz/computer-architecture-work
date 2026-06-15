CC = gcc
CFLAGS = -O2 -march=native

TARGET = cache_size

all: $(TARGET)

$(TARGET): cache_size.c
	$(CC) $(CFLAGS) cache_size.c -o $(TARGET)

run: $(TARGET)
	@echo "Executando benchmark..."
	@bash cache_size.sh

plot:
	@echo "Gerando gráficos..."
	@python3 graficos_cache.py

detect:
	@echo "Detectando regiões..."
	@python3 detectar_regiao.py

full: clean all run detect plot

clean:
	@echo "Limpando arquivos gerados..."
	@rm -f $(TARGET)
	@rm -f miss_rate.png tempo.png regioes.txt
	@rm -f resultados.csv resultados_finos.csv

rebuild: clean all