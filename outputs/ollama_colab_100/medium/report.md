# Lab 16 Benchmark Report

## Metadata
- Dataset: medium
- Mode: ollama_remote
- Records: 80
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.625 | 0.825 | 0.2 |
| Avg attempts | 1 | 1.625 | 0.625 |
| Avg token estimate | 1948.3 | 3343.97 | 1395.67 |
| Avg latency (ms) | 4470.88 | 8525.83 | 4054.95 |

## Failure modes
```json
{
  "react": {
    "wrong_final_answer": 15,
    "none": 25
  },
  "reflexion": {
    "none": 33,
    "wrong_final_answer": 7
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
