# AI Financial Analyst 📈

A professional, multi-agent financial analysis platform that leverages Large Language Models (LLMs) to provide real-time insights, risk detection, and comprehensive financial reports for public companies.

![Dashboard Preview](https://github.com/user-attachments/assets/preview-image-placeholder.png)
*(Note: Replace the placeholder above with your actual screenshot URL after uploading to GitHub)*

## ✨ Key Features

*   **Multi-Agent Architecture**:
    *   **Data Agent**: Fetches real-time financial data (Income Statement, Balance Sheet, Cash Flow) using `yfinance`.
    *   **Trend Agent**: Analyzes historical data to identify growth patterns and market signals.
    *   **Risk Agent**: Uses LLMs (Gemini/GPT) to scan financial metrics for potential risks (Liquidity, Solvency, Profitability).
    *   **Narrative Agent**: Synthesizes all data into a professional "Executive Summary" and detailed report.
*   **Real-time Data**: Integrated with Yahoo Finance API for up-to-date market data.
*   **Intelligent Insights**: Powered by Google Gemini (Free Tier supported) or OpenAI GPT-4.
*   **Interactive Dashboard**: Modern Next.js frontend with:
    *   5-Year Financial Performance Charts (Revenue vs Net Income).
    *   Dynamic Risk Analysis Badges.
    *   Executive Summaries generated in real-time.
    *   Direct links to SEC EDGAR filings and official reports.

## 🛠️ Tech Stack

*   **Frontend**: Next.js 14 (App Router), Tailwind CSS, Recharts, Lucide React.
*   **Backend**: FastAPI, LangChain, LangGraph, Pydantic.
*   **AI/LLM**: Google Gemini (via `langchain-google-genai`) or OpenAI.
*   **Data Source**: `yfinance` (Yahoo Finance API).

## 🚀 Getting Started

### Prerequisites

*   Python 3.10+
*   Node.js 18+
*   A Google API Key (Free) or OpenAI API Key.

### 1. Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys**:
    *   Rename `.env.example` to `.env`:
        ```bash
        mv .env.example .env
        ```
    *   Open `.env` and paste your API Key:
        ```env
        # Recommended: Free Tier available
        GOOGLE_API_KEY=your_gemini_api_key_here
        
        # Optional: If you prefer OpenAI
        # OPENAI_API_KEY=your_openai_key_here
        ```

4.  Start the backend server:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The API will run at `http://localhost:8000`.

### 2. Frontend Setup

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm run dev
    ```

4.  Open your browser and visit `http://localhost:3000`.

## 💡 Usage

1.  Enter a valid US stock ticker (e.g., `AAPL`, `TSLA`, `NVDA`, `MSFT`) in the search bar.
2.  Click **Analyze**.
3.  Wait for the Multi-Agent system to fetch data, compute metrics, and generate the report (usually takes 3-5 seconds).
4.  Review the **Executive Summary**, **Risk Analysis**, and **Financial Charts**.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
