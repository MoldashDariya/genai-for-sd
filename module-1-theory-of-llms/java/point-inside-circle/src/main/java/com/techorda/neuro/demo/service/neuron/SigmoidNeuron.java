package com.techorda.neuro.demo.service.neuron;

/**
 * Neuron with the sigmoid activation function.
 * Output range: (0, 1), so it can be read as a probability.
 */
public class SigmoidNeuron extends Neuron {

    public SigmoidNeuron(int inputCount) {
        super(inputCount);
    }

    @Override
    protected double activationFunction(double x) {
        return 1.0 / (1.0 + Math.exp(-x));
    }

    /**
     * Derivative of sigmoid at the weighted sum {@code x}: f'(x) = f(x) * (1 - f(x)).
     */
    @Override
    public double derivative(double x) {
        double fx = activationFunction(x);
        return fx * (1.0 - fx);
    }
}
