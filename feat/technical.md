# Technical Specification -> Building the frontend
---

***Links***
- Where to find the whole specification: [[frontend]]

## Requirements
---
- Move all backend logic to a new `/backend` directory and create a more modern flask infrastructure for this
- Make a new frontend directory that houses the required frontend infrastructure and files
- Make sure they are both linked together correctly (assuming the frontend is on a new service on the same app service plan)
- Do local testing with a build to ensure that this all works, use chrome mcp when you reach this step
- Update github actions workflow to ensure that the build passes with frontend and backend correctly working in tandem on the same Azure app service
- write detailed instructions for hosting on azure and testing locally

