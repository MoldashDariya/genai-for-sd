package com.techorda.neuro.demo.service;

import com.techorda.neuro.demo.service.neuron.Neuron;
import com.techorda.neuro.demo.service.neuron.NeuronType;
import lombok.Getter;

/**
 * Represents a layer of neurons in a neural network.
 */
@Getter
public class NeuronLayer {

    private Neuron[] neurons;

    /**
     * Creates a fully connected layer.
     *
     * @param inputCount  number of inputs of every neuron (size of the previous layer)
     * @param neuronCount number of neurons in this layer
     * @param type        activation function of the neurons
     */
    public NeuronLayer(int inputCount, int neuronCount, NeuronType type) {
        neurons = new Neuron[neuronCount];
        for (int i = 0; i < neuronCount; i++) {
            neurons[i] = type.create(inputCount);
        }
    }

    /**
     * Activates all neurons in the layer with the given inputs.
     *
     * @param inputs the input values to the layer
     * @return the output values from all neurons in the layer
     */
    public double[] activate(double[] inputs) {
        double[] outputs = new double[neurons.length];
        for (int i = 0; i < neurons.length; i++) {
            outputs[i] = neurons[i].activate(inputs);
        }
        return outputs;
    }

    public int size() {
        return neurons.length;
    }
}
