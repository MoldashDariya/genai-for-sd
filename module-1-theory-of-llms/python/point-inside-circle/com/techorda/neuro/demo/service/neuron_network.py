import logging
import math
import random
from typing import List, Optional, Sequence, Tuple

from neuron_layer import NeuronLayer
from neuron.sigmoid_neuron import SigmoidNeuron
from neuron.tanh_neuron import TanhNeuron

logger = logging.getLogger(__name__)

RADIUS = 5.0
# Training points are sampled from the square [-DATA_RANGE, DATA_RANGE]^2.
DATA_RANGE = 10.0
# Coordinates are divided by this value before entering the network, so they are roughly in [-1, 1].
INPUT_SCALE = 10.0

HIDDEN_NEURONS = 12
TRAIN_SIZE = 400
TEST_SIZE = 400
EPOCHS = 300
LEARNING_RATE = 0.3
LOG_EVERY = 1000


def is_inside_circle(x: float, y: float) -> int:
    """The exact rule used to label the generated data: 1 if x^2 + y^2 < 5^2, otherwise 0."""
    return 1 if x * x + y * y < RADIUS * RADIUS else 0


class NeuronNetwork:
    """
    Neural network that determines whether a point (x, y) lies inside
    the circle with center (0, 0) and radius 5.

    Input: [x, y]. Output: [p] - probability (0..1) that the point is inside.
    classify(x, y) turns it into the required answer: 1 - inside, 0 - outside.

    Architecture: 2 inputs -> 12 tanh neurons -> 1 sigmoid neuron.
    """

    def __init__(self):
        self.layers: List[NeuronLayer] = []
        self.random = random.Random(42)

        self.layers.append(NeuronLayer([TanhNeuron(2) for _ in range(HIDDEN_NEURONS)]))
        self.layers.append(NeuronLayer([SigmoidNeuron(HIDDEN_NEURONS)]))
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
        """Returns [p] - the probability that the point [x, y] is inside the circle."""
        output = self._normalize(inputs)
        for layer in self.layers:
            output = layer.activate(output)
        return output

    def classify(self, x: float, y: float) -> int:
        """Returns 1 if the network thinks the point is inside the circle, otherwise 0."""
        return 1 if self.predict([x, y])[0] >= 0.5 else 0

    def generate_data(self, size: int) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Generates labelled points uniformly from [-DATA_RANGE, DATA_RANGE]^2.
        Half of the points are inside the circle and half outside, so the classes are balanced
        (otherwise only ~20% of random points would be inside).

        Returns (inputs, outputs): inputs[i] = [x, y], outputs[i] = [1.0] (inside) or [0.0] (outside).
        """
        inside_needed = size // 2
        outside_needed = size - inside_needed
        samples = []
        while len(samples) < size:
            x = self.random.uniform(-DATA_RANGE, DATA_RANGE)
            y = self.random.uniform(-DATA_RANGE, DATA_RANGE)
            label = is_inside_circle(x, y)
            if label == 1 and inside_needed > 0:
                inside_needed -= 1
            elif label == 0 and outside_needed > 0:
                outside_needed -= 1
            else:
                continue
            samples.append(([x, y], [float(label)]))
        self.random.shuffle(samples)
        return [s[0] for s in samples], [s[1] for s in samples]

    def accuracy(self, inputs: Sequence[Sequence[float]], outputs: Sequence[Sequence[float]]) -> float:
        """Share of points (0..1) that the network classifies correctly."""
        correct = sum(1 for p, o in zip(inputs, outputs) if self.classify(p[0], p[1]) == int(o[0]))
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
        and logs the accuracy on the test data.

        training_inputs - input data for training ([x, y] per sample)
        training_outputs - expected output data for training ([1.0] or [0.0] per sample)
        epochs - number of training iterations
        learning_rate - step size for weight updates
        """
        if training_inputs is None or training_outputs is None:
            self._backpropagation(self.training_inputs, self.training_outputs, epochs, learning_rate)
            logger.info("Accuracy: train = %.2f%%, test = %.2f%%",
                        self.accuracy(self.training_inputs, self.training_outputs) * 100,
                        self.accuracy(self.test_inputs, self.test_outputs) * 100)
        else:
            self._backpropagation(training_inputs, training_outputs, epochs, learning_rate)

    def _backpropagation(self, training_inputs, training_outputs, epochs, learning_rate) -> None:
        layer_count = len(self.layers)
        order = list(range(len(training_inputs)))

        for epoch in range(1, epochs + 1):
            self.random.shuffle(order)
            total_error = 0.0

            for sample in order:
                # ---- Forward pass: remember inputs and weighted sums of every layer ----
                layer_inputs = []
                layer_sums = []
                signal = self._normalize(training_inputs[sample])
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
                output_neurons = self.layers[last].neurons
                for n, neuron in enumerate(output_neurons):
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

    @staticmethod
    def _normalize(inputs: Sequence[float]) -> List[float]:
        return [value / INPUT_SCALE for value in inputs]
