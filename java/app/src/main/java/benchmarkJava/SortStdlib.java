package benchmarkJava;

import java.util.ArrayList;

import benchmarkJava.Common;

public class SortStdlib {
    public static long act(int size) {
        ArrayList<Double> l = new ArrayList<Double>(size);

        for (int i = 0; i < size; i++) {
            l.add(Common.getNumber());
        }
        long start = System.currentTimeMillis();
        l.sort((Double a, Double b) -> Double.compare(a, b));
        long end = System.currentTimeMillis();

        if (size < 50) {
            System.out.println(l);
        } else {
            System.out.println(l.get(Common.rand.nextInt(size)));
        }

        return end - start;
    }
}
