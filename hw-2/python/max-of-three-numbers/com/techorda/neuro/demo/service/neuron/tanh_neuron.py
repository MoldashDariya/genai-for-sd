import math

from neuron.neuron import Neuron


class TanhNeuron(Neuron):
    """Neuron with the hyperbolic tangent activation function. Output range: (-1, 1)."""

    def __init__(self, input_count: int) -> None:
        super().__init__(input_count)

    def activation_function(self, x: float) -> float:
        return math.tanh(x)

    def derivative(self, x: float) -> float:
        """Derivative of tanh at the weighted sum x: f'(x) = 1 - f(x)^2."""
        fx = math.tanh(x)
        return 1.0 - fx * fx
