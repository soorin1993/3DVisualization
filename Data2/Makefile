# Variables
CC = gcc
CFLAGS = -lm  -m64 -o0 -Wall -Wextra -std=gnu99 -pedantic -ggdb 

# Targets
ALL : run

run : main.c chargetransport.o matrix.o read.o charge.o linklist.o clusterfunctions.o clustersitenode.o cluster.o sitenode.o montecarlo.o functions.o io.o
	$(CC) $(CFLAGS) main.c chargetransport.o read.o charge.o matrix.o linklist.o clusterfunctions.o clustersitenode.o cluster.o sitenode.o functions.o io.o montecarlo.o -o run

chargetransport.o : ../CHARGETRANSPORT/chargetransport.c
	$(CC) $(CFLAGS) -c ../CHARGETRANSPORT/chargetransport.c -o chargetransport.o

charge.o : ../CHARGE/charge.c
	$(CC) $(CFLAGS) -c ../CHARGE/charge.c -o charge.o

#mem.o : ../MEM/mem.c
#	$(CC) $(CFLAGS) -c ../MEM/mem.c -o mem.o

functions.o : ../FUNCTIONS/functions.c
	$(CC) $(CFLAGS) -c ../FUNCTIONS/functions.c -o functions.o

read.o : ../PARAMETERS/read.c
	$(CC) $(CFLAGS) -c ../PARAMETERS/read.c -o read.o

clusterfunctions.o : ../CLUSTER/CLUSTERFUNCTIONS/clusterfunctions.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/clusterfunctions.c -o clusterfunctions.o

linklist.o : ../CLUSTER/CLUSTERFUNCTIONS/LINKLIST/linklist.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/LINKLIST/linklist.c -o linklist.o

montecarlo.o : ../CLUSTER/CLUSTERFUNCTIONS/MONTECARLO/montecarlo.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/MONTECARLO/montecarlo.c -o montecarlo.o

sitenode.o : ../CLUSTER/CLUSTERFUNCTIONS/SITENODE/sitenode.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/SITENODE/sitenode.c -o sitenode.o

cluster.o : ../CLUSTER/CLUSTERFUNCTIONS/DATASTRUCT/cluster.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/DATASTRUCT/cluster.c -o cluster.o

matrix.o : ../CLUSTER/CLUSTERFUNCTIONS/MATRIX/matrix.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERFUNCTIONS/MATRIX/matrix.c -o matrix.o

clustersitenode.o : ../CLUSTER/CLUSTERSITENODE/clustersitenode.c
	$(CC) $(CFLAGS) -c ../CLUSTER/CLUSTERSITENODE/clustersitenode.c -o clustersitenode.o

io.o : ../IO/io.c
	$(CC) $(CFLAGS) -c ../IO/io.c -o io.o

.PHONY: clean
clean:
	$(RM) *.o
