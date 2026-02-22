# 🛡️ AI-Powered Windows Event Log Analyzer

A Python-based security tool that collects Windows Security Event Logs,
detects anomalies using rule-based analysis, and generates AI-powered
threat assessment reports using a Large Language Model.

## Features

- Collects failed logon events (Event ID 4625) from Windows Security Log
- Detects brute force and credential stuffing patterns
- Sends findings to an LLM (Groq / OpenAI / Anthropic) for threat analysis
- Generates a professional HTML report with findings and recommendations

## Project Structure
```
ai-event-log-analyzer/
├── src/
│   ├── collector/event_collector.py   # Windows Event Log collection
│   ├── analyzer/anomaly_detector.py   # Rule-based anomaly detection
│   ├── ai/threat_analyzer.py          # LLM threat analysis
│   └── reporter/report_generator.py   # HTML report generation
├── reports/                           # Generated reports (git-ignored)
├── .env                               # API keys (git-ignored)
├── requirements.txt
└── main.py
```

## Setup

1. Clone the repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file in the project root:
```env
   GROQ_API_KEY=your_groq_api_key_here
   LLM_PROVIDER=groq
```
4. Get a free Groq API key at [console.groq.com](https://console.groq.com)

## Usage

> ⚠️ Must be run as Administrator to access Windows Security Event Logs.
```bash
python main.py
```

The HTML report will be saved to the `reports/` directory.

## Detection Rules

| Rule | Description |
|------|-------------|
| `BRUTE_FORCE` | Single IP with 5+ failed logon attempts |
| `MULTI_ACCOUNT_TARGETING` | Single IP targeting 3+ distinct usernames |

## Tech Stack

- **Python 3.13**
- **pywin32** — Windows Event Log access
- **Groq API** — LLM inference (Llama 3.3 70B)
- **python-dotenv** — Environment variable management