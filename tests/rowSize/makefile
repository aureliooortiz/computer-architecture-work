CC=gcc
CFLAGS=-O2

all: stride

stride: stride.c
	$(CC) $(CFLAGS) stride.c -o stride

run: stride
	./stride.sh

graphs:
	python3 graficos.py

clean:
	rm -f stride
	rm -f *.png
	rm -f *.csv
	rm -f regiao.txt