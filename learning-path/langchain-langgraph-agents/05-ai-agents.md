# Lesson 5 - AI Agents

> 60-90 minutes - Understand the loop offline before trying a hosted model.

**Goal:** distinguish a scripted workflow from a model-driven agent and inspect a bounded tool loop.

**Prerequisites:** [tool calling](02-tool-calling.md) and [LangGraph workflows](04-langgraph-workflows.md).

**Focus:** an agent uses a model to choose actions, observes tool results, and continues until it answers or reaches a limit.

---

## Workflow versus agent

In the previous lesson, code chose a branch based on whether retrieval found passages. In a model-driven agent, a model can decide whether to retrieve, calculate, or answer.

That flexibility adds uncertainty. Useful checks include correct tool choice, validated arguments, correct interpretation of results, and termination.

## Python example - An offline loop simulator

Save [lesson 2](02-tool-calling.md)'s example as `study_tools.py`, then run this complete block from the same practice directory.

```python
from study_tools import estimate_study_time

tools = {estimate_study_time.name: estimate_study_time}

def scripted_planner(observations):
    if not observations:
        return {
            "type": "tool",
            "name": "estimate_study_time",
            "args": {"lessons": 3, "minutes_per_lesson": 45},
        }
    return {"type": "final", "answer": observations[-1]}

def run_loop(planner, max_tool_calls=2):
    observations = []
    tool_calls = 0
    for _ in range(5):
        decision = planner(observations)
        if decision["type"] == "final":
            return decision["answer"]
        if decision["type"] != "tool":
            raise ValueError("Unknown decision type.")
        if tool_calls >= max_tool_calls:
            raise RuntimeError("Tool-call limit reached.")
        if decision["name"] not in tools:
            raise ValueError("Requested tool is not allowed.")

        result = tools[decision["name"]].invoke(decision["args"])
        observations.append(result)
        tool_calls += 1

    raise RuntimeError("Step limit reached.")

print(run_loop(scripted_planner))
```

**Expected:** `135 minutes`.

The planner is a fixed Python rule, not an AI model. These dictionaries simulate decisions and observations; they are not the actual chat-model tool-message protocol. The example makes the execution boundary and limits easy to inspect.

## Optional - A model-driven agent

This extension makes hosted API calls and may incur provider charges. The rest of the track works without it.

Install the additional provider package:

```powershell
python -m pip install langchain-anthropic
```

Set `ANTHROPIC_API_KEY` locally and `ANTHROPIC_MODEL` to a tool-capable model ID available in your account. For PowerShell 7, you can enter them for the current terminal session:

```powershell
$env:ANTHROPIC_API_KEY = Read-Host "API key" -MaskInput
$env:ANTHROPIC_MODEL = Read-Host "Tool-capable model ID"
```

Save the following as `hosted_agent.py`, beside `study_tools.py`. The project can import its builder without running the demo.

```python
import os
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langgraph.errors import GraphRecursionError

def build_agent(tools, system_prompt):
    if not os.environ.get("ANTHROPIC_API_KEY") or not os.environ.get("ANTHROPIC_MODEL"):
        raise RuntimeError("Set ANTHROPIC_API_KEY and ANTHROPIC_MODEL first.")
    model = ChatAnthropic(
        model=os.environ["ANTHROPIC_MODEL"],
        max_tokens=512,
        timeout=30,
        max_retries=1,
    )
    return create_agent(
        model=model, tools=tools, system_prompt=system_prompt
    )

if __name__ == "__main__":
    from study_tools import estimate_study_time

    agent = build_agent(
        [estimate_study_time],
        "Use the study-time tool for calculations. Keep the answer brief.",
    )
    try:
        result = agent.invoke(
            {"messages": [{
                "role": "user",
                "content": "How many minutes for 3 lessons at 45 minutes each?",
            }]},
            config={"recursion_limit": 10},
        )
        for message in result["messages"]:
            print(message.type, message.content)
            if getattr(message, "tool_calls", None):
                print("Requested calls:", message.tool_calls)
    except GraphRecursionError:
        print("Agent stopped because it exceeded the graph-step limit.")
```

**Expected behavior:** inspect whether the model actually requested the tool, whether the result was 135 minutes, and whether it ended with a supported answer. The exact messages and tool decisions vary. A final correct number alone does not prove tool use.

The step limit is not an exact tool-call or spending cap. Record model calls and usage when comparing actual agents. Keep keys in the local environment, not notes or source files.

## Exercises

1. Change the offline planner to request an unknown tool. Confirm rejection.
2. Make it request a tool forever. Confirm that the tool-call limit stops it.
3. Request an invalid lesson count and inspect the schema error.
4. If you try the hosted extension, compare five repeated runs for tool use, answer correctness, and termination.

**Hints:** keep exceptions visible while learning. A tool error and a successful result should not be indistinguishable in your observations.

## Checkpoint

- [ ] I can distinguish an offline loop simulation from a model-driven agent.
- [ ] I can locate schema validation and allowed-tool checks.
- [ ] I can explain why tool use needs evaluation as well as a stopping rule.

References: [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents), [ChatAnthropic integration](https://docs.langchain.com/oss/python/integrations/chat/anthropic).

Previous: [LangGraph](04-langgraph-workflows.md). Next: [Notes-assistant project](mini-project.md). [Track index](README.md) | [Progress](progress.md).
