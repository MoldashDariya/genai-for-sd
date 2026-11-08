import logging
import math
import random
from typing import List, Optional, Sequence, Tuple

from neuron_layer import NeuronLayer
from neuron.relu_neuron import ReluNeuron
from neuron.tanh_neuron import TanhNeuron

logger = logging.getLogger(__name__)

INPUTS = 3
HIDDEN_NEURONS = 24
TRAIN_SIZE = 400
TEST_SIZE = 400
EPOCHS = 300
LEARNING_RATE = 0.1
# The step size decays linearly from LEARNING_RATE to LEARNING_RATE * FINAL_LR_FACTOR during training.
FINAL_LR_FACTOR = 0.1
# A prediction is considered correct if it differs from the real maximum by less than this value.
TOLERANCE = 0.05
LOG_EVERY = 1000


class NeuronNetwork:
    """
    Neural network that finds the maximum of three numbers in the range [-1, 1].

    Input: [x1, x2, x3]. Output: [m] - the approximation of max(x1, x2, x3).

    Architecture: 3 inputs -> 24 ReLU neurons -> 1 tanh neuron.
    - ReLU in the hidden layer: max is a piecewise linear function and ReLU networks
      represent such functions well (max(a, b) = b + relu(a - b)).
    - tanh in the output layer: its range (-1, 1) matches the range of the answer,
      so the network never predicts values outside [-1, 1].
    """

    def __init__(self):
        self.layers: List[NeuronLayer] = []
        self.random = random.Random(42)

        self.layers.append(NeuronLayer([ReluNeuron(INPUTS) for _ in range(HIDDEN_NEURONS)]))
        self.layers.append(NeuronLayer([TanhNeuron(HIDDEN_NEURONS)]))
        for layer in self.layers:
            self.initialize_weights(layer)

        # Training and test data are generated once; every call of train() continues
        # training on the same training data, so repeated calls keep improving the model.
        self.training_inputs, self.training_outputs = self.generate_data(TRAIN_SIZE)
        self.test_inputs, self.test_outputs = self.generate_data(TEST_SIZE)

        # The network trains during initialization.
        self.train()

    def initialize_weights(self, layer: NeuronLayer) -> None:
        """
        Xavier (Glorot) uniform initialisation: weights in [-limit, limit],
        limit = sqrt(6 / (inputs + outputs)); biases start at 0.
        """
        for neuron in layer.neurons:
            input_count = len(neuron.weights)
            limit = math.sqrt(6.0 / (input_count + layer.size()))
            neuron.weights = [self.random.uniform(-limit, limit) for _ in range(input_count)]
            neuron.bias = 0.0

    def predict(self, inputs: List[float]) -> List[float]:
        """Returns [m] - the predicted max(x1, x2, x3) for inputs [x1, x2, x3]."""
        output = list(inputs)
        for layer in self.layers:
            output = layer.activate(output)
        return output

    def max(self, x1: float, x2: float, x3: float) -> float:
        """Convenience method: predicted maximum of three numbers."""
        return self.predict([x1, x2, x3])[0]

    def generate_data(self, size: int) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Generates random triples from [-1, 1]^3 with the expected output max(x1, x2, x3).

        Three kinds of samples are mixed (one third each):
        1) all three numbers uniform in [-1, 1];
        2) the maximum m uniform in [-1, 1] and the other two in [-1, m] - with plain uniform
           sampling the maximum would be negative only in 1/8 of cases, so that region would
           be barely learned;
        3) the same, but the other two numbers are close to m (within 0.2) - the hardest
           region, where max has its "kinks".
        The 8 corners of the cube are always included, so the edge values -1 and 1 are covered too.

        Returns (inputs, outputs): inputs[i] = [x1, x2, x3], outputs[i] = [max(x1, x2, x3)].
        """
        inputs: List[List[float]] = []
        for corner in range(min(8, size)):
            inputs.append([1.0 if corner & bit else -1.0 for bit in (1, 2, 4)])
        while len(inputs) < size:
            kind = len(inputs) % 3
            if kind == 0:
                inputs.append([self.random.uniform(-1, 1) for _ in range(INPUTS)])
            elif kind == 1:
                inputs.append(self._triple_with_uniform_max(2.0))
            else:
                inputs.append(self._triple_with_uniform_max(0.2))
        outputs = [[max(triple)] for triple in inputs]
        return inputs, outputs

    def _triple_with_uniform_max(self, spread: float) -> List[float]:
        """spread - how far below the maximum the other two numbers may be."""
        maximum = self.random.uniform(-1, 1)
        low = max(-1.0, maximum - spread)
        triple = [maximum, self.random.uniform(low, maximum), self.random.uniform(low, maximum)]
        self.random.shuffle(triple)
        return triple

    def mean_absolute_error(self, inputs: Sequence[Sequence[float]],
                            outputs: Sequence[Sequence[float]]) -> float:
        return sum(abs(o[0] - self.predict(list(p))[0]) for p, o in zip(inputs, outputs)) / len(inputs)

    def accuracy(self, inputs: Sequence[Sequence[float]], outputs: Sequence[Sequence[float]]) -> float:
        """Share of samples (0..1) where the prediction differs from the real maximum by less than TOLERANCE."""
        correct = sum(1 for p, o in zip(inputs, outputs) if abs(o[0] - self.predict(list(p))[0]) < TOLERANCE)
        return correct / len(inputs)

    def train(self,
              training_inputs: Optional[List[List[float]]] = None,
              training_outputs: Optional[List[List[float]]] = None,
              epochs: int = EPOCHS,
              learning_rate: float = LEARNING_RATE) -> None:
        """
        Trains the neural network using backpropagation (stochastic gradient descent)
        for the given number of epochs and learning rate.
        Loss function: Mean Squared Error. The error is logged every 1000 epochs
        (and on the first and the last epoch).

        Python has no method overloading, so the two template methods train() and
        train(inputs, outputs, epochs, learning_rate) are combined into one:
        called without data, it trains on the training data generated in the constructor
        and logs the quality on the test data.

        training_inputs - input data for training ([x1, x2, x3] per sample)
        training_outputs - expected output data for training ([max] per sample)
        epochs - number of training iterations
        learning_rate - step size for weight updates at the first epoch
        """
        if training_inputs is None or training_outputs is None:
            self._backpropagation(self.training_inputs, self.training_outputs, epochs, learning_rate)
            logger.info("Test data: mean absolute error = %.4f, within +-%s: %.2f%%",
                        self.mean_absolute_error(self.test_inputs, self.test_outputs),
                        TOLERANCE,
                        self.accuracy(self.test_inputs, self.test_outputs) * 100)
        else:
            self._backpropagation(training_inputs, training_outputs, epochs, learning_rate)

    def _backpropagation(self, training_inputs, training_outputs, epochs, initial_learning_rate) -> None:
        layer_count = len(self.layers)
        order = list(range(len(training_inputs)))

        for epoch in range(1, epochs + 1):
            progress = (epoch - 1) / epochs
            learning_rate = initial_learning_rate * (1.0 - (1.0 - FINAL_LR_FACTOR) * progress)
            self.random.shuffle(order)
            total_error = 0.0

            for sample in order:
                # ---- Forward pass: remember inputs and weighted sums of every layer ----
                layer_inputs = []
                layer_sums = []
                signal = list(training_inputs[sample])
                for layer in self.layers:
                    layer_inputs.append(signal)
                    sums = [neuron.weighted_sum(signal) for neuron in layer.neurons]
                    layer_sums.append(sums)
                    signal = [neuron.activation_function(s) for neuron, s in zip(layer.neurons, sums)]
                predicted = signal

                # ---- Error (expected - predicted) and MSE ----
                expected = training_outputs[sample]
                deltas: List[List[float]] = [[] for _ in range(layer_count)]
                last = layer_count - 1
                for n, neuron in enumerate(self.layers[last].neurons):
                    error = expected[n] - predicted[n]
                    total_error += error * error
                    deltas[last].append(error * neuron.derivative(layer_sums[last][n]))

                # ---- Backward pass: propagate deltas to hidden layers ----
                for l in range(last - 1, -1, -1):
                    next_neurons = self.layers[l + 1].neurons
                    for n, neuron in enumerate(self.layers[l].neurons):
                        error = sum(deltas[l + 1][k] * next_neurons[k].weights[n]
                                    for k in range(len(next_neurons)))
                        deltas[l].append(error * neuron.derivative(layer_sums[l][n]))

                # ---- Weight update: w += lr * delta * input, b += lr * delta ----
                for l, layer in enumerate(self.layers):
                    inputs = layer_inputs[l]
                    for n, neuron in enumerate(layer.neurons):
                        step = learning_rate * deltas[l][n]
                        neuron.weights = [w + step * x for w, x in zip(neuron.weights, inputs)]
                        neuron.bias += step

            if epoch % LOG_EVERY == 0 or epoch == 1 or epoch == epochs:
                logger.info("Epoch %d: MSE = %.6f", epoch, total_error / len(training_inputs))
