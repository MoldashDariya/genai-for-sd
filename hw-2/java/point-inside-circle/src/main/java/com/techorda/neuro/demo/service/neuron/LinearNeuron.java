package com.techorda.neuro.demo.service.neuron;

/**
 * Linear Neuron implementation
 * This class provided as example of custom neuron implementation
 * Please implement your oun neuron by extending Neuron class
 */
public class LinearNeuron extends Neuron{

    public LinearNeuron(int inputCount) {
        super(inputCount);
    }

    @Override
    protected double activationFunction(double x) {
        return x;
    }

    @Override
    public double derivative(double x) {
        return 1.0;
    }
}
