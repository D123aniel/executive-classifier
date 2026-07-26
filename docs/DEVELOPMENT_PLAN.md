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

### In Progress

- [ ] Connect the GitHub repository to Vercel

### Next

- [ ] Restrict production CORS origins
- [ ] Deploy Angular to Vercel
- [ ] Add production budget and abuse safeguards
- [ ] Populate the About page with research materials
- [ ] Add model methodology, metrics, and limitations
- [ ] Add deployment and contributor documentation

## Active Milestone: Deployment

The Modal image, persistent model volume, and permanent scale-to-zero endpoint are working. Both `GET /health` and `POST /predict` were verified against the permanent endpoint on July 26, 2026. The permanent API is available at `https://d123aniel--executive-classifier-api-fastapi-app.modal.run`. The next step is to route Angular's `/api` requests to this endpoint through Vercel, then deploy and verify the frontend.

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
- Set Modal spending limits and alerts
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
