# Lesson 2 - Tool Calling

> 45-75 minutes - Separate a request to call a tool from executing it.

**Goal:** define a typed tool, validate its inputs, and invoke it.

**Prerequisites:** [prompts and composition](01-prompts-and-langchain.md), type hints, and exceptions.

**Focus:** the model can propose a tool name and arguments. Application code executes the function.

---

## The round trip

A typical model/tool interaction is:

1. The application gives the model tool descriptions and input schemas.
2. The model returns a tool-call request.
3. The application checks the request and executes the permitted tool.
4. A tool-result message, linked to that call, goes back to the model.
5. The model can answer or request another tool.

A function with a tool decorator is callable without a model. Direct invocation is a good first check.

## Python example - A validated study-time tool

Save this complete block as `study_tools.py` in your practice directory. Later examples import the tool.

```python
from langchain.tools import tool
from pydantic import BaseModel, ConfigDict, Field, ValidationError

class StudyEstimate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lessons: int = Field(ge=1, le=20, strict=True)
    minutes_per_lesson: int = Field(default=45, ge=5, le=120, strict=True)

@tool(args_schema=StudyEstimate)
def estimate_study_time(lessons: int, minutes_per_lesson: int = 45) -> str:
    """Estimate total study minutes for a small set of lessons."""
    return f"{lessons * minutes_per_lesson} minutes"

if __name__ == "__main__":
    print(estimate_study_time.name)
    print(estimate_study_time.invoke({"lessons": 3}))
    try:
        estimate_study_time.invoke({"lessons": 0})
    except ValidationError:
        print("Invalid lesson count rejected.")
```

**Expected:** the tool name, `135 minutes`, and `Invalid lesson count rejected.`

The docstring describes the tool's purpose. The schema describes required fields, defaults, and allowed ranges. Strict integer fields reject strings such as `"3"`; extra fields are also rejected.

## What the schema does and does not prove

The schema checks structure and numeric boundaries. It cannot determine whether the user meant three lessons or five, or whether an action is authorized.

This tool only calculates a number. For a tool that changes something, keep the actual permission check in application code and make its behavior explicit. A model's proposed arguments are inputs to check.

When assembling a model/tool conversation yourself, tool-call identifiers connect results to requests. Higher-level agent helpers handle that message protocol, but you still need to understand the boundary.

## Exercises

1. Set `minutes_per_lesson` to 30 and predict the output for three lessons.
2. Try zero, a negative number, `"3"`, and an unexpected argument. Explain the rejection.
3. Add a new read-only tool that converts minutes to hours.
4. Explain why attaching a tool description to a model does not execute the Python function.

**Hints:** call `.invoke({...})` with a dictionary. Keep conversion and validation rules explicit instead of assuming the model will supply the right types.

## Common mistakes

- Calling a tool because the model named it, without checking the allowed tool registry.
- Treating type annotations alone as runtime validation.
- Confusing a tool result with the model's final answer.
- Silently catching an error and reporting a successful calculation.

## Checkpoint

- [ ] I can define and directly invoke a tool.
- [ ] I can explain validation errors.
- [ ] I can identify who proposes a call, who executes it, and how the result returns.

Reference: [LangChain tool documentation](https://docs.langchain.com/oss/python/langchain/tools).

Previous: [Prompts](01-prompts-and-langchain.md). Next: [Retrieval and RAG](03-retrieval-and-rag.md). [Track index](README.md) | [Progress](progress.md).
