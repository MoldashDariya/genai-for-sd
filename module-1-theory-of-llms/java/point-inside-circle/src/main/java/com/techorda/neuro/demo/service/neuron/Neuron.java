package com.techorda.neuro.demo.service.neuron;

import lombok.Getter;
import lombok.Setter;

/**
 * Abstract class representing a neuron in a neural network.
 * Each neuron has weights, a bias, and an activation function.
 */
@Getter
@Setter
public abstract class Neuron {

    private double[] weights;
    private double bias;

    /**
     * Constructs a Neuron with a specified number of inputs.
     * Initializes weights and bias with random values in the range [-0.5, 0.5].
     *
     * @param inputCount the number of input connections to this neuron
     */
    public Neuron(int inputCount) {
        weights = new double[inputCount];
        for (int i = 0; i < inputCount; i++) {
            weights[i] = Math.random() - 0.5;
        }
        bias = Math.random() - 0.5;
    }

    /**
     * Calculates the neuron's output for the given inputs using the sigmoid activation function.
     *
     * @param inputs the input values to the neuron
     * @return the activated output value
     */
    public double activate(double[] inputs) {
        return activateSum(weightedSum(inputs));
    }

    /**
     * Calculates the weighted sum of inputs plus bias (the value before the activation function).
     *
     * @param inputs the input values to the neuron
     * @return bias + sum(inputs[i] * weights[i])
     */
    public double weightedSum(double[] inputs) {
        if (inputs.length != weights.length) {
            throw new IllegalArgumentException("Input length does not match weights length.");
        }
        double sum = bias;
        for (int i = 0; i < inputs.length; i++) {
            sum += inputs[i] * weights[i];
        }
        return sum;
    }

    /**
     * Applies the activation function to an already computed weighted sum.
     *
     * @param sum weighted sum returned by {@link #weightedSum(double[])}
     * @return the activated output value
     */
    public double activateSum(double sum) {
        return activationFunction(sum);
    }

    /**
     * Applies the activation function to the input value.
     *
     * @param x the input value
     * @return the result of the sigmoid function
     */
    protected abstract double activationFunction(double x);

    /**
     * Calculates the derivative of the activation function at the given input value.
     *
     * @param x the input value
     * @return the derivative of the activation function
     */
    public abstract double derivative(double x);
}
