from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.agents.orchestrator import run_analysis
from app.models.schemas import AnalysisResult

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Financial Analyst")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Financial Analyst API is running"}

@app.post("/analyze/{ticker}", response_model=AnalysisResult)
async def analyze_company(ticker: str):
    """
    Trigger the analysis pipeline for a specific company ticker.
    """
    # In a real scenario, we might trigger an async job here.
    # For MVP, we run it synchronously or await the async function.
    result = await run_analysis(ticker)
    return result
