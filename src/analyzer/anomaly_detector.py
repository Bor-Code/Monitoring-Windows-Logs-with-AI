from collections import defaultdict

BRUTE_FORCE_THRESHOLD = 5
MULTI_ACCOUNT_THRESHOLD = 3

def analyze(events: list[dict]) -> dict:
    if not events:
        print("[!] No events to analyze.")
        return {}
    print(f"[*] Running anomaly detection on {len(events)} event(s)...\n")
    ip_stats = defaultdict(lambda: {
        "attempt_count": 0,
        "targeted_usernames": set(),
    })
    for event in events:
        ip = event.get("source_ip", "N/A")
        if ip in ("N/A", "-", ""):
            continue
        ip_stats[ip]["attempt_count"] += 1
        ip_stats[ip]["targeted_usernames"].add(event.get("target_username", "N/A"))
    brute_force_ips = _detect_brute_force(ip_stats)
    multi_account_ips = _detect_multi_account(ip_stats)
    all_flagged_ips = set(brute_force_ips) | set(multi_account_ips)
    results = {
        "total_events_analyzed": len(events),
        "unique_source_ips": len(ip_stats),
        "flagged_ips": _build_flagged_ip_report(
            all_flagged_ips, ip_stats, brute_force_ips, multi_account_ips
        ),
    }
    return results

def _detect_brute_force(ip_stats: dict)->list[str]:
    flagged = []
    for ip, stats in ip_stats.items():
        if stats["attempt_count"]>=BRUTE_FORCE_THRESHOLD:
            flagged.append(ip)
    return flagged


def _detect_multi_account(ip_stats: dict)->list[str]:
    flagged = []
    for ip, stats in ip_stats.items():
        if len(stats["targeted_usernames"])>=MULTI_ACCOUNT_THRESHOLD:
            flagged.append(ip)
    return flagged


def _build_flagged_ip_report(
    all_flagged_ips: set,
    ip_stats: dict,
    brute_force_ips: list,
    multi_account_ips: list,
)->list[dict]:
    report = []
    for ip in all_flagged_ips:
        triggered_rules = []
        if ip in brute_force_ips:
            triggered_rules.append("BRUTE_FORCE")
        if ip in multi_account_ips:
            triggered_rules.append("MULTI_ACCOUNT_TARGETING")
        report.append({
            "ip": ip,
            "attempt_count": ip_stats[ip]["attempt_count"],
            "targeted_usernames": list(ip_stats[ip]["targeted_usernames"]),
            "triggered_rules": triggered_rules,
        })
    report.sort(key=lambda x: x["attempt_count"], reverse=True)
    return report

def display_analysis(results: dict) -> None:
    if not results:
        return
    print("=" * 55)
    print("          ANOMALY DETECTION REPORT")
    print("=" * 55)
    print(f"  Total Events Analyzed : {results['total_events_analyzed']}")
    print(f"  Unique Source IPs     : {results['unique_source_ips']}")
    print(f"  Flagged IPs           : {len(results['flagged_ips'])}")
    print("=" * 55)
    if not results["flagged_ips"]:
        print("\n[✓] No anomalies detected. No IPs exceeded the thresholds.")
        return
    print("\n[!] SUSPICIOUS ACTIVITY DETECTED:\n")
    separator = "-" * 55
    for entry in results["flagged_ips"]:
        print(separator)
        print(f"  IP Address       : {entry['ip']}")
        print(f"  Failed Attempts  : {entry['attempt_count']}")
        print(f"  Targeted Users   : {', '.join(entry['targeted_usernames'])}")
        print(f"  Triggered Rules  : {', '.join(entry['triggered_rules'])}")
    print(separator)