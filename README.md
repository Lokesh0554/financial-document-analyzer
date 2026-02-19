# financial-document-analyzer
AI Financial Document Analyzer using CrewAI, FastAPI, Celery, Redis and SQLite with async background processing and stored analysis results.
## Commands Used
## Create & Activate Virtual Environment

------>python -m venv venv
------>venv\Scripts\activate
Install Dependencies
------>pip install -r requirements.txt
------>pip install celery redis sqlalchemy python-multipart
Run FastAPI
uvicorn main:app 
------>reload
Open:http://127.0.0.1:8000/docs
Start Redis
------>redis-cli ping
Expected: PONG

Start Celery Worker (Windows)
----->python -m celery -A celery_app worker --pool=solo --loglevel=info
Create Database Tables
python
       from database import engine
    from models import Base
    Base.metadata.create_all(bind=engine)
    exit()
    Test API
----->Upload PDF via /docs → POST /analyze

Output Generated In-->output/analysis_timestamp.txt



## Bugs Found & Fixes

During debugging, several major issues were discovered and fixed.  
The **very first blocker** was related to OpenAI API quota, which directly affected the ability to analyze the provided sample financial PDF.

### 🚨 CRITICAL BLOCKER — OpenAI API Quota (Sample PDF Could Not Be Processed Initially)

**What happened**

When testing the system using the assignment’s provided file:

data/sample.pdf (Tesla Financial Report)

The application returned: RateLimitError: You exceeded your current quota

This happened **before any analysis output could be generated**, which initially made it appear that the system was broken.

### Why this happened

This project relies on CrewAI agents that use an OpenAI LLM to:

- Read the uploaded PDF
- Extract financial insights
- Generate the analysis report

Even though the assignment provided a sample PDF, **LLM execution still requires a funded OpenAI API account**.

The repository did not include:
- API credits
- An active API key
- Offline fallback logic

Therefore the system failed **before producing any output files**, even though the code pipeline itself was correct.

This was an **external infrastructure limitation**, not a code defect.
### How this was handled

To ensure the project could still be validated and tested:

1. Verified that the API pipeline works independently of LLM output.
2. Implemented output saving logic that runs regardless of LLM success.
3. Added background workers and persistence to demonstrate full functionality.
4. Once OpenAI credits were added, the system produced full analysis reports successfully without any code changes.

---

### Result

The system is fully functional.  
The inability to generate the sample PDF output initially was caused **only by missing OpenAI API quota**, not by application bugs.

This has been resolved and verified.

### 1. Dependency Conflicts (Installation Failure)

**Issue**
ResolutionImpossible dependency conflicts


**Cause**
Incompatible versions between CrewAI, OpenAI, LangChain and Pydantic.

**Fix**
- Created a clean virtual environment
- Installed CrewAI-compatible versions
- Removed conflicting LangChain packages

---

### 2. Agent Tool Validation Errors

**Issue**


ValidationError: tools must be BaseTool instances


**Cause**
Python functions were passed directly as tools.

**Fix**
Converted tools into CrewAI-compatible tool objects.

---

### 3. Authentication Errors (Invalid API Key)

**Issue**
401 invalid_api_key

**Fix**
- Added `.env` configuration
- Loaded environment variables correctly
- Restarted services after key updates

### 4. Output Files Not Being Saved

**Issue**
Output folder existed but remained empty.

**Fix**
Implemented timestamp-based report generation:

output/analysis_YYYY-MM-DD_HH-MM-SS.txt
### 5. Blocking API Requests

**Issue**
FastAPI waited for long LLM calls.

**Fix — Bonus Feature**
Integrated **Celery + Redis queue** for background processing.

API now responds instantly and processes tasks asynchronously.

### 6. Celery Crash on Windows

**Issue**

PermissionError [WinError 5]
**Fix**
Started worker using Windows-safe pool:

Celery -A celery_app worker --pool=solo --loglevel=info

### 7. No Database Storage

**Fix — Bonus Feature**
Added SQLAlchemy database to store:
- Uploaded file name
- Query
- Generated analysis
- Status

---

## Final Outcome

After resolving all issues, the system now provides:

✅ Working FastAPI service  
✅ Background processing (Celery + Redis)  
✅ Output report generation  
✅ Database persistence  
✅ Fully debugged dependency stack  
The only initial blocker was **OpenAI API quota**, which is an external requirement for LLM execution.


