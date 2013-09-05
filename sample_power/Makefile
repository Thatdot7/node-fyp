all: test_sample

test_sample: main.o calculation.o logging.o setup.o
	gcc *o -o test_sample -lpthread -lsqlite3 -lm

*o: *c
	gcc -c *c

clean:
	rm -rf *o test_sample
