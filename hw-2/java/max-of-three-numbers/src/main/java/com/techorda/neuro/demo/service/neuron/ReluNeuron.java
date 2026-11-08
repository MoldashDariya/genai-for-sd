package com.techorda.neuro.demo.service.neuron;

/**
 * Neuron with the ReLU activation function: f(x) = max(0, x).
 * ReLU networks represent piecewise linear functions (such as max) very well:
 * max(a, b) = b + relu(a - b).
 */
public class ReluNeuron extends Neuron {

    public ReluNeuron(int inputCount) {
        super(inputCount);
    }

    @Override
    protected double activationFunction(double x) {
        return Math.max(0.0, x);
    }

    /**
     * Derivative of ReLU at the weighted sum {@code x}: 1 if x > 0, otherwise 0.
     */
    @Override
    public double derivative(double x) {
        return x > 0 ? 1.0 : 0.0;
    }
}
