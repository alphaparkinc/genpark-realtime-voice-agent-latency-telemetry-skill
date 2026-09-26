import sys, json
from client import RealtimeVoiceLatencyTelemetry

def main():
    print("Testing RealtimeVoiceLatencyTelemetry...")
    prof = RealtimeVoiceLatencyTelemetry()
    res = prof.run_benchmark_telemetry_profiling()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["turn_101_e2e_ms"] == 650
    assert res["turn_101_compliant"] is True
    print("All Realtime Voice Latency Telemetry tests passed successfully!")

if __name__ == "__main__":
    main()
