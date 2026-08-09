CC ?= cc
CPPFLAGS ?= -D_POSIX_C_SOURCE=200809L
CFLAGS ?= -O2
FLAGS = -DLONGTYPE

all: drat-trim lrat-check compress decompress gapless

drat-trim: drat-trim.c
	$(CC) $(CPPFLAGS) $(CFLAGS) drat-trim.c -std=c99 -o drat-trim

lrat-check: lrat-check.c
	$(CC) $(CPPFLAGS) $(CFLAGS) lrat-check.c -std=c99 $(FLAGS) -o lrat-check

compress: compress.c
	$(CC) $(CPPFLAGS) $(CFLAGS) compress.c -std=c99 $(FLAGS) -o compress

decompress: decompress.c
	$(CC) $(CPPFLAGS) $(CFLAGS) decompress.c -std=c99 $(FLAGS) -o decompress

gapless: gapless.c
	$(CC) $(CPPFLAGS) $(CFLAGS) gapless.c -std=c99 -o gapless

clean:
	rm -f drat-trim lrat-check compress decompress gapless
