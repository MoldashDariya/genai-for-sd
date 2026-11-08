package com.techorda.neuro.demo.service;

import com.techorda.neuro.demo.service.neuron.Neuron;
import com.techorda.neuro.demo.service.neuron.NeuronType;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Neural network that determines whether a point (x, y) lies inside
 * the circle with center (0, 0) and radius 5.
 * <p>
 * Input: {x, y}. Output: one value in (0, 1) - the probability that the point is inside.
 * {@link #classify(double, double)} turns it into the required answer: 1 - inside, 0 - outside.
 * <p>
 * Architecture: 2 inputs -> 16 tanh neurons -> 1 sigmoid neuron.
 */
@Slf4j
public class NeuronNetwork {

    static final double RADIUS = 5.0;

    /** Training points are sampled from the square [-DATA_RANGE, DATA_RANGE]^2. */
    private static final double DATA_RANGE = 10.0;
    /** Coordinates are divided by this value before entering the network, so they are roughly in [-1, 1]. */
    private static final double INPUT_SCALE = 10.0;

    private static final int HIDDEN_NEURONS = 16;
    private static final int TRAIN_SIZE = 1000;
    private static final int TEST_SIZE = 500;
    private static final int EPOCHS = 2000;
    private static final double LEARNING_RATE = 0.1;

    private final List<NeuronLayer> layers = new ArrayList<>();
    private final Random random = new Random(42);

    /**
     * Creates the network and trains it on generated data.
     */
    public NeuronNetwork() {
        layers.add(new NeuronLayer(2, HIDDEN_NEURONS, NeuronType.TANH));
        layers.add(new NeuronLayer(HIDDEN_NEURONS, 1, NeuronType.SIGMOID));
        for (NeuronLayer layer : layers) {
            initializeWeights(layer);
        }
        train();
    }

    /**
     * Xavier (Glorot) uniform initialisation: weights in [-limit, limit],
     * limit = sqrt(6 / (inputs + outputs)); biases start at 0.
     */
    private void initializeWeights(NeuronLayer layer) {
        for (Neuron neuron : layer.getNeurons()) {
            int inputCount = neuron.getWeights().length;
            double limit = Math.sqrt(6.0 / (inputCount + layer.size()));
            double[] weights = new double[inputCount];
            for (int i = 0; i < inputCount; i++) {
                weights[i] = (random.nextDouble() * 2 - 1) * limit;
            }
            neuron.setWeights(weights);
            neuron.setBias(0.0);
        }
    }

    /**
     * @param inputs {x, y}
     * @return array with one value - probability (0..1) that the point is inside the circle
     */
    public double[] predict(double[] inputs) {
        double[] output = normalize(inputs);
        for (NeuronLayer layer : layers) {
            output = layer.activate(output);
        }
        return output;
    }

    /**
     * @return 1 if the network thinks the point is inside the circle, otherwise 0
     */
    public int classify(double x, double y) {
        return predict(new double[]{x, y})[0] >= 0.5 ? 1 : 0;
    }

    /**
     * The exact rule used to label the generated data.
     *
     * @return 1 if x^2 + y^2 < 5^2, otherwise 0
     */
    public static int isInsideCircle(double x, double y) {
        return x * x + y * y < RADIUS * RADIUS ? 1 : 0;
    }

    /**
     * Generates training and test data, trains the network and logs the accuracy on the test data.
     */
    public void train() {
        DataSet trainData = generateData(TRAIN_SIZE);
        DataSet testData = generateData(TEST_SIZE);

        train(trainData.inputs, trainData.outputs, EPOCHS, LEARNING_RATE);

        log.info("Accuracy: train = {}%, test = {}%",
                String.format("%.2f", accuracy(trainData) * 100),
                String.format("%.2f", accuracy(testData) * 100));
    }

    /**
     * Generates labelled points uniformly from [-DATA_RANGE, DATA_RANGE]^2.
     * Half of the points are inside the circle and half outside, so the classes are balanced
     * (otherwise only ~20% of random points would be inside).
     *
     * @param size number of points
     * @return inputs {x, y} and expected outputs {1} (inside) or {0} (outside)
     */
    DataSet generateData(int size) {
        double[][] inputs = new double[size][];
        double[][] outputs = new double[size][];
        int insideNeeded = size / 2;
        int outsideNeeded = size - insideNeeded;
        int index = 0;
        while (index < size) {
            double x = (random.nextDouble() * 2 - 1) * DATA_RANGE;
            double y = (random.nextDouble() * 2 - 1) * DATA_RANGE;
            int label = isInsideCircle(x, y);
            if (label == 1 && insideNeeded > 0) {
                insideNeeded--;
            } else if (label == 0 && outsideNeeded > 0) {
                outsideNeeded--;
            } else {
                continue;
            }
            inputs[index] = new double[]{x, y};
            outputs[index] = new double[]{label};
            index++;
        }
        shuffle(inputs, outputs);
        return new DataSet(inputs, outputs);
    }

    /**
     * Share of points (0..1) that the network classifies correctly.
     */
    double accuracy(DataSet data) {
        int correct = 0;
        for (int i = 0; i < data.inputs.length; i++) {
            if (classify(data.inputs[i][0], data.inputs[i][1]) == (int) data.outputs[i][0]) {
                correct++;
            }
        }
        return (double) correct / data.inputs.length;
    }

    /**
     * Trains the neural network with backpropagation (stochastic gradient descent)
     * for the given number of epochs and learning rate.
     * Loss function: Mean Squared Error. The error is logged every 1000 epochs.
     *
     * @param trainingInputs  input data for training
     * @param trainingOutputs expected output data for training
     * @param epochs          number of training iterations
     * @param learningRate    step size for weight updates
     */
    private void train(double[][] trainingInputs,
                       double[][] trainingOutputs,
                       int epochs,
                       double learningRate) {
        int layerCount = layers.size();
        int[] order = new int[trainingInputs.length];
        for (int i = 0; i < order.length; i++) {
            order[i] = i;
        }

        for (int epoch = 1; epoch <= epochs; epoch++) {
            shuffle(order);
            double totalError = 0;

            for (int sample : order) {
                // ---- Forward pass: remember inputs and weighted sums of every layer ----
                double[][] layerInputs = new double[layerCount][];
                double[][] layerSums = new double[layerCount][];
                double[] signal = normalize(trainingInputs[sample]);
                for (int l = 0; l < layerCount; l++) {
                    Neuron[] neurons = layers.get(l).getNeurons();
                    layerInputs[l] = signal;
                    layerSums[l] = new double[neurons.length];
                    double[] out = new double[neurons.length];
                    for (int n = 0; n < neurons.length; n++) {
                        layerSums[l][n] = neurons[n].weightedSum(signal);
                        out[n] = neurons[n].activateSum(layerSums[l][n]);
                    }
                    signal = out;
                }
                double[] predicted = signal;

                // ---- Error (expected - predicted) and MSE ----
                double[] expected = trainingOutputs[sample];
                double[][] deltas = new double[layerCount][];
                int last = layerCount - 1;
                Neuron[] outputNeurons = layers.get(last).getNeurons();
                deltas[last] = new double[outputNeurons.length];
                for (int n = 0; n < outputNeurons.length; n++) {
                    double error = expected[n] - predicted[n];
                    totalError += error * error;
                    deltas[last][n] = error * outputNeurons[n].derivative(layerSums[last][n]);
                }

                // ---- Backward pass: propagate deltas to hidden layers ----
                for (int l = last - 1; l >= 0; l--) {
                    Neuron[] neurons = layers.get(l).getNeurons();
                    Neuron[] nextNeurons = layers.get(l + 1).getNeurons();
                    deltas[l] = new double[neurons.length];
                    for (int n = 0; n < neurons.length; n++) {
                        double error = 0;
                        for (int k = 0; k < nextNeurons.length; k++) {
                            error += deltas[l + 1][k] * nextNeurons[k].getWeights()[n];
                        }
                        deltas[l][n] = error * neurons[n].derivative(layerSums[l][n]);
                    }
                }

                // ---- Weight update: w += lr * delta * input, b += lr * delta ----
                for (int l = 0; l < layerCount; l++) {
                    Neuron[] neurons = layers.get(l).getNeurons();
                    for (int n = 0; n < neurons.length; n++) {
                        double[] weights = neurons[n].getWeights();
                        for (int w = 0; w < weights.length; w++) {
                            weights[w] += learningRate * deltas[l][n] * layerInputs[l][w];
                        }
                        neurons[n].setBias(neurons[n].getBias() + learningRate * deltas[l][n]);
                    }
                }
            }

            if (epoch % 1000 == 0 || epoch == 1) {
                log.info("Epoch {}: MSE = {}", epoch, totalError / trainingInputs.length);
            }
        }
    }

    private static double[] normalize(double[] inputs) {
        double[] scaled = new double[inputs.length];
        for (int i = 0; i < inputs.length; i++) {
            scaled[i] = inputs[i] / INPUT_SCALE;
        }
        return scaled;
    }

    private void shuffle(int[] array) {
        for (int i = array.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int tmp = array[i];
            array[i] = array[j];
            array[j] = tmp;
        }
    }

    private void shuffle(double[][] inputs, double[][] outputs) {
        for (int i = inputs.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            double[] tmpIn = inputs[i];
            inputs[i] = inputs[j];
            inputs[j] = tmpIn;
            double[] tmpOut = outputs[i];
            outputs[i] = outputs[j];
            outputs[j] = tmpOut;
        }
    }

    /** Training or test data: inputs[i] = {x, y}, outputs[i] = {expected value}. */
    static class DataSet {
        final double[][] inputs;
        final double[][] outputs;

        DataSet(double[][] inputs, double[][] outputs) {
            this.inputs = inputs;
            this.outputs = outputs;
        }
    }
}
