import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT="""You are a senior cybersecurity analyst specializing in 
Windows endpoint security and threat detection. You will be given structured 
data from a Windows Security Event Log analysis tool. Your job is to:
1. Interpret the anomalies detected and assess their threat level (Low / Medium / High / Critical).
2. Explain what each flagged IP's behavior suggests in plain, professional language.
3. Recommend concrete remediation steps for a system administrator.
Be concise but thorough. Format your response in clear sections."""

def _build_user_prompt(analysis_results: dict) -> str:
    flagged = analysis_results.get("flagged_ips", [])
    if not flagged:
        return "The analysis found no anomalies. Please confirm the system appears clean."
    lines = [
        f"Windows Security Event Log Analysis Results:",
        f"- Total failed logon events analyzed: {analysis_results['total_events_analyzed']}",
        f"- Unique source IPs observed: {analysis_results['unique_source_ips']}",
        f"- Flagged suspicious IPs: {len(flagged)}",
        "",
        "Flagged IP Details:",
    ]
    for i, entry in enumerate(flagged, start=1):
        lines.append(f"\n  [{i}] IP Address: {entry['ip']}")
        lines.append(f"Failed Attempts : {entry['attempt_count']}")
        lines.append(f"Targeted Users  : {', '.join(entry['targeted_usernames'])}")
        lines.append(f"Triggered Rules : {', '.join(entry['triggered_rules'])}")
    lines.append("\nPlease provide your threat assessment and remediation recommendations.")
    return "\n".join(lines)

class BaseLLMProvider(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, user_prompt: str) -> str:
        pass

class GroqProvider(BaseLLMProvider):
    def __init__(self):
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("[!] GROQ_API_KEY not found in .env file.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        print(f"[*] Sending analysis to Groq ({self.model})...")
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
        )
        return response.choices[0].message.content

def _get_provider() -> BaseLLMProvider:
    provider_name = os.getenv("LLM_PROVIDER", "groq").lower().strip()
    providers = {
        "groq": GroqProvider,
    }
    if provider_name not in providers:
        raise ValueError(
            f"[!] Unknown LLM_PROVIDER '{provider_name}'. "
            f"Valid options: {list(providers.keys())}"
        )
    print(f"[*] LLM Provider: {provider_name.upper()}")
    return providers[provider_name]()


def run_threat_analysis(analysis_results: dict) -> str:
    if not analysis_results:
        return "[!] No analysis results to send."
    provider = _get_provider()
    user_prompt = _build_user_prompt(analysis_results)
    return provider.complete(SYSTEM_PROMPT, user_prompt)