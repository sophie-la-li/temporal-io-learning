
import { getTemporalClient } from '../../../temporal/src/client';

export async function POST(req: Request) {
    interface RequestBody {
        transactionId: string;
    }

    let body: RequestBody;

    try {
        body = await req.json() as RequestBody;
    } catch (error) {
        return new Response("Invalid JSON body", { status: 400 });
    }

    const { transactionId } = body;

    const handle = await getTemporalClient().workflow.start("GetAllNetworks", {
        taskQueue: "NETWORK_RUNNER_QUEUE",
        workflowId: transactionId,
        args: []
    });

    return Response.json(await handle.result());
}
