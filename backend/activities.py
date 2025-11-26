
import asyncio
import time

from temporalio import activity

from shared import NetworkConfig
from shared import NetworkResult
from shared import NetworkList

class NetworkActivities:
    def __init__(self):
        pass

    @activity.defn
    async def getAll(self) -> NetworkList:
        c: NetworkConfig = NetworkConfig(
            "test",
            ["1", "b"],
            ["3 + 5"],
            2,
            3,
            4
        )

        list: NetworkList = NetworkList([c])
        return list

    @activity.defn
    async def delete(self, data: NetworkConfig) -> str:
        time.sleep(1)
        print(f"delete {data}")
        return "test"

    @activity.defn
    async def execute(self, data: NetworkConfig) -> NetworkResult:
        time.sleep(1)
        print(f"execute {data}")

        result: NetworkResult = NetworkResult(
            iterations = 123,
            last_input = [1,2],
            last_output = [3]
        )

        return result
