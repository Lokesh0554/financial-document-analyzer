from celery_app import celery
from database import SessionLocal
from models import AnalysisResult
from datetime import datetime
import os

@celery.task(bind=True)
def run_analysis_task(self, file_name, query):
    db = SessionLocal()

    try:
        # 1️⃣ create DB record (status = processing)
        record = AnalysisResult(
            task_id=self.request.id,
            file_name=file_name,
            query=query,
            result="Processing...",
            status="processing"
        )
        db.add(record)
        db.commit()

        # 2️⃣ simulate analysis (replace later with CrewAI)
        result_text = f"Financial analysis completed for {file_name}.\nQuery: {query}"

        # 3️⃣ save output file
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"analysis_{timestamp}.txt"

        with open(f"output/{output_file}", "w", encoding="utf-8") as f:
            f.write(result_text)

        # 4️⃣ update DB record (status = completed)
        record.result = result_text
        record.status = "completed"
        db.commit()

        return output_file

    except Exception as e:
        record.status = "failed"
        record.result = str(e)
        db.commit()
        raise e

    finally:
        db.close()
