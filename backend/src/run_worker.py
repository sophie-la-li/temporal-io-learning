
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import NetworkActivities
from workflows import DeleteNetwork
from workflows import ExecuteNetwork
from workflows import GetAllNetworks

async def main() -> None:
    client: Client = await Client.connect("temporal-server:7233", namespace="default")
    activities = NetworkActivities()

    worker: Worker = Worker(
        client,
        task_queue = "NETWORK_RUNNER_QUEUE",
        workflows = [DeleteNetwork, GetAllNetworks, ExecuteNetwork],
        activities = [activities.delete, activities.getAll, activities.execute],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
