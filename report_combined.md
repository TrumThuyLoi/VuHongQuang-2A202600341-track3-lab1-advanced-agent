# Lab 16 Combined Benchmark Report

## Overview
- Dataset source: `data/hotpot_100.json`
- Distribution: 30 easy, 40 medium, 30 hard
- Runtime mode: `ollama_remote`
- Output root: `outputs/ollama_colab_100`

## 1. Tong Hop Toan Bo (100 mau)

### Metadata
- Report path: `outputs/ollama_colab_100/report.json`
- Records: 200 (100 mau x 2 agent)
- Agents: react, reflexion

### Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.65 | 0.79 | +0.14 |
| Avg attempts | 1.00 | 1.65 | +0.65 |
| Avg token estimate | 1930.44 | 3408.28 | +1477.84 |
| Avg latency (ms) | 7012.52 | 11438.14 | +4425.62 |

### Failure Modes
- ReAct: none=65, wrong_final_answer=35
- Reflexion: none=79, wrong_final_answer=21

### Autograde
- Total: 92/100
- Flow (Core): 72/80
- Schema: 30/30
- Experiment: 30/30
- Analysis: 12/20
- Bonus: 20/20

---

## 2. Muc Do De (30 mau)

### Metadata
- Report path: `outputs/ollama_colab_100/easy/report.json`
- Records: 60 (30 mau x 2 agent)

### Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.8000 | 0.8667 | +0.0667 |
| Avg attempts | 1.0000 | 1.3667 | +0.3667 |
| Avg token estimate | 1958.57 | 2815.03 | +856.46 |
| Avg latency (ms) | 7955.33 | 6802.43 | -1152.90 |

### Failure Modes
- ReAct: none=24, wrong_final_answer=6
- Reflexion: none=26, wrong_final_answer=4

### Autograde
- Total: 82/100
- Flow (Core): 62/80
- Schema: 30/30
- Experiment: 20/30
- Analysis: 12/20
- Bonus: 20/20

---

## 3. Muc Do Trung Binh (40 mau)

### Metadata
- Report path: `outputs/ollama_colab_100/medium/report.json`
- Records: 80 (40 mau x 2 agent)

### Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.6250 | 0.8250 | +0.2000 |
| Avg attempts | 1.0000 | 1.6250 | +0.6250 |
| Avg token estimate | 1948.30 | 3343.97 | +1395.67 |
| Avg latency (ms) | 4470.88 | 8525.83 | +4054.95 |

### Failure Modes
- ReAct: none=25, wrong_final_answer=15
- Reflexion: none=33, wrong_final_answer=7

### Autograde
- Total: 82/100
- Flow (Core): 62/80
- Schema: 30/30
- Experiment: 20/30
- Analysis: 12/20
- Bonus: 20/20

---

## 4. Muc Do Kho (30 mau)

### Metadata
- Report path: `outputs/ollama_colab_100/hard/report.json`
- Records: 60 (30 mau x 2 agent)

### Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.5333 | 0.6667 | +0.1334 |
| Avg attempts | 1.0000 | 1.9667 | +0.9667 |
| Avg token estimate | 1878.50 | 4087.27 | +2208.77 |
| Avg latency (ms) | 4386.83 | 11174.60 | +6787.77 |

### Failure Modes
- ReAct: none=16, wrong_final_answer=14
- Reflexion: none=20, wrong_final_answer=10

### Autograde
- Total: 82/100
- Flow (Core): 62/80
- Schema: 30/30
- Experiment: 20/30
- Analysis: 12/20
- Bonus: 20/20

---

## Nhan Xet Nhanh
- Report tong dat 92/100 vi dap ung nguong thuc nghiem `num_records >= 100`.
- Cac report theo muc (easy/medium/hard) cung 82/100 vi autograde hien tai cham theo rule cau truc/nguong, khong co trong so rieng theo do kho.
- Ve chat luong mo hinh, Reflexion deu cai thien EM tren ca 3 muc, nhung doi lai token va latency tang ro ret.

## File Lien Quan
- Combined report: `outputs/ollama_colab_100/report_combined.md`
- Overall report JSON: `outputs/ollama_colab_100/report.json`
- Easy report JSON: `outputs/ollama_colab_100/easy/report.json`
- Medium report JSON: `outputs/ollama_colab_100/medium/report.json`
- Hard report JSON: `outputs/ollama_colab_100/hard/report.json`
- Run log: `outputs/ollama_colab_100/run.log`
