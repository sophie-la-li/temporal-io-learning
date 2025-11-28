
import { getTemporalClient } from '../../../temporal/src/client';

export async function POST(req: Request) {
    interface RequestBody {
        networkConfig: string;
        transactionId: string;
    }

    let body: RequestBody;
    let networkConfigJson: object;

    try {
        body = await req.json() as RequestBody;
    } catch (error) {
        return new Response("Invalid JSON body", { status: 400 });
    }

    const { networkConfig, transactionId } = body;

    try {
        networkConfigJson = JSON.parse(networkConfig)
    } catch (error) {
        return new Response("Invalid NetworkConfig JSON", { status: 400 });
    }

    const handle = await getTemporalClient().workflow.start("DeleteNetwork", {
        taskQueue: "NETWORK_RUNNER_QUEUE",
        workflowId: transactionId,
        args: [networkConfigJson]
    });

    return Response.json(await handle.result());
}
