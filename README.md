# Video Generation Agent

This repository demonstrates how to build a video generation agent using the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/), [Gemini 2.5 Flash Image (Nano Banana)](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-image?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog), and [Veo 3.1](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/veo-3.1-generate-preview?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog).

It is a full-stack web application designed to be deployed on [Google Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog), with ADK Web UI,
using [Vertex AI Agent Engine Sessions Service](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/overview?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog) for session management and [Google Cloud Storage](https://cloud.google.com/storage/docs/introduction?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog) for storing artifacts.

## Features

TODO

## Architecture

TODO

## Prerequisites

* An existing [Google Cloud Project](https://console.cloud.google.com/?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog). New customers [**get $300 in free credits**](https://cloud.google.com/free?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog) to run, test, and deploy workloads.
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/install?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog).
* [Python 3.11+](https://www.python.org/downloads/?utm_campaign=CDR_0xc245fc42_default_b443956672&utm_medium=external&utm_source=blog).

## Installation

1. Clone the repository:

    TODO

2. Create a Python virtual environment and activate it:

    > We recommend using [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

    ```bash
    uv venv .venv
    source .venv/bin/activate
    ```

3. Install the Python dependencies:

    ```bash
    uv pip install pip
    uv pip install -r agents/video_avatar_agent/requirements.txt
    uv pip install -r mcp/requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root of the project by copying the `.env-template` file:

    ```bash
    cp .env-template .env
    ```

2. Update the `.env` file with your Google Cloud project ID, location, and the name of your GCS bucket for AI assets.

## Running Locally

To start the MCP server run:

```bash
./deployment/run_mcp_local.sh
```

The MCP server will run on `http://localhost:8080`.

To run the agent locally, use the `run_agent_local.sh` script:

```bash
./deployment/run_agent_local.sh
```

This will:

1. Register an Agent Engine resource for using with the session service.
2. Start a local a web server with the ADK Web UI, which you can access in your browser.

## Deployment

To deploy the MCP server and the agent to Cloud Run, use the `deploy.sh` script:

```bash
./deployment/deploy.sh
```

This script will:

1. Register an Agent Engine resource for using with the session service.
2. Deploy the MCP server to Cloud Run.
3. Deploy the agent to Cloud Run, with the ADK Web UI.

## Agent Details

TODO
