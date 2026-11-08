# python
from abc import ABC, abstractmethod
from typing import List, Sequence
import random

class Neuron(ABC):
    def __init__(self, input_count: int) -> None:
        if input_count < 1:
            raise ValueError("input_count must be >= 1")
        self.weights: List[float] = [random.random() - 0.5 for _ in range(input_count)]
        self.bias: float = random.random() - 0.5

    def activate(self, inputs: Sequence[float]) -> float:
        return self.activation_function(self.weighted_sum(inputs))

    def weighted_sum(self, inputs: Sequence[float]) -> float:
        """Bias plus the weighted sum of inputs (the value before the activation function)."""
        if len(inputs) != len(self.weights):
            raise ValueError("Input length does not match weights length.")
        return self.bias + sum(i * w for i, w in zip(inputs, self.weights))

    @abstractmethod
    def activation_function(self, x: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def derivative(self, x: float) -> float:
        raise NotImplementedError
