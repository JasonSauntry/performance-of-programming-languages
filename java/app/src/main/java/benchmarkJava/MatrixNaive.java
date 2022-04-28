package benchmarkJava;

import java.util.Random;
import java.lang.StringBuilder;

import benchmarkJava.Common;

public class MatrixNaive {
    public static long act(int size) {
        MatrixNaive a = new MatrixNaive(size, true);
        MatrixNaive b = new MatrixNaive(size, true);

        long start = System.currentTimeMillis();
        MatrixNaive c = a.multiply(b);
        long end = System.currentTimeMillis();

        // System.err.println(a);
        // System.err.println(b);
        // System.err.println(c);

        return end - start;
    }

    private double buffer[][];
    private final int size;

    public MatrixNaive(int size, boolean initRand) {
        this.size = size;
        this.buffer = new double[size][size];

        if (initRand) {
            for (int i = 0; i < this.size; i++) {
                for (int j = 0; j < this.size; j++) {
                    this.buffer[i][j] = Common.getNumber();
                }
            }
        }
    }

    public MatrixNaive multiply(MatrixNaive that) {
        MatrixNaive ret = new MatrixNaive(size, false);
        for (int i = 0; i < this.size; i++) {
            for (int j = 0; j < this.size; j++) {
                for (int k = 0; k < this.size; k++) {
                    ret.buffer[i][j] += this.buffer[k][j] * that.buffer[i][k];
                }
            }
        }
        return ret;
    }

    public String toString() {
        StringBuilder ret = new StringBuilder();
        for (int i = 0; i < this.size; i++) {
            for (int j = 0; j < this.size; j++) {
                ret.append(String.format("% -6.2f ", this.buffer[i][j]));
            }
            ret.append('\n');
        }

        return ret.toString();
    }


}
