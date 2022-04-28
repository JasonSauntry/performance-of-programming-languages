bins=matmul matmul_opt sort_stdlib heap
heads=common.h matmul_common.h

compiler=gcc -std=gnu11 -O3 -g

FLAGS=

all: $(bins)

matmul: matmul.c $(heads)
	$(compiler) $< -o $@ $(FLAGS)

matmul_opt: matmul_opt.c $(heads)
	$(compiler) $< -o $@ $(FLAGS) -lopenblas

sort_stdlib: sort_stdlib.c $(heads)
	$(compiler) $< -o $@ $(FLAGS)

heap: heap.c $(heads)
	$(compiler) $< -o $@ $(FLAGS)

clean: $(bins)
	rm $(bins)
