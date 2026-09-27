# DEBUNKIFY — Deployable Version

This package uses **DEBUNKIFY-BOTH-LOGOS-IMAGE-ONLY** as the frontend/design base. The frontend HTML, CSS, assets, branding, layout and visual styling are kept unchanged.

## Active features
- News / Text Verification
- Reverse Image Verification

The backend contains the working investigation logic for these two features, including live search evidence, Groq analysis, Cloudinary image upload and Google Lens reverse-image search through SerpAPI.

## Not included as active project features
- Website Shield
- Social verification
- Video verification
- Extra website/security scanning modules

## Secrets
The real `.env` files are intentionally not included. Copy `backend/.env.example` to `backend/.env` for local development and enter your own credentials.

Required variables:
- `SERPAPI_KEY`
- `GROQ_API_KEY`
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

## Local run
From the project root:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Render deployment
The included `render.yaml` is configured for a Python web service. Add the five environment variables in Render before deploying.

## Frontend API URL
The existing frontend supports an API URL through the `?api=` query parameter, `window.DEBUNKIFY_API_URL`, or localStorage key `DEBUNKIFY_API_URL`.


## Important: API keys
Do not commit `backend/.env` to GitHub. Set `GEMINI_API_KEY`, `GROQ_API_KEY`, `SERPAPI_KEY` (and Cloudinary variables if reverse-image upload storage is used) in Render Environment Variables. Keep only `.env.example` in the repository.
