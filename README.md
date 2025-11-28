# temporal-io-learning
A sandbox to learn Temporal.io usage with Python, TypeScript and Next.js.

# Getting Started
- cp server/temporal.db.new server/temporal.db
- docker compose up -d
- execute "poetry install" and "bin/run run_worker.py" in backend container
- server ui: http://localhost:8233
- frontend: http://localhost:3000

# Notes
- https://learn.temporal.io/tutorials/typescript/build-one-click-order-app-nextjs/
- https://learn.temporal.io/getting_started/typescript/hello_world_in_typescript/
- temporal workflows/workers in frontend app are not used atm, as i wanted to test running workflows implemented in the backend app
