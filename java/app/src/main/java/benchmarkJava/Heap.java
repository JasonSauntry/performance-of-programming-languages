package benchmarkJava;

import java.lang.IllegalStateException;
import java.util.ArrayList;

import benchmarkJava.Common;

public class Heap<T extends Comparable> {
    public static long act(int size) {
        ArrayList<Double> l = new ArrayList<Double>(size);

        for (int i = 0; i < size; i++) {
            l.add(Common.getNumber());
        }

        System.out.println("Starting sort…");
        long start = System.currentTimeMillis();
        Heap<Double> h = new Heap<Double>();
        for (double e : l) {
            h.push(e);
        }

        ArrayList<Double> o = new ArrayList<Double>(size);
        while (!h.isEmpty()) {
            o.add(h.pop());
        }
        long end = System.currentTimeMillis();
        System.out.println("Done");

        if (size < 50) {
            System.out.println(size);
            System.out.println(o);
        } else {
            System.out.println(o.get(Common.rand.nextInt(size)));
        }

        return end - start;
    }

    HeapNode<T> head = null;

    public void push(T val) {
        if (this.head != null) {
            this.head.push(val);
        } else {
            this.head = new HeapNode<T>(val);
        }
    }

    public T pop() {
        if (this.head != null) {
            T ret = this.head.pop();
            if (this.head.isEmpty()) {
                this.head = null;
            }
            return ret;
        } else {
            throw new IllegalStateException("Cannot pop an empty heap");
        }
    }

    public String toString() {
        if (this.head != null) {
            return this.head.toString();
        } else {
            return "φ";
        }
    }

    public boolean isEmpty() {
        return this.head == null;
    }
}
