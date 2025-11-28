
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import NetworkActivities
    from shared import NetworkConfig
    from shared import NetworkResult
    from shared import NetworkList

@workflow.defn
class GetAllNetworks:
    @workflow.run
    async def run(self) -> NetworkList:
        retry_policy = RetryPolicy(
            maximum_attempts = 1,
            maximum_interval = timedelta(seconds=2),
            non_retryable_error_types = []
        )

        return await workflow.execute_activity_method(
            NetworkActivities.getAll,
            start_to_close_timeout = timedelta(seconds=5),
            retry_policy = retry_policy
        )

@workflow.defn
class DeleteNetwork:
    @workflow.run
    async def run(self, data: NetworkConfig) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts = 1,
            maximum_interval = timedelta(seconds=2),
            non_retryable_error_types = ["InvalidNetworkId"]
        )

        return await workflow.execute_activity_method(
            NetworkActivities.delete,
            data,
            start_to_close_timeout = timedelta(seconds=5),
            retry_policy = retry_policy
        )

@workflow.defn
class ExecuteNetwork:
    @workflow.run
    async def run(self, data: NetworkConfig) -> str:
        retry_policy = RetryPolicy(
            maximum_attempts = 1,
            maximum_interval = timedelta(seconds=2),
            non_retryable_error_types = ["InvalidNetworkId"]
        )

        return await workflow.execute_activity_method(
            NetworkActivities.execute,
            data,
            start_to_close_timeout = timedelta(seconds=60),
            retry_policy = retry_policy
        )
