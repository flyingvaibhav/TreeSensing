This is the frontend for the TreeSense Imaging project — a small Next.js + TypeScript application that provides a clean UI for uploading aerial images, running tree-detection with the backend ML model, and viewing historical detection results.

## Quick start

Install dependencies and run the dev server:

```powershell
# from repository root
cd frontend
pnpm install
pnpm dev

# open http://localhost:3000
```

Notes:
- This project uses `pnpm` in the repo, but `npm` or `yarn` will also work.
- The frontend expects the backend API to be available at `NEXT_PUBLIC_API_URL` (default: `http://127.0.0.1:8000`). See "Environment" below.

## Frontend purpose & workflow

High-level flow:

1. User opens the Next.js UI and navigates to the Upload page.
2. User selects an aerial image and clicks "Detect Trees".
3. The frontend validates the file (size/type), shows a preview, then POSTs the image to the backend `/upload` endpoint as multipart/form-data.
4. The backend runs the YOLOv8 model, returns detection results (tree count, confidence scores, image size, timestamp) and stores them in MongoDB.
5. The frontend receives the response and shows the detection summary to the user.
6. The user can view the history page which GETs `/detections` from the backend and shows saved records.

This app uses a small client-side API layer (`src/utils/api.ts`) and a centralized Axios instance (`src/lib/config.ts`) for all requests.

## Project structure (important files)

```
frontend/
├─ src/
│  ├─ app/
│  │  ├─ page.tsx            # Landing page (home)
│  │  ├─ upload/page.tsx     # Upload & detect UI
│  │  └─ trees/page.tsx      # Detection history / table
│  ├─ constants/
│  │  ├─ types.ts            # TS interfaces for Detection, etc.
│  │  └─ config.ts           # API endpoint constants, app limits
│  ├─ lib/
│  │  └─ config.ts           # Axios instance (API) with interceptors
│  └─ utils/
│     └─ api.ts              # uploadImage, fetchDetections, fetchById
└─ README.md
```

## Pages / Components

- `/` (Home) — landing page with quick links to Upload and History.
- `/upload` — file input, preview, upload button. Validates file type and size, shows progress and detection results.
- `/trees` — history of detections: table, stats (total detections, total trees, average confidence), link to upload.

## API interaction

- The frontend uses `src/lib/config.ts` to create an `API` axios instance. `API` base URL is set from `NEXT_PUBLIC_API_URL`.
- `src/utils/api.ts` exposes typed functions:
	- `uploadImage(file: File)` → POST `API_ENDPOINTS.UPLOAD` (multipart). Returns detection result.
	- `fetchDetections(limit?: number)` → GET `API_ENDPOINTS.DETECTIONS`.
	- `fetchDetectionById(id)` → GET `API_ENDPOINTS.DETECTION_BY_ID(id)`.

Use these functions in pages/components; they return typed responses matching `src/constants/types.ts`.

## Environment

Create `.env.local` in `frontend/` (not committed) with:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

This value is used by `src/lib/config.ts` to configure the Axios base URL.

## TypeScript notes

- `tsconfig.json` is configured with the paths alias `@/*` → `./src/*`, enabling imports like `@/utils/api` and `@/constants`.
- Common type files live in `src/constants/types.ts`. Keep interfaces updated when backend response shape changes.

## Styling

- The project uses Tailwind CSS utility classes in the UI. Tailwind config is in the project root (see `postcss.config.mjs` & `tailwind` setup if present).

## Local testing tips

1. Start backend (FastAPI) first so `NEXT_PUBLIC_API_URL` endpoints are reachable.
2. Start the frontend: `pnpm dev` and open `http://localhost:3000`.
3. Upload images via `/upload` and check the developer console/network tab for request/response details.

If you see a `Network Error` from the frontend, check:
- Backend is running (uvicorn main:app --reload)
- CORS is enabled (backend `main.py` has CORS middleware allowing the frontend origin or `*`)
- `NEXT_PUBLIC_API_URL` is correct and reachable from the browser

## Troubleshooting

- "Network Error": ensure backend is running and accessible at `NEXT_PUBLIC_API_URL`. Also check the browser console for CORS errors.
- If API calls return 500: inspect the backend logs (uvicorn) for stack trace. A common case is MongoDB `ObjectId` serialization (handled in backend already).
- If types mismatch: update `src/constants/types.ts` to reflect the backend response.

## Deployment

- Frontend: deploy on Vercel (recommended) or Netlify — ensure `NEXT_PUBLIC_API_URL` points to your deployed backend.
- Backend: deploy FastAPI to any provider (Railway, Render, Heroku, AWS) and update `NEXT_PUBLIC_API_URL` accordingly.

## Contributing

Please follow existing code style and TypeScript typings. Add new types into `src/constants/types.ts`. Create API helpers in `src/utils/api.ts` and consume them from the pages.

---

If you want, I can also add a short example snippet at the top demonstrating how to call the `uploadImage` util from a component — say `useUpload` hook or similar. Would you like that?
