# LangSmith Configuration Fix

## Issue
The LangSmith project was not appearing in the UI because the environment variables defined in `.env` were not being loaded into the application process.

## Fix
I have updated the following files to explicitly load the `.env` file using `python-dotenv`:

1.  `backend/api.py`: Added `load_dotenv()` at the top of the file. This ensures that when running the API server (e.g., via `uvicorn` or `python api.py`), the environment variables are loaded.
2.  `backend/main.py`: Added `load_dotenv()` at the top of the file. This ensures that when running the CLI chat (via `python main.py`), the environment variables are loaded.

## Verification
To verify the fix:
1.  Ensure you have `python-dotenv` installed (it is listed in `requirements.txt`).
2.  Run the application (API or CLI).
3.  Check your LangSmith project UI. You should now see traces appearing.

## Note
The `backend/ingest_data.py` script was already loading `.env` correctly, so data ingestion traces (if any) might have been working if that script was run.
