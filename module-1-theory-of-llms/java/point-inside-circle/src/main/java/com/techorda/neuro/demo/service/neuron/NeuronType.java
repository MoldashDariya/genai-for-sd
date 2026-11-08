package com.techorda.neuro.demo.service.neuron;

/**
 * Available neuron (activation function) types.
 */
public enum NeuronType {
    LINEAR,
    SIGMOID,
    TANH;

    /**
     * Creates a neuron of this type.
     *
     * @param inputCount number of inputs of the neuron
     * @return new neuron
     */
    public Neuron create(int inputCount) {
        switch (this) {
            case LINEAR:
                return new LinearNeuron(inputCount);
            case SIGMOID:
                return new SigmoidNeuron(inputCount);
            case TANH:
                return new TanhNeuron(inputCount);
            default:
                throw new IllegalStateException("Unknown neuron type: " + this);
        }
    }
}
