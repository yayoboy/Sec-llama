"""
Anomaly Detector using AI and statistical methods
"""

from typing import List, Dict, Any
from collections import Counter
import statistics

from core.llm_interface import get_llm


class AnomalyDetector:
    """Detect anomalies in security logs"""

    def __init__(self):
        self.llm = get_llm()
        self.baseline = {}

    def detect_anomalies(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in logs"""
        print("[*] Detecting anomalies...")

        anomalies = []

        # Request frequency anomalies
        ip_counts = Counter([log.get("ip") for log in logs if "ip" in log])

        # Calculate mean and std dev
        if ip_counts:
            counts = list(ip_counts.values())
            mean = statistics.mean(counts)
            std_dev = statistics.stdev(counts) if len(counts) > 1 else 0

            # Flag IPs with requests > mean + 2*std_dev
            threshold = mean + (2 * std_dev)

            for ip, count in ip_counts.items():
                if count > threshold:
                    anomalies.append({
                        "type": "high_request_rate",
                        "ip": ip,
                        "count": count,
                        "threshold": threshold,
                    })

        print(f"[!] Found {len(anomalies)} anomalies")
        return anomalies
