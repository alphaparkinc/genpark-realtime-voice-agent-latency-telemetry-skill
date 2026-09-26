import sys, json
from client import RealtimeVoiceLatencyTelemetry

def main():
    prof = RealtimeVoiceLatencyTelemetry()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(prof.run_benchmark_telemetry_profiling(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "record_pipeline_event", "description": "Record pipeline stage timestamp (VAD, STT, LLM_FIRST_TOKEN, TTS_FIRST_AUDIO, PLAYOUT)."},
                        {"name": "compute_turn_latency_breakdown", "description": "Calculate stage-by-stage latency breakdown and critical path."},
                        {"name": "generate_sla_diagnostic_report", "description": "Produce SLA latency percentiles (P50, P90, P99) and bottleneck diagnostic."},
                        {"name": "run_benchmark_telemetry_profiling", "description": "Simulate and benchmark multi-turn voice session latency analytics."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "record_pipeline_event":
                    out = prof.record_pipeline_event(args.get("turn_id", "default"), args.get("stage_name", "UNKNOWN"), args.get("timestamp_ms"), args.get("metadata"))
                elif tname == "compute_turn_latency_breakdown":
                    out = prof.compute_turn_latency_breakdown(args.get("turn_id", "default"))
                elif tname == "generate_sla_diagnostic_report":
                    out = prof.generate_sla_diagnostic_report()
                elif tname == "run_benchmark_telemetry_profiling":
                    out = prof.run_benchmark_telemetry_profiling()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
