# Lab 16 Benchmark Report

## Metadata
- Dataset: hotpot_100.json
- Mode: ollama_remote
- Records: 200
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.65 | 0.79 | 0.14 |
| Avg attempts | 1 | 1.65 | 0.65 |
| Avg token estimate | 1930.44 | 3408.28 | 1477.84 |
| Avg latency (ms) | 7012.52 | 11438.14 | 4425.62 |

## Failure modes
```json
{
  "react": {
    "none": 65,
    "wrong_final_answer": 35
  },
  "reflexion": {
    "none": 79,
    "wrong_final_answer": 21
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
