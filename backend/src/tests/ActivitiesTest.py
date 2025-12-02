
import uuid
import pytest
import hashlib
import random

from temporalio.client import WorkflowFailureError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from sll_neural_network import NeuralNetwork

from activities import NetworkActivities
from shared import NetworkConfig
from shared import NetworkResult
from shared import NetworkList

@pytest.mark.asyncio
async def testGetAll(mocker) -> None:
    pathMock = mocker.patch("os.fsencode", return_value="dir")
    readMock = mocker.patch("os.listdir", return_value=["test.nn"])
    openMock = mocker.patch("builtins.open", return_value="file")
    decodeMock = mocker.patch("json.load", return_value={"config":{"a":1}})

    activities = NetworkActivities()
    allNetworks = await activities.getAll()
    assert type(allNetworks) is NetworkList
    assert len(allNetworks.networks) == 1
    assert type(allNetworks.networks[0] is dict)
    assert allNetworks.networks[0]["a"] == 1

    pathMock.assert_called_once_with(NetworkActivities.networkStoragePath)
    readMock.assert_called_once_with("dir")
    openMock.assert_called_once_with(f"{NetworkActivities.networkStoragePath}/test.nn")
    decodeMock.assert_called_once_with("file")

@pytest.mark.asyncio
async def testDelete(mocker) -> None:
    checkMock = mocker.patch("os.path.isfile", return_value=True)
    deleteMock = mocker.patch("os.remove", return_value="removed")

    activities = NetworkActivities()
    result = await activities.delete(NetworkConfig(
        id = "test",
        input = ["rand:0:10"],
        expected_output = ["i0"],
        hidden_neuron_layer_size = 1,
        hidden_neuron_layers = 1,
        iterations_before_result = 1,
        epsilon = 1
    ))
    assert result == "deleted"

    fileName: string = hashlib.md5("test".encode('utf-8')).hexdigest()
    filePath: string = f"{NetworkActivities.networkStoragePath}/{fileName}.nn"
    checkMock.assert_called_once_with(filePath)
    deleteMock.assert_called_once_with(filePath)

@pytest.mark.asyncio
async def testExecuteNew(mocker) -> None:
    checkMock = mocker.patch("os.path.isfile", return_value=False)
    openMock = mocker.patch("builtins.open", return_value="file")
    dumpMock = mocker.patch("random.randint", side_effect=[4,2])
    dumpMock = mocker.patch("json.dump", return_value="dumped")

    def trainMockFn(input, expected_output, self):
        assert self.inputSize == 2
        assert self.outputSize == 1
        assert self.hiddenSize == 3
        assert self.hiddenNumber == 2
        assert self.epsilon == 4
        return [42]

    trainMock = mocker.patch(
        "sll_neural_network.NeuralNetwork.NeuralNetwork.train",
        side_effect = trainMockFn
    )

    activities = NetworkActivities()
    result = await activities.execute(NetworkConfig(
        id = "test",
        input = ["rand:0:10", "rand:0:10"],
        expected_output = ["i0 + i1"],
        hidden_neuron_layer_size = 3,
        hidden_neuron_layers = 2,
        iterations_before_result = 1,
        epsilon = 4
    ))
    #assert result == "deleted"

    fileName: string = hashlib.md5("test".encode('utf-8')).hexdigest()
    filePath: string = f"{NetworkActivities.networkStoragePath}/{fileName}.nn"
    checkMock.assert_called_once_with(filePath)
    openMock.assert_called_once_with(filePath, "w")

    trainMock.assert_has_calls([
        mocker.call([4, 2], [6], mocker.ANY)
    ])

    dumpMock.assert_called_once_with(
        {
            "config": {
                "id": "test",
                "input": ["rand:0:10", "rand:0:10"],
                "expected_output": ["i0 + i1"],
                "hidden_neuron_layer_size": 3,
                "hidden_neuron_layers": 2,
                "iterations_before_result": 1,
                "epsilon": 4
            },
            "weights": {},
            "iterations": 1
        },
        "file",
         indent = "    "
    )

@pytest.mark.asyncio
async def testExecuteExisting(mocker) -> None:
    checkMock = mocker.patch("os.path.isfile", return_value=True)
    openMock = mocker.patch("builtins.open", return_value="file")
    dumpMock = mocker.patch("json.dump", return_value="dumped")
    decodeMock = mocker.patch("json.load", return_value={
        "config": {
            "id": "test",
            "input": ["rand:0:10"],
            "expected_output": ["i0"],
            "hidden_neuron_layer_size": 1,
            "hidden_neuron_layers": 2,
            "iterations_before_result": 3,
            "epsilon": 4
        },
        "weights": {
            "a": 1
        },
        "iterations": 100
    })

    def trainMockFn(input, expected_output, self):
        assert self.inputSize == 1
        assert self.outputSize == 1
        assert self.hiddenSize == 1
        assert self.hiddenNumber == 2
        assert self.weights == { "a": 1 }
        assert self.epsilon == 11
        return [42]

    trainMock = mocker.patch(
        "sll_neural_network.NeuralNetwork.NeuralNetwork.train",
        side_effect = trainMockFn
    )

    activities = NetworkActivities()
    result = await activities.execute(NetworkConfig(
        id = "test",
        input = ["123", "456"],
        expected_output = ["456", "789"],
        hidden_neuron_layer_size = 0,
        hidden_neuron_layers = 0,
        iterations_before_result = 2,
        epsilon = 11
    ))
    #assert result == "deleted"

    fileName: string = hashlib.md5("test".encode('utf-8')).hexdigest()
    filePath: string = f"{NetworkActivities.networkStoragePath}/{fileName}.nn"
    decodeMock.assert_called_once_with("file")
    checkMock.assert_called_once_with(filePath)

    openMock.assert_has_calls([
        mocker.call(filePath, "r"),
        mocker.call(filePath, "w")
    ])

    trainMock.assert_has_calls([
        mocker.call([123], [456], mocker.ANY),
        mocker.call([123], [456], mocker.ANY)
    ])

    dumpMock.assert_called_once_with(
        {
            "config": {
                "id": "test",
                "input": ["rand:0:10"],
                "expected_output": ["i0"],
                "hidden_neuron_layer_size": 1,
                "hidden_neuron_layers": 2,
                "iterations_before_result": 3,
                "epsilon": 4
            },
            "weights": {
                "a": 1
            },
            "iterations": 102
        },
        "file",
         indent = "    "
    )
