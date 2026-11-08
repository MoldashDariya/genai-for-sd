package com.techorda.neuro.demo.service;

import com.techorda.neuro.demo.service.neuron.Neuron;
import com.techorda.neuro.demo.service.neuron.NeuronType;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Neural network that finds the maximum of three numbers in the range [-1, 1].
 * <p>
 * Input: {x1, x2, x3}. Output: one value - the approximation of max(x1, x2, x3).
 * <p>
 * Architecture: 3 inputs -> 32 ReLU neurons -> 1 tanh neuron.
 * <ul>
 *   <li>ReLU in the hidden layer: max is a piecewise linear function and ReLU networks represent
 *       such functions well (max(a, b) = b + relu(a - b)).</li>
 *   <li>tanh in the output layer: its range (-1, 1) matches the range of the answer, so the network
 *       never predicts values outside [-1, 1].</li>
 * </ul>
 */
@Slf4j
public class NeuronNetwork {

    private static final int INPUTS = 3;
    private static final int HIDDEN_NEURONS = 32;
    private static final int TRAIN_SIZE = 1000;
    private static final int TEST_SIZE = 500;
    private static final int EPOCHS = 2000;
    private static final double LEARNING_RATE = 0.05;
    /** A prediction is considered correct if it differs from the real maximum by less than this value. */
    private static final double TOLERANCE = 0.05;

    private final List<NeuronLayer> layers = new ArrayList<>();
    private final Random random = new Random(42);
    /** How many times {@link #train()} has been called; every next call fine-tunes with a smaller step. */
    private int trainingRound = 0;

    /**
     * Creates the network and trains it on generated data.
     */
    public NeuronNetwork() {
        layers.add(new NeuronLayer(INPUTS, HIDDEN_NEURONS, NeuronType.RELU));
        layers.add(new NeuronLayer(HIDDEN_NEURONS, 1, NeuronType.TANH));
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
     * @param inputs {x1, x2, x3}, each in [-1, 1]
     * @return array with one value - predicted max(x1, x2, x3)
     */
    public double[] predict(double[] inputs) {
        double[] output = inputs;
        for (NeuronLayer layer : layers) {
            output = layer.activate(output);
        }
        return output;
    }

    /**
     * Convenience method: predicted maximum of three numbers.
     */
    public double max(double x1, double x2, double x3) {
        return predict(new double[]{x1, x2, x3})[0];
    }

    /**
     * Generates training and test data, trains the network and logs the quality on the test data.
     * The first call trains from scratch; every next call continues training (fine-tuning)
     * with a two times smaller learning rate than the previous one.
     */
    public void train() {
        DataSet trainData = generateData(TRAIN_SIZE);
        DataSet testData = generateData(TEST_SIZE);

        double learningRate = LEARNING_RATE / Math.pow(2, trainingRound);
        trainingRound++;
        train(trainData.inputs, trainData.outputs, EPOCHS, learningRate);

        log.info("Test data: MSE = {}, mean absolute error = {}, within +-{}: {}%",
                String.format("%.6f", meanSquaredError(testData)),
                String.format("%.4f", meanAbsoluteError(testData)),
                TOLERANCE,
                String.format("%.2f", accuracy(testData) * 100));
    }

    /**
     * Generates random triples from [-1, 1]^3 with the expected output max(x1, x2, x3).
     * <p>
     * Three kinds of samples are mixed (one third each):
     * 1) all three numbers uniform in [-1, 1];
     * 2) the maximum m uniform in [-1, 1] and the other two in [-1, m] - with plain uniform sampling
     *    the maximum would be negative only in 1/8 of cases, so that region would be barely learned;
     * 3) the same, but the other two numbers are close to m (within 0.2) - the hardest region,
     *    where max has its "kinks".
     * The 8 corners of the cube are always included, so the edge values -1 and 1 are covered too.
     *
     * @param size number of samples
     * @return inputs {x1, x2, x3} and expected outputs {max}
     */
    DataSet generateData(int size) {
        double[][] inputs = new double[size][];
        double[][] outputs = new double[size][];
        int index = 0;
        for (int corner = 0; corner < 8 && index < size; corner++, index++) {
            inputs[index] = new double[]{
                    (corner & 1) == 0 ? -1.0 : 1.0,
                    (corner & 2) == 0 ? -1.0 : 1.0,
                    (corner & 4) == 0 ? -1.0 : 1.0};
        }
        for (; index < size; index++) {
            switch (index % 3) {
                case 0:
                    inputs[index] = uniformTriple();
                    break;
                case 1:
                    inputs[index] = tripleWithUniformMax(2.0);
                    break;
                default:
                    inputs[index] = tripleWithUniformMax(0.2);
                    break;
            }
        }
        for (int i = 0; i < size; i++) {
            outputs[i] = new double[]{Math.max(inputs[i][0], Math.max(inputs[i][1], inputs[i][2]))};
        }
        return new DataSet(inputs, outputs);
    }

    private double[] uniformTriple() {
        return new double[]{uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)};
    }

    /**
     * @param spread how far below the maximum the other two numbers may be
     *               (2.0 - anywhere in [-1, max], 0.2 - close to the maximum)
     */
    private double[] tripleWithUniformMax(double spread) {
        double max = uniform(-1, 1);
        double low = Math.max(-1.0, max - spread);
        double[] triple = {max, uniform(low, max), uniform(low, max)};
        int position = random.nextInt(3);
        double tmp = triple[position];
        triple[position] = triple[0];
        triple[0] = tmp;
        return triple;
    }

    private double uniform(double from, double to) {
        return from + random.nextDouble() * (to - from);
    }

    double meanSquaredError(DataSet data) {
        double sum = 0;
        for (int i = 0; i < data.inputs.length; i++) {
            double error = data.outputs[i][0] - predict(data.inputs[i])[0];
            sum += error * error;
        }
        return sum / data.inputs.length;
    }

    double meanAbsoluteError(DataSet data) {
        double sum = 0;
        for (int i = 0; i < data.inputs.length; i++) {
            sum += Math.abs(data.outputs[i][0] - predict(data.inputs[i])[0]);
        }
        return sum / data.inputs.length;
    }

    /**
     * Share of samples (0..1) where the prediction differs from the real maximum by less than {@link #TOLERANCE}.
     */
    double accuracy(DataSet data) {
        int correct = 0;
        for (int i = 0; i < data.inputs.length; i++) {
            if (Math.abs(data.outputs[i][0] - predict(data.inputs[i])[0]) < TOLERANCE) {
                correct++;
            }
        }
        return (double) correct / data.inputs.length;
    }

    /**
     * Trains the neural network with backpropagation (stochastic gradient descent)
     * for the given number of epochs and learning rate.
     * Loss function: Mean Squared Error. The error is logged every 1000 epochs.
     * The step size decays linearly from {@code initialLearningRate} to {@code initialLearningRate / 10}
     * during training, so the network settles in a minimum instead of jumping around it.
     *
     * @param trainingInputs  input data for training
     * @param trainingOutputs expected output data for training
     * @param epochs          number of training iterations
     * @param initialLearningRate step size for weight updates at the first epoch
     */
    private void train(double[][] trainingInputs,
                       double[][] trainingOutputs,
                       int epochs,
                       double initialLearningRate) {
        int layerCount = layers.size();
        int[] order = new int[trainingInputs.length];
        for (int i = 0; i < order.length; i++) {
            order[i] = i;
        }

        for (int epoch = 1; epoch <= epochs; epoch++) {
            double progress = (double) (epoch - 1) / epochs;
            double learningRate = initialLearningRate * (1.0 - 0.9 * progress);
            shuffle(order);
            double totalError = 0;

            for (int sample : order) {
                // ---- Forward pass: remember inputs and weighted sums of every layer ----
                double[][] layerInputs = new double[layerCount][];
                double[][] layerSums = new double[layerCount][];
                double[] signal = trainingInputs[sample];
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

    private void shuffle(int[] array) {
        for (int i = array.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int tmp = array[i];
            array[i] = array[j];
            array[j] = tmp;
        }
    }

    /** Training or test data: inputs[i] = {x1, x2, x3}, outputs[i] = {max(x1, x2, x3)}. */
    static class DataSet {
        final double[][] inputs;
        final double[][] outputs;

        DataSet(double[][] inputs, double[][] outputs) {
            this.inputs = inputs;
            this.outputs = outputs;
        }
    }
}
