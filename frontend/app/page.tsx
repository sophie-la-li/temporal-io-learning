
'use client'

import Head from 'next/head';
import React, { useState, useRef, useEffect } from 'react'
import { v4 as uuid4 } from 'uuid'
import { testJson } from './shared';

const NN_BUTTON_STYLE = "bg-blue-300 hover:bg-blue-500 p-2 rounded-md m-1"

const NN_TRAINING_CONFIG_TPL = {
    id: "multiplying-network",
    input: [
        "rand:0:10",
        "rand:0:10"
    ],
    expected_output: [
        "i0 * i1"
    ],
    hidden_neuron_layer_size: 10,
    hidden_neuron_layers: 1,
    iterations_before_result: 1000,
    epsilon: 0.01
}

const NN_TRAINING_OUTPUT_TPL = {
    iterations: 0,
    last_input: [0],
    last_expected_output: [0],
    last_output: [0]
}

type NN_TRAINING_STATE = 'PAUSED' | 'TRAINING' | 'DELETED' | 'ERROR';

const LoadingSpinner: React.FC = () => {
    return (
        <div
            className="inline-block align-middle">
            <svg className="w-8 h-8 animate-spin text-gray-900/50" viewBox="0 0 64 64" fill="none"
                 xmlns="http://www.w3.org/2000/svg" width="24" height="24">
                <path
                    d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
                    stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"></path>
                <path
                    d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
                    stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"
                    className="text-gray-900">
                </path>
            </svg>
        </div>
    );
};

const NnTraining: React.FC = () => {
    const [state, setState] = useState<NN_TRAINING_STATE>('PAUSED');
    const [transactionId, setTransactionId] = useState(uuid4());
    const [networkConfig, setNetworkConfig] = useState(JSON.stringify(NN_TRAINING_CONFIG_TPL, null, 4));
    const [outputData, setOutputData] = useState(NN_TRAINING_OUTPUT_TPL);
    const [existingNetworks, setExistingNetworks] = useState([]);
    const stateRef = useRef(state);
    stateRef.current = state;

    const updateNetworkList = () => {
        fetch('/api/getAllNetworks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transactionId }),
        }).then((response) => {
            response.json().then((data) => {
                setExistingNetworks(data.networks)
            });
        }).catch(() => {
            setState('ERROR');
        });
    };

    useEffect(() => {
        updateNetworkList();
    }, [])

    const changeNetworkConfig = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        setNetworkConfig(event.target.value)
    };

    const loadNetwork = (
        event: React.MouseEvent<HTMLInputElement | HTMLButtonElement>
    ) => {
        setNetworkConfig(event.target.getAttribute("network"));
        setState('PAUSED');
    };

    const deleteNetwork = () => {
        if (!testJson(networkConfig)) {
            setState('ERROR');
            return;
        }

        fetch('/api/deleteNetwork', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ networkConfig, transactionId }),
        }).then((response) => {
            response.json().then((data) => {
                setState('DELETED');
                updateNetworkList();
            });
        }).catch(() => {
            setState('ERROR');
        });
    };

    const executeNetwork = () => {
        let firstStart = stateRef.current != "TRAINING"
        setState('TRAINING');

        if (!testJson(networkConfig)) {
            setState('ERROR');
            return;
        }

        fetch('/api/executeNetwork', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ networkConfig, transactionId }),
        }).then((response) => {
            response.json().then((data) => {
                setOutputData(data);

                if (firstStart) {
                    updateNetworkList();
                }

                setTimeout(() => {
                    if (stateRef.current == "TRAINING") {
                        executeNetwork();
                    }
                }, 1000);
            });
        }).catch(() => {
            setState('ERROR');
        });
    };

    const stopNetwork = () => {
        setState('PAUSED');
    };

    return (
        <div>
            <div className="bg-white m-2 p-5">
                <h3 className="font font-extrabold text-gray-900 sm:text-2xl mb-5">Existing Networks</h3>
                <list>
                    {existingNetworks.map((eNetworkConfig) => (
                        <li className="ml-10">
                            {eNetworkConfig.id}
                            <button onClick={loadNetwork} network={JSON.stringify(eNetworkConfig, null, 4)} className={NN_BUTTON_STYLE}>load</button>
                        </li>
                    ))}
                </list>
            </div>
            <div className="bg-white m-2 p-5">
                <h3 className="font font-extrabold text-gray-900 sm:text-2xl mb-5">Config</h3>
                <p className="m-5 ml-0">
                    Note: For existing networks, the length of the input and expected_output array will no longer
                    be updated. Same for the hidden_neuron_layer_size and hidden_neuron_layers options.
                    You still can change the input and expected_output values and iterations_before_result and epsilon options.
                    If you wan't to change more, you will need to delete the network and recreate it.
                </p>
                <textarea
                    className="border"
                    value={networkConfig}
                    rows="15"
                    cols="100"
                    onChange={(event) => changeNetworkConfig(event)}
                ></textarea><br/>
                <button onClick={deleteNetwork} className={NN_BUTTON_STYLE}>delete network</button>
                <button onClick={executeNetwork} className={NN_BUTTON_STYLE}>run training</button>
                <button onClick={stopNetwork} className={NN_BUTTON_STYLE}>stop training</button>
                {
                    {
                        PAUSED:   ( <span /> ),
                        DELETED: ( <span>Deleted!</span> ),
                        TRAINING: ( <span><LoadingSpinner/> Training ...</span> ),
                        ERROR:    ( <span>ERROR!</span> ),
                    }[state]
                }
            </div>
            <div className="bg-white m-2 p-5">
                <h3 className="font font-extrabold text-gray-900 sm:text-2xl mb-5">Output</h3>
                <table className="table-fixed">
                    <tbody>
                    <tr>
                        <td className="w-50">Iterations:</td>
                        <td>{outputData.iterations}</td>
                    </tr>
                    <tr>
                        <td>Last Input:</td>
                        <td>{outputData.last_input.map((number) => number + ", ")}</td>
                    </tr>
                    <tr>
                        <td>Last Expected Output:</td>
                        <td>{outputData.last_expected_output.map((number) => number + ", ")}</td>
                    </tr>
                    <tr>
                        <td>Last Output:</td>
                        <td>{outputData.last_output.map((number) => number + ", ")}</td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const Home: React.FC = () => {
    return (
        <div className="pt-8 pb-80 sm:pt-12 sm:pb-40 lg:pt-24 lg:pb-48">
            <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 sm:static">
                <Head>
                    <title>Neural Network Tester</title>
                    <link rel="icon" href="/favicon.ico"/>
                </Head>
                <header className="relative overflow-hidden">
                    <div>
                        <h1 className="font font-extrabold text-gray-900 sm:text-6xl">
                            Neural Network Tester
                        </h1>
                        <h2 className="font font-extrabold text-gray-900 sm:text-3xl">
                            Using Temporal.io + Next.js + Python
                        </h2>
                    </div>
                </header>
                <NnTraining />
            </div>
        </div>
    );
};

export default Home;
