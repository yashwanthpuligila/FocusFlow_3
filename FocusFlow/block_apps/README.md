Block Apps - local API and blocker

This folder contains the Python-based blocker (existing) and a small Node/Express API (server.js) to let the frontend read/write the block list and enable/disable blocking.

How to run

1. Install Node dependencies and start the API (PowerShell):

    cd block_apps
    npm install
    npm start

The API listens on http://localhost:5000 by default.

2. Run the Python blocker (this script watches block_enabled.txt and blocklist.txt):

    # in a separate terminal
    cd block_apps
    python block_apps.py

Frontend

The React frontend can call the API endpoints:
- GET /blocklist -> { sites: string[] }
- POST /blocklist { sites: string[] }
- GET /status -> { enabled: boolean }
- POST /enable -> { ok: true, enabled: true }
- POST /disable -> { ok: true, enabled: false }
