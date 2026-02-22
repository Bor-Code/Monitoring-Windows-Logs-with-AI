from src.collector.event_collector import fetch_failed_logons, display_events
from src.analyzer.anomaly_detector import analyze, display_analysis
from src.ai.threat_analyzer import run_threat_analysis
from src.reporter.report_generator import generate_report

def main():
    events = fetch_failed_logons()
    display_events(events)
    results = analyze(events)
    display_analysis(results)
    ai_report = run_threat_analysis(results)
    print("\n" + "=" * 55)
    print("AI THREAT ASSESSMENT")
    print("=" * 55)
    print(ai_report)
    print("=" * 55)
    generate_report(events, results, ai_report)

if __name__ == "__main__":
    main()