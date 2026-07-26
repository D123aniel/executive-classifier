# Executive Classifier — Development Plan

## Product

An Angular web application that accepts an analyst question and executive response, then uses a fine-tuned RoBERTa-large classifier to score the response as:

- Direct
- Partially Evasive
- Fully Evasive

The Angular frontend will run on Vercel. FastAPI and model inference will run on Modal.

## Current Status

### Complete

- [x] Create the public `executive-classifier` repository
- [x] Scaffold Angular 22 with TypeScript
- [x] Scaffold FastAPI with Python
- [x] Restore and load the final `best_model` artifact
- [x] Lock the label order
- [x] Reproduce three saved holdout predictions
- [x] Implement `GET /health`
- [x] Implement `POST /predict`
- [x] Add input validation and truncation reporting
- [x] Add uncertainty and top-two margin output
- [x] Build the main classifier page
- [x] Build the placeholder About page
- [x] Add local Angular-to-FastAPI proxying
- [x] Add responsive UI, loading, and error states
- [x] Add Vercel SPA routing configuration
- [x] Pass backend and frontend tests
- [x] Configure Modal application and persistent model storage
- [x] Upload the final `best_model` artifact to Modal
- [x] Run and verify the temporary Modal development endpoint
- [x] Verify deployed `GET /health` and `POST /predict` responses
- [x] Create the permanent Modal deployment
- [x] Verify the permanent health and prediction endpoints
- [x] Configure Vercel to proxy Angular `/api` requests to Modal
- [x] Verify the Angular production build
- [x] Connect the GitHub repository to Vercel
- [x] Deploy Angular to Vercel
- [x] Verify the production frontend and proxied API endpoints
- [x] Limit Modal to one GPU container and one concurrent request
- [x] Enforce request-size and execution-time limits
- [x] Reduce Modal's idle scale-down window to one minute
- [x] Restrict production CORS to the Vercel application
- [x] Set a $5 monthly Modal workspace spend budget

### In Progress

- [ ] Gather research and report material for the About page

### Next

- [ ] Populate the About page with research materials
- [ ] Add model methodology, metrics, and limitations
- [ ] Add deployment and contributor documentation

## Active Milestone: Project Documentation

The production application is live at `https://executive-classifier.vercel.app`. Vercel serves the Angular application and proxies `/api` requests to the permanent Modal endpoint at `https://d123aniel--executive-classifier-api-fastapi-app.modal.run`. The frontend, `GET /api/health`, and `POST /api/predict` were all verified in production on July 26, 2026. Cost exposure is constrained by scale-to-zero operation with a one-minute idle window, one GPU container, one concurrent request, request-size validation, execution timeouts, and a $5 monthly workspace budget. Production CORS allows the Vercel application and rejects unapproved origins. Deployment is complete; the active milestone is documenting the research, methodology, evaluation results, limitations, and contributor workflow.

## Deployment Responsibilities

### AI

- Application code and tests
- Modal configuration
- Vercel configuration
- API integration
- Documentation
- Deployment troubleshooting

### Daniel

- Authenticate the Modal CLI
- Create or approve the Modal Volume
- Set the Modal workspace spend budget
- Connect the GitHub repository to Vercel
- Approve production deployments
- Provide research and report material for the About page
- Confirm team attribution and model publication permission

Passwords and private tokens must be entered through provider tools, not shared in chat.

## Verification Targets

- Saved model predictions remain reproducible
- Backend tests pass
- Angular tests pass
- Angular production build succeeds without warnings
- Local frontend can call the local API
- Deployed frontend can call Modal
- User-submitted text is not stored or logged
- Model weights and datasets are never committed to Git
