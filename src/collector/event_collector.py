"""
    Relavent Event ID's:
        4624-Succesful Logon
        4625-Failed Logon (Our Primary Focus for Anomaly Detection)
"""
import win32evtlog
import win32evtlogutil
import win32con
import datetime

#Constants
LOG_TYPE="Security"
TARGET_EVENT_ID=4625
MAX_EVENTS_TO_FETCH=50

def fetch_failed_logons(max_events: int=MAX_EVENTS_TO_FETCH)->list[dict]:
    events=[]
    hand=win32evtlog.OpenEventLog(None,LOG_TYPE)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    print(f"[*] Querying '{LOG_TYPE}' log for Event ID {TARGET_EVENT_ID} (Failed Logons)...")
    print(f"[*] Fetching up to {max_events} events. This may take a moment...\n")

    try:
        while len(events)<max_events:
            records=win32evtlog.ReadEventLog(hand,flags,0)
            if not records:
                break
            for event in records:
                if len(events)>=max_events:
                    break
                if event.EventID & 0xFFFF!=TARGET_EVENT_ID:
                    continue
                inserts=event.StringInserts or []
                parsed_event={
                     "event_id": TARGET_EVENT_ID,
                    "timestamp": str(event.TimeGenerated),
                    "target_username": inserts[5] if len(inserts) > 5 else "N/A",
                    "target_domain": inserts[6] if len(inserts) > 6 else "N/A",
                    "source_ip": inserts[19] if len(inserts) > 19 else "N/A",
                    "logon_type": inserts[10] if len(inserts) > 10 else "N/A",
                    "failure_reason": inserts[11] if len(inserts) > 11 else "N/A",
                }
                events.append(parsed_event)
    finally:
        win32evtlog.CloseEventLog(hand)
    print(f"[+] Found {len(events)} failed logon event(s).\n")
    return events

def display_events(events:list[dict])->None:
    if not events:
        print("[!] No failed logon events found. Your system looks clean (or the log is empty).")
        return
    separator="-"*55
    for i, event in enumerate(events,start=1):
        print(f"  Event #{i}")
        print(separator)
        print(f"  Timestamp      : {event['timestamp']}")
        print(f"  Target User    : {event['target_username']}@{event['target_domain']}")
        print(f"  Source IP      : {event['source_ip']}")
        print(f"  Logon Type     : {event['logon_type']}")
        print(f"  Failure Reason : {event['failure_reason']}")
        print()

if __name__ == "__main__":
    failed_logons=fetch_failed_logons()
    display_events(failed_logons)