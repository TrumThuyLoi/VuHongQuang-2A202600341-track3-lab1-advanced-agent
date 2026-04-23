# Lab 16 Benchmark Report

## Metadata
- Dataset: easy
- Mode: ollama_remote
- Records: 60
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.8 | 0.8667 | 0.0667 |
| Avg attempts | 1 | 1.3667 | 0.3667 |
| Avg token estimate | 1958.57 | 2815.03 | 856.46 |
| Avg latency (ms) | 7955.33 | 6802.43 | -1152.9 |

## Failure modes
```json
{
  "react": {
    "none": 24,
    "wrong_final_answer": 6
  },
  "reflexion": {
    "none": 26,
    "wrong_final_answer": 4
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
