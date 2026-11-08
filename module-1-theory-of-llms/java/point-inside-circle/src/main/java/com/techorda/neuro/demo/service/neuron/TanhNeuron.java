package com.techorda.neuro.demo.service.neuron;

/**
 * Neuron with the hyperbolic tangent activation function.
 * Output range: (-1, 1).
 */
public class TanhNeuron extends Neuron {

    public TanhNeuron(int inputCount) {
        super(inputCount);
    }

    @Override
    protected double activationFunction(double x) {
        return Math.tanh(x);
    }

    /**
     * Derivative of tanh at the weighted sum {@code x}: f'(x) = 1 - f(x)^2.
     */
    @Override
    public double derivative(double x) {
        double fx = Math.tanh(x);
        return 1.0 - fx * fx;
    }
}
