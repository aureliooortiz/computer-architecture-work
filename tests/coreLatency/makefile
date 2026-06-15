CC = gcc
CFLAGS = -O2 -Wall -pthread
TARGET = pingPong
SRC = pingPong.c
N = 50

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

run: $(TARGET)
	@for i in $$(seq 1 $(N)); do ./$(TARGET); done | sort -n | head -1

clean:
	rm -f $(TARGET)

.PHONY: all run clean
