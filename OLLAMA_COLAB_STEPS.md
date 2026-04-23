# Huong Dan Chuyen Tu Mock Sang Ollama (Host tren Colab)

Tai lieu nay tong hop cac buoc da cap nhat cho truong hop ban da host Ollama tren Colab va da test endpoint thanh cong.

## 1. Cau hinh bien moi truong

Tao (hoac cap nhat) file `.env`:

```env
LLM_LINK=<URL OpenAI-compatible endpoint cua ban>
LLM_MODEL=qwen2.5:7b
```

Ghi chu:
- Neu server cua ban yeu cau duong dan `/v1`, hay dam bao `LLM_LINK` da dung duong dan.
- `test_llm.py` dang dung `api_key='ollama'`, co the giu nguyen neu endpoint chap nhan.

## 2. Bo sung dependencies

Cap nhat `requirements.txt` de co toi thieu:

- `openai`
- `python-dotenv`
- `pydantic`

Sau do cai dat lai:

```bash
pip install -r requirements.txt
```

## 3. Hoan thien schema trong src/reflexion_lab/schemas.py

Can thay cac TODO bang model day du:

- `JudgeResult`:
  - `score: int` (0/1)
  - `reason: str`
  - `missing_evidence: list[str]`
  - `spurious_claims: list[str]`
- `ReflectionEntry`:
  - `attempt_id: int`
  - `failure_reason: str`
  - `lesson: str`
  - `next_strategy: str`

## 4. Hoan thien prompt trong src/reflexion_lab/prompts.py

Dien 3 system prompt:

- `ACTOR_SYSTEM`: tra loi final answer ro rang, dung context.
- `EVALUATOR_SYSTEM`: bat buoc tra ve JSON hop le theo dung field cua `JudgeResult`.
- `REFLECTOR_SYSTEM`: phan tich sai o attempt truoc, de xuat chien luoc moi theo dung field cua `ReflectionEntry`.

Khuyen nghi: voi Evaluator va Reflector, yeu cau model "chi tra JSON, khong them van ban ngoai JSON".

## 5. Thay logic mock bang goi LLM that

Hien tai `agents.py` dang goi:

- `actor_answer(...)`
- `evaluator(...)`
- `reflector(...)`

Tu `src/reflexion_lab/mock_runtime.py`.

Ban co 2 lua chon:

1. Viet lai noi dung cac ham trong `mock_runtime.py` de goi endpoint that.
2. Tao file runtime moi (vi du: `ollama_runtime.py`) roi doi import trong `agents.py`.

De an toan va it thay doi, nen giu nguyen chu ky ham (function signature).

## 6. Cach goi endpoint OpenAI-compatible

Mau chung:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url=os.getenv("LLM_LINK"),
    api_key="ollama",
)

resp = client.chat.completions.create(
    model=os.getenv("LLM_MODEL", "qwen2.5:7b"),
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=0,
)

text = resp.choices[0].message.content
usage = resp.usage
```

## 7. Token va latency that (khong dung estimate)

Trong moi attempt:

- Do latency bang `time.perf_counter()` truoc/sau API call.
- Token that:
  - `prompt_tokens = resp.usage.prompt_tokens`
  - `completion_tokens = resp.usage.completion_tokens`
  - `total_tokens = resp.usage.total_tokens`

Cap nhat lai `AttemptTrace` trong `agents.py` bang so lieu that.

## 8. Cap nhat report mode

Trong `run_benchmark.py`, thay `mode="mock"` thanh mode that, vi du:

- `mode="ollama_remote"` hoac `mode="real_llm"`

## 9. Chay kiem thu tung buoc

Smoke test:

```bash
python test_llm.py
python run_benchmark.py --dataset data/hotpot_mini.json --out-dir outputs/ollama_colab_smoke
```

Autograde format:

```bash
python autograde.py --report-path outputs/ollama_colab_smoke/report.json
```

## 10. Chay benchmark that theo yeu cau lab

Sau khi smoke test on dinh:

- Repo nay da co san file `data/hotpot_100.json` gom 100 mau HotpotQA that voi ty le:
  - 30 `easy`
  - 40 `medium`
  - 30 `hard`
- Truoc khi chay, dam bao endpoint Ollama tren Colab con hoat dong. Neu tunnel het han hoac bi Cloudflare 1033 thi benchmark se fail ngay tu request dau tien.
- Chay test tong (toan bo 100 mau) bang dung duong dan dataset:

```bash
cd /home/tobiv/DaoTaoAI/VuHongQuang-track3-lab1-advanced-agent
/usr/bin/python3.11 run_benchmark.py --dataset data/hotpot_100.json --out-dir outputs/ollama_colab_100 --resume
```

- Script se tu dong chia thanh 3 muc do va tao report rieng:
  - `outputs/ollama_colab_100/easy/report.json`
  - `outputs/ollama_colab_100/medium/report.json`
  - `outputs/ollama_colab_100/hard/report.json`
- File log tien trinh testcase nam tai:
  - `outputs/ollama_colab_100/run.log`
- Trong log se co:
  - testcase dang chay (`RUN ... case=i/n qid=...`)
  - testcase da chay xong (`DONE ...`)
  - thong tin resume (`RESUME ... done=... pending=...`)

- Sau khi chay xong, kiem tra autograde cho tung muc:

```bash
/usr/bin/python3.11 autograde.py --report-path outputs/ollama_colab_100/easy/report.json
/usr/bin/python3.11 autograde.py --report-path outputs/ollama_colab_100/medium/report.json
/usr/bin/python3.11 autograde.py --report-path outputs/ollama_colab_100/hard/report.json
```

- Neu ban muon chay lai tu dau (bo qua resume):

```bash
/usr/bin/python3.11 run_benchmark.py --dataset data/hotpot_100.json --out-dir outputs/ollama_colab_100 --no-resume
```

- Ket qua dat yeu cau toi thieu cua buoc nay khi:
  - Co du report cho 3 muc: `easy`, `medium`, `hard` (ca `report.json` va `report.md`)
  - Co du `outputs/ollama_colab_100/run.log`
  - Autograde doc duoc cac file report ma khong loi format
- Neu ban gap loi `FileNotFoundError`, hay kiem tra lai ban da dung `--dataset data/hotpot_100.json` thay vi `--dataset hotpot_100.json`.
- Neu ban gap loi HTML/Cloudflare trong luc goi LLM, can khoi dong lai tunnel Colab roi chay lai benchmark.

## Checklist nhanh

- [ ] `test_llm.py` goi endpoint Colab thanh cong
- [ ] `schemas.py` khong con TODO
- [ ] `prompts.py` khong con placeholder
- [ ] Actor, Evaluator, Reflector deu goi LLM that
- [ ] Token/latency dung so lieu that tu response
- [ ] Report mode khong con `mock`
- [ ] Da chay `data/hotpot_100.json` thanh cong
- [ ] Chay duoc benchmark va autograde
