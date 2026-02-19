from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from tasks import run_analysis_task
import os

app = FastAPI(title="Financial Document Analyzer")

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document")
):
    try:
        os.makedirs("data", exist_ok=True)

        file_path = f"data/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Send job to Celery queue
        task = run_analysis_task.delay(file.filename, query)

        return {
            "status": "queued",
            "task_id": task.id,
            "message": "Analysis started in background"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔹 ADD THIS ENDPOINT
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"output/{filename}"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
