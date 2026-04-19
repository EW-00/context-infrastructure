#!/usr/bin/env python3
"""
L2 Reflector Agent (Trigger Script)
Instructs an OpenCode session to read observations, write reflection candidates, and perform limited GC.
"""
import os
import sys
from pathlib import Path
from opencode_client import OpenCodeClient
from datetime import datetime

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "docs" / "KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"

PROMPT_TEMPLATE = """
执行记忆系统的"反思与晋升"任务。

SOP: {kb_path}

步骤：
1. 读取 /contexts/memory/OBSERVATIONS.md，分析 🔴 和高优 🟡 条目
2. 将具有普适性的稳定模式先写入候选层，而不是直接修改 rules/：
   - contexts/reflection/skill_candidates.md: 技术方法论、工作流、最佳实践
   - contexts/reflection/axiom_candidates.md: 更抽象的判断原则或长期决策模式
   - contexts/reflection/sync_candidates.md: 可能值得跨机器共享、但仍需人工审核的内容
3. 只在候选层和明确过期的低价值观测层面执行 GC。不要直接改写 rules/ 下的任何文件。

晋升门槛：跨项目通用 + 多次验证 + 有明确适用场景
完成后回复简短汇报，说明写入了哪些 candidates，以及是否清理了明显过期的 OBSERVATIONS 条目。
"""

def main():
    import argparse
    parser = argparse.ArgumentParser(description='L2 Reflector Agent')
    parser.add_argument('--model', default='openai/gpt-5.4',
                        help='Model ID to use')
    args = parser.parse_args()
    
    model_id = args.model
    target_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Triggering Fully Agentic Reflector using model: {model_id}...")
    client = OpenCodeClient()
    
    session_id = client.create_session(f"Heartbeat L2 Reflector - {target_date}")
    if not session_id:
        return
        
    prompt = PROMPT_TEMPLATE.format(kb_path=KNOWLEDGE_BASE)
    client.send_message(session_id, prompt, model_id=model_id)
    # If send_message timed out, agent may still be running; poll until done
    print("Waiting for session to complete (sync mode)...")
    client.wait_for_session_complete(session_id)
    print(f"Task complete (Session: {session_id}).")

if __name__ == "__main__":
    main()
