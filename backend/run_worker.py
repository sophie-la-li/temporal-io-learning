# @@@SNIPSTART python-money-transfer-project-template-run-worker
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import BankingActivities
from shared import MONEY_TRANSFER_TASK_QUEUE_NAME
from workflows import oneClickBuy


async def main() -> None:
    client: Client = await Client.connect("temporal-server:7233", namespace="default")
    # Run the worker
    activities = BankingActivities()
    worker: Worker = Worker(
        client,
        task_queue="ecommerce-oneclick",
        workflows=[oneClickBuy],
        activities=[activities.purchase],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND
