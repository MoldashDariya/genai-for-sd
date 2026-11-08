package com.techorda.neuro.demo.service;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MaxOfThreeTest {

    private static final double DELTA = 0.1;

    private static NeuronNetwork network;

    @BeforeAll
    static void setUp() {
        network = new NeuronNetwork();
    }

    @Test
    void findsMaximumOfKnownTriples() {
        double[][] cases = {
                {0.0, 0.0, 0.0},
                {1.0, 1.0, 1.0},
                {-1.0, -1.0, -1.0},
                {0.5, -0.2, 0.1},
                {-0.7, -0.3, -0.9},
                {0.2, 0.9, -0.4},
                {-0.5, 0.0, 0.8},
                {-1.0, 1.0, 0.0},
        };
        for (double[] c : cases) {
            double expected = Math.max(c[0], Math.max(c[1], c[2]));
            assertEquals(expected, network.max(c[0], c[1], c[2]), DELTA,
                    "max(" + c[0] + ", " + c[1] + ", " + c[2] + ")");
        }
    }

    @Test
    void errorOnNewTestDataIsSmall() {
        NeuronNetwork.DataSet testData = network.generateData(2000);
        double mae = network.meanAbsoluteError(testData);
        assertTrue(mae < 0.05, "mean absolute error = " + mae);
    }
}
