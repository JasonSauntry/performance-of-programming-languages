package benchmarkJava;

import java.util.Random;

class Common {
    public static Random rand = new Random();

    public static double getNumber() {
        return rand.nextGaussian();
    }


}
