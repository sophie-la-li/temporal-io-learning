
import asyncio
import time
import sys
import json
import os.path
import hashlib
import random
import re

from temporalio import activity
from sll_neural_network import NeuralNetwork as NN

from shared import NetworkConfig
from shared import NetworkResult
from shared import NetworkList

class NetworkActivities:
    networkStoragePath: string = "./networks"

    def __init__(self):
        pass

    def _getNetworkFilePath(self, config: NetworkConfig) -> str:
        hashedId: string = hashlib.md5(config.id.encode('utf-8')).hexdigest()
        filePath: string = f"{self.networkStoragePath}/{hashedId}.nn"
        return filePath

    @activity.defn
    async def getAll(self) -> NetworkList:
        list: NetworkList = NetworkList([])
        directory = os.fsencode(self.networkStoragePath)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".nn"):
                data = json.load(open(
                    self.networkStoragePath + "/" + filename
                ))
                list.networks.append(data["config"])
        return list

    @activity.defn
    async def delete(self, config: NetworkConfig) -> str:
        filePath: str = self._getNetworkFilePath(config)
        if os.path.isfile(filePath):
            os.remove(filePath)
        return "deleted"

    @activity.defn
    async def execute(self, config: NetworkConfig) -> NetworkResult:
        filePath: str = self._getNetworkFilePath(config)
        data: dict = {}

        if os.path.isfile(filePath):
            data = json.load(open(filePath, "r"))
        else:
            data["config"] = config.__dict__
            data["iterations"] = 0
            data["weights"] = {}

        network = NN.NeuralNetwork()
        network.inputSize = len(data["config"]["input"])
        network.outputSize = len(data["config"]["expected_output"])
        network.hiddenSize = data["config"]["hidden_neuron_layer_size"]
        network.hiddenNumber = data["config"]["hidden_neuron_layers"]
        network.weights = data["weights"]
        network.epsilon = config.epsilon

        for i in range(config.iterations_before_result):
            print("training network: " + str(i+1) + "/" + str(config.iterations_before_result), end='\r')

            input: list = []
            expected_output: list = []

            for j in range(network.inputSize):
                f = config.input[j]

                if f.isnumeric():
                    input.append(int(f))
                    continue

                if f.startswith("rand"):
                    p = f.rsplit(":")
                    f = random.randint(int(p[1]), int(p[2]))
                    input.append(int(f))
                    continue

            for k in range(network.outputSize):
                f = config.expected_output[k]

                for ii in range(len(input)):
                    f = f.replace("i" + str(ii), str(input[ii]))

                if f.isnumeric():
                    expected_output.append(int(f))
                    continue

                if re.search("^[0-9\\+\\-\\*\\/\\(\\)\\ ]*?$", f):
                    f = eval(f)
                    expected_output.append(f)
                    continue

            output: list = network.train(input, expected_output, network)
            data["iterations"] += 1

        result: NetworkResult = NetworkResult(
            iterations = data["iterations"],
            last_input = input,
            last_expected_output = expected_output,
            last_output = output
        )

        data["weights"] = network.weights
        json.dump(data, open(filePath, "w"), indent = "    ")
        return result
