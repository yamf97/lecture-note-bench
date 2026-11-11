#!/usr/bin/env python3
"""OpenAI 호환 게이트웨이(Vercel AI Gateway 등)에 프롬프트 파일을 보내고 결과를 저장한다.

    python3 tools/run_gateway.py --list [substr]                      # 모델 ID 목록
    python3 tools/run_gateway.py --model openai/gpt-oss-120b \
        --prompt docs/experiments/…prompt2-directive.md --out docs/experiments/bench/A-2.md \
        [--reasoning medium] [--base-url https://ai-gateway.vercel.sh/v1]

- 키는 base-url의 호스트에 맞는 환경변수 또는 ~/.config/<게이트웨이>/key 에서만 읽고, 값을 출력하지 않는다 (전역 §5.6).
  Vercel: AI_GATEWAY_API_KEY / ~/.config/ai-gateway/key · OpenRouter: OPENROUTER_API_KEY / ~/.config/openrouter/key
- 프롬프트 파일에 `=====` 줄이 두 개 있으면 그 사이만 보낸다. 없으면 전체.
- 표준 라이브러리만 쓴다.
- reasoning 파라미터 이름은 제공자마다 다르다 [원문 미확인]: 먼저 OpenAI식 `reasoning_effort`,
  400이면 OpenRouter식 `reasoning: {effort}` 로 재시도한다. 어느 쪽이 먹혔는지 결과 머리말에 적는다.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_BASE = "https://ai-gateway.vercel.sh/v1"

# 게이트웨이별 키 — 환경변수가 우선, 없으면 파일. 값은 절대 출력하지 않는다.
GATEWAYS = {
    "ai-gateway.vercel.sh": ("AI_GATEWAY_API_KEY", "~/.config/ai-gateway/key"),
    "openrouter.ai": ("OPENROUTER_API_KEY", "~/.config/openrouter/key"),
}
_BASE = DEFAULT_BASE


def key():
    host = _BASE.split("//", 1)[-1].split("/", 1)[0]
    env, path = GATEWAYS.get(host, ("AI_GATEWAY_API_KEY", "~/.config/ai-gateway/key"))
    path = os.path.expanduser(path)
    k = os.environ.get(env)
    if not k and os.path.exists(path):
        k = open(path, encoding="utf-8").read().strip()
    if not k:
        sys.exit(f"키가 없다. 환경변수 {env} 또는 파일 {path} (chmod 600).")
    return k


def call_stream(base, body, timeout=1800):
    """stream: true 로 보내고 SSE 조각을 모아 (status, 합친 응답 dict) 로 돌려준다.
    긴 생성에서 비스트리밍 연결이 끊기는 것을 피한다."""
    body = {**body, "stream": True, "stream_options": {"include_usage": True}}
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json"},
        method="POST",
    )
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {"error": str(e)}
    content, finish, usage = [], None, {}
    with r:
        for raw in r:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            for ch in chunk.get("choices", []):
                delta = ch.get("delta", {}).get("content")
                if delta:
                    content.append(delta)
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
            if chunk.get("usage"):
                usage = chunk["usage"]
    return 200, {"choices": [{"message": {"content": "".join(content)}, "finish_reason": finish}], "usage": usage}


def call(base, path, body=None, timeout=900):
    req = urllib.request.Request(
        base.rstrip("/") + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": "Bearer " + key(),
            "Content-Type": "application/json",
        },
        method="POST" if body is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read())
        except Exception:
            payload = {"error": str(e)}
        return e.code, payload


def list_models(base, substr):
    st, data = call(base, "/models")
    if st != 200:
        sys.exit(f"models 실패 {st}: {json.dumps(data)[:300]}")
    ids = sorted(m.get("id", "") for m in data.get("data", []))
    for i in ids:
        if not substr or substr.lower() in i.lower():
            print(i)


def prompt_body(path):
    text = open(path, encoding="utf-8").read()
    parts = text.split("\n=====\n")
    if len(parts) >= 3:
        return parts[1].strip() + "\n"
    return text


def run(base, model, prompt_path, out_path, reasoning, stream=False):
    prompt = prompt_body(prompt_path)
    msgs = [{"role": "user", "content": prompt}]
    attempts = []
    if reasoning:
        attempts.append(("reasoning_effort", {"reasoning_effort": reasoning}))
        attempts.append(("reasoning.effort", {"reasoning": {"effort": reasoning}}))
    attempts.append(("none", {}))

    for name, extra in attempts:
        body = {"model": model, "messages": msgs, **extra}
        t0 = time.time()
        st, data = call_stream(base, body) if stream else call(base, "/chat/completions", body)
        dt = time.time() - t0
        if st == 200:
            break
        print(f"[{model}] {name}: HTTP {st} — {json.dumps(data)[:200]}", file=sys.stderr)
    else:
        sys.exit(f"[{model}] 모든 시도 실패")

    choice = data["choices"][0]
    content = choice["message"].get("content") or ""
    usage = data.get("usage", {})
    header = (
        "<!-- run_gateway.py\n"
        f"  model: {model}\n"
        f"  reasoning: {reasoning or '(없음)'} via {name}{' (stream)' if stream else ''}\n"
        f"  prompt: {prompt_path}\n"
        f"  elapsed_s: {dt:.1f}\n"
        f"  usage: {json.dumps(usage)}\n"
        f"  finish_reason: {choice.get('finish_reason')}\n"
        f"  date: {time.strftime('%Y-%m-%d %H:%M')}\n"
        "-->\n\n"
    )
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + content)
    print(f"ok {out_path} — {dt:.0f}s, tokens {usage.get('prompt_tokens')}/{usage.get('completion_tokens')}, reasoning via {name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--list", nargs="?", const="", metavar="SUBSTR")
    ap.add_argument("--model")
    ap.add_argument("--prompt")
    ap.add_argument("--out")
    ap.add_argument("--reasoning", default="medium")
    ap.add_argument("--stream", action="store_true", help="SSE 스트리밍으로 받는다 (긴 생성용)")
    a = ap.parse_args()
    global _BASE
    _BASE = a.base_url

    if a.list is not None:
        return list_models(a.base_url, a.list)
    if not (a.model and a.prompt and a.out):
        ap.error("--model --prompt --out 이 모두 필요하다 (또는 --list)")
    run(a.base_url, a.model, a.prompt, a.out, a.reasoning, a.stream)


if __name__ == "__main__":
    main()
