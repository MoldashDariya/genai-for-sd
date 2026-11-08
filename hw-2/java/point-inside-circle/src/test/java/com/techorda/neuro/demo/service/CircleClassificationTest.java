package com.techorda.neuro.demo.service;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CircleClassificationTest {

    private static NeuronNetwork network;

    @BeforeAll
    static void setUp() {
        network = new NeuronNetwork();
    }

    @Test
    void pointsInsideCircleReturnOne() {
        double[][] inside = {{0, 0}, {1, 1}, {3, 3}, {-2, 4}, {0, -4.5}, {4, -1}};
        for (double[] p : inside) {
            assertEquals(1, network.classify(p[0], p[1]), "(" + p[0] + ", " + p[1] + ")");
        }
    }

    @Test
    void pointsOutsideCircleReturnZero() {
        double[][] outside = {{6, 6}, {0, -7}, {-8, 2}, {5.5, 0}, {9, -9}, {-4, 4}};
        for (double[] p : outside) {
            assertEquals(0, network.classify(p[0], p[1]), "(" + p[0] + ", " + p[1] + ")");
        }
    }

    @Test
    void accuracyOnNewTestDataIsHigh() {
        NeuronNetwork.DataSet testData = network.generateData(2000);
        double accuracy = network.accuracy(testData);
        assertTrue(accuracy > 0.95, "accuracy = " + accuracy);
    }
}
