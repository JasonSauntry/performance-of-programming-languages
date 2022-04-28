package benchmarkJava;

import java.util.Random;
import java.lang.StringBuilder;

import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;

import benchmarkJava.Common;

public class MatrixOpt {
    public static long act(int size) {
        DMatrixRMaj a = getRandMatrix(size);
        DMatrixRMaj b = getRandMatrix(size);

        long start = System.currentTimeMillis();
        DMatrixRMaj c = CommonOps_DDRM.mult(a, b, null);
        long end = System.currentTimeMillis();

        System.err.println(a);
        System.err.println(b);
        System.err.println(c);

        return end - start;
    }

    public static DMatrixRMaj getRandMatrix(int size) {
        DMatrixRMaj mat = new DMatrixRMaj(size, size);
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                mat.set(i, j, Common.getNumber());
            }
        }
        return mat;
    }
}
