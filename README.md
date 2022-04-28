# Performance of Programming Languages

This project is a comparison of the performance of C, Java and Python on a series of benchmarks. To
read the results, and to read about the experimental design, look in `report.pdf`.

## Organization

Benchmark code is organized in directories by language. The project root contains other files, such
as the final report, the original proposal, data, and analysis scripts.

## Building

### C

The C code depends on GCC, OpenBLAS and Make. Install them both. Then:

```bash
cd c
make

# Run
./heap [n]
./matmul [n]
./matmul_opt [n]
./sort_stdlib [n]
```

### Python

The Python code depends on the Numpy linear algebra library, which can be installed using pip:

```bash
# From project root
# If you're using a Python venv, create and activate it here

pip install -r requirements.txt

# Run
./python/heap.py [n]
./python/matmul.py [n]
./python/matmul_opt.py [n]
./python/sort_stdlib.py [n]
```

### Java

The Java code is built using Gradle and depends on the EJMP linear algebra library. Install Gradle,
then:


```bash
cd java
./gradlew buiild

# Run in development
./gradlew run --args "heap [n]"
./gradlew run --args "matmul [n]"
./gradlew run --args "matmul_opt [n]"
./gradlew run --args "sort_stdlib [n]"

# Build for use from runner script
./gradlew installDist
```

## Running

The script `runner.py` will run all benchmarks and collect their data. The benchmarks are specified
in `benchmark_spec.yaml`, and output will be in `/tmp/foo.tsv`. These paths are hardcoded, I never
got around to making them configurable. If you would like them to not be hardcoded, PRs are welcome.

The script `analysis.py` will process the raw data and draw pretty graphs. The source file is
hardcoded in the script. When I wrote this readme it was `results-4.tsv`, but it's quite likely I
changed it and forgot to update this readme since then.
