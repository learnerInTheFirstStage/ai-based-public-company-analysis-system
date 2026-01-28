# AI Agent--based Financial Analysis System

## Development Specification

------------------------------------------------------------------------

## 1. Project Overview

This project aims to build an **AI Agent--based system** that analyzes
public company financial filings (10-K / 10-Q) and produces
**multi-dimensional, explainable financial insights**.

The focus is on: - Agent orchestration - System design -
Interpretability and modularity

Rather than investment advice or real-time trading.

------------------------------------------------------------------------

## 2. Project Goals

-   Showcase agent-based system design
-   Demonstrate structured financial analysis using LLMs
-   Emphasize explainability over raw metrics
-   Serve as a strong portfolio and interview project

------------------------------------------------------------------------

## 3. Non-Goals

-   No real-time stock prices
-   No trading or investment recommendations
-   No custom model training or fine-tuning
-   No large-scale company coverage

------------------------------------------------------------------------

## 4. System Architecture

    User
     ↓
    Analysis Orchestrator (Main Agent)
     ↓
    ┌────────────────────────────────┐
    │ Data Understanding Agent       │
    │ Metric Computation Agent       │
    │ Trend Analysis Agent           │
    │ Risk Signal Agent              │
    └────────────────────────────────┘
     ↓
    Narrative Generation Agent
     ↓
    Frontend (Text + Charts)

------------------------------------------------------------------------

## 5. Agent Design Pattern

-   Single-responsibility agents
-   Strict input/output contracts (JSON)
-   LLMs used for reasoning & explanation only
-   Deterministic computation handled by code

This minimizes hallucination and improves debuggability.

------------------------------------------------------------------------

## 6. Agent Responsibilities

### 6.1 Data Understanding Agent

-   Parse 10-K / 10-Q filings
-   Extract structured financial statements
-   Normalize reporting periods

**Output:** structured JSON

------------------------------------------------------------------------

### 6.2 Metric Computation Agent

-   Compute financial ratios using code
-   Examples:
    -   Gross Margin
    -   Operating Margin
    -   Free Cash Flow
    -   Debt Ratio

**Note:** No LLM involvement

------------------------------------------------------------------------

### 6.3 Trend Analysis Agent

-   Analyze YoY / QoQ changes
-   Detect divergences:
    -   Revenue ↑ but Cash Flow ↓
    -   Profit growth driven by one-time events

**Output:** signals + confidence scores

------------------------------------------------------------------------

### 6.4 Risk Signal Agent

-   Analyze MD&A and Risk Factors
-   Detect:
    -   New risk disclosures
    -   Tone shifts
    -   One-off adjustments

**Output:** risk flags

------------------------------------------------------------------------

### 6.5 Narrative Generation Agent

-   Aggregate all agent outputs
-   Produce:
    -   TL;DR summary
    -   Detailed explanations
    -   Key takeaways

This is the only agent generating free-form text.

------------------------------------------------------------------------

## 7. Orchestrator Logic

-   Controls agent execution order
-   Skips agents based on data availability
-   Aggregates structured outputs
-   Passes consolidated context to Narrative Agent

------------------------------------------------------------------------

## 8. Data Pipeline

1.  Retrieve public filings
2.  Clean and preprocess text
3.  Extract structured data
4.  Cache intermediate agent outputs

------------------------------------------------------------------------

## 9. Frontend Presentation

-   Company overview
-   Financial health summary
-   Key signals
-   Charts with agent explanations
-   Methodology / Explainability section

------------------------------------------------------------------------

## 10. Technology Stack

**Backend** - Python - FastAPI

**Data** - Pandas - DuckDB

**Agent Framework** - LangGraph or custom orchestrator

**Frontend** - Next.js - Recharts / ECharts

------------------------------------------------------------------------

## 11. MVP Scope

-   1--2 companies
-   1--2 years of data
-   Limited financial metrics
-   Fixed analysis templates

------------------------------------------------------------------------

## 12. Future Extensions

-   Valuation Agent
-   Scenario Analysis Agent
-   Interactive Q&A Agent
-   User-controlled analysis depth

------------------------------------------------------------------------

## 13. Limitations & Disclaimer

This system is for **educational and analytical purposes only** and does
**not provide investment advice**.
