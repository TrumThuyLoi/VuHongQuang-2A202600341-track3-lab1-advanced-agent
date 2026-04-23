# Lab 16 Benchmark Report

## Metadata
- Dataset: hard
- Mode: ollama_remote
- Records: 60
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.5333 | 0.6667 | 0.1334 |
| Avg attempts | 1 | 1.9667 | 0.9667 |
| Avg token estimate | 1878.5 | 4087.27 | 2208.77 |
| Avg latency (ms) | 4386.83 | 11174.6 | 6787.77 |

## Failure modes
```json
{
  "react": {
    "none": 16,
    "wrong_final_answer": 14
  },
  "reflexion": {
    "none": 20,
    "wrong_final_answer": 10
  }
}
```

## Extensions implemented
- structured_evaluator
- reflection_memory
- benchmark_report_json
- mock_mode_for_autograding

## Discussion
Reflexion helps when the first attempt stops after the first hop or drifts to a wrong second-hop entity. The tradeoff is higher attempts, token cost, and latency. In a real report, students should explain when the reflection memory was useful, which failure modes remained, and whether evaluator quality limited gains.
