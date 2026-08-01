# FitNova - AI Sales Call Intelligence Platform (Frontend)

Frontend-only scaffold. No backend, no auth - everything runs on mock JSON data in `src/mock/`.

## Getting started

```bash
npm install
npm run dev
```

Then open the URL shown in the terminal (usually http://localhost:5173).

To build for production:

```bash
npm run build
```

## How it's organized

- `src/pages/` - one folder per role (Director, Leader, Advisor) plus Login and Shared pages (Call Details, Analytics, Reports, Settings, 404)
- `src/components/` - reusable pieces, grouped by what they're for (common, layout, dashboard, charts, upload, transcript, analysis)
- `src/mock/` - fake JSON data standing in for the backend
- `src/services/mockService.js` - functions that return Promises, just like real API calls would. When the backend is ready, swap the insides of these functions for `apiClient` (axios) calls - the rest of the app won't need to change
- `src/routes/AppRoutes.jsx` - every route in one place
- `src/styles/index.css` - Tailwind + the FitNova color theme (edit the `@theme` block to change colors globally)

## Login flow

The login page doesn't check credentials - it just routes you to the dashboard matching whichever role you pick in the dropdown (Sales Director / Team Leader / Advisor).

## Notes for backend integration later

- Replace calls to `src/services/mockService.js` functions with `src/services/apiClient.js` (axios) calls
- Update `apiClient.js`'s `baseURL` to point at your real API
- The Audio Player and Upload Dropzone are visual placeholders only
