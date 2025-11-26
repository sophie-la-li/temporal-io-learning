
import random
import math
from copy import copy, deepcopy

class NeuralNetwork:
    ACTIVATION_FN_IDENDITY: int = 0
    ACTIVATION_FN_SIGMOID: int = 1

    inputSize: int = 1
    hiddenSize: int = 1
    hiddenNumber: int = 1
    outputSize: int = 1
    epsilon: float = 0.01
    weights: dict = {}
    valueCache: list = []
    hiddenActivationFunction: int = ACTIVATION_FN_SIGMOID
    outputActivationFunction: int = ACTIVATION_FN_IDENDITY

    def _isLastLayer(self, layer: int) -> bool:
        return self.hiddenNumber + 1 == layer

    def _getActivationFunction(self, layer: int) -> int:
        fn: int = self.hiddenActivationFunction
        if self._isLastLayer(layer): fn = self.outputActivationFunction
        return fn

    def _activate(self, layer: int, value: float) -> float:
        match self._getActivationFunction(layer):
            case self.ACTIVATION_FN_SIGMOID:
                return 1.0 / (1.0 + pow(math.exp(1.0), -value))
            case _:
                return value

    def _derivative(self, layer: int, value: float) -> float:
        match self._getActivationFunction(layer):
            case self.ACTIVATION_FN_SIGMOID:
                value = self._activate(layer, value)
                return value * (1 - value)
            case _:
                return 1

    def _getWeights(self, layer: int, neuron: int, weightCount: int) -> list:
        key: str = str(layer) + "-" + str(neuron)
        if key not in self.weights:
            self.weights[key] = []
            for i in range(weightCount):
                self.weights[key].append(random.random())
        return self.weights[key]

    def _getEmptyDeltaList(self) -> None:
        deltas: list = deepcopy(self.valueCache) # just for the structure; bit ugly
        for i in range(len(deltas)):
            for j in range(len(deltas[i])):
                deltas[i][j] = 0
        return deltas

    def train(self, input: list, expectedOutput: list) -> list:
        output = self.execute(input)
        smallDeltas: list = self._getEmptyDeltaList()

        for layer in reversed(range(self.hiddenNumber + 2)):
            if layer == 0: continue # skip input layer
            isOutput: bool = self._isLastLayer(layer)

            size: int = self.hiddenSize
            if isOutput: size = self.outputSize

            for neuron in range(size):
                value: float = self.valueCache[layer][neuron]
                weights = self._getWeights(layer, neuron, 0)

                if isOutput:
                    smallDeltas[layer][neuron] = expectedOutput[neuron] - value
                smallDelta: float = smallDeltas[layer][neuron]

                bigDeltaFactor: float = self._derivative(layer, value)

                for prevLayerNeuron in range(len(weights)):
                    pWeight: float = weights[prevLayerNeuron]
                    pValue: float = self.valueCache[layer-1][prevLayerNeuron]

                    # prepare small delta for previous layer
                    smallDeltas[layer-1][prevLayerNeuron] += smallDelta * pWeight

                    bigDelta: float = self.epsilon * bigDeltaFactor * smallDelta * pValue
                    weights[prevLayerNeuron] += bigDelta

        return output

    def execute(self, input: list) -> list:
        if len(input) != self.inputSize:
            raise Exception('input size (' + str(len(input))
                + ') has to match setting (' + str(self.inputSize) + ')')

        values: list = [input]

        for layer in range(self.hiddenNumber + 2):
            if layer == 0: continue # skip input layer
            isOutput: bool = self._isLastLayer(layer)
            size: int = self.hiddenSize
            if isOutput: size = self.outputSize
            values.append([])

            for neuron in range(size):
                prevLayerValues: list = values[layer-1]
                weights: list = self._getWeights(layer, neuron, len(prevLayerValues))
                sum: float = 0
                for i in range(len(prevLayerValues)):
                    sum += prevLayerValues[i] * weights[i]
                value: float = self._activate(layer, sum)
                value = round(value, 5) # tbc
                values[layer].append(value)

        self.valueCache = values
        return values[-1]

