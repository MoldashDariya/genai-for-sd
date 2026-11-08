// src/test/java/com/techorda/neuro/demo/service/NeuronNetworkTest.java
package com.techorda.neuro.demo.service;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class NeuronNetworkTest {

    @Test
    void testPredictReturnsFiniteOutput() {
        NeuronNetwork network = new NeuronNetwork();
        double[] input = {0.5, -0.2};
        double[] output = network.predict(input);
        assertEquals(1, output.length);
        assertTrue(Double.isFinite(output[0]));
    }

    @Test
    void testTrainImprovesPrediction() {
        NeuronNetwork network = new NeuronNetwork();
        double[][] inputs = {
                {0.0, 0.0},
                {1.0, 1.0}
        };
        double[][] outputs = {
                {0.0},
                {1.0}
        };

        double[] before = network.predict(inputs[1]);
        network.train();
        double[] after = network.predict(inputs[1]);
        assertTrue(Math.abs(after[0] - 1.0) < Math.abs(before[0] - 1.0));
    }
}