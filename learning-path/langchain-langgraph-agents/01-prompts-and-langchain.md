# Lesson 1 - Prompts and LangChain

> 45-75 minutes - Make the data flow visible before adding a model.

**Goal:** build a prompt and compose two steps using LangChain's runnable interface.

**Prerequisites:** Python functions, dictionaries, and the [track setup](README.md#setup).

**Focus:** frameworks connect components; they do not replace understanding each component's input and output.

---

## The vocabulary

| Term | Meaning |
|---|---|
| Language model | A model that processes and generates language |
| Chat message | Content with a role such as system, human, or assistant |
| Prompt template | A reusable message structure with named input slots |
| Runnable | A component with a standard way to invoke it |
| Chain | Connected components passing outputs to subsequent inputs |
| Context | Information supplied for the current model response |

A prompt can guide a model's behavior, but it does not guarantee correctness. Check outputs against evidence and requirements.

## Python example - An offline composition

This complete script needs the installed framework but no API key or network call.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

prompt = ChatPromptTemplate.from_messages([
    ("system", "Explain {topic} to a beginner. Keep the answer concrete."),
    ("human", "{question}"),
])

def offline_reply(prompt_value):
    messages = prompt_value.to_messages()
    return "OFFLINE MOCK received: " + messages[-1].content

pipeline = prompt | RunnableLambda(offline_reply)
inputs = {
    "topic": "breadth-first search",
    "question": "Why does BFS use a queue?",
}

formatted = prompt.invoke(inputs)
for message in formatted.to_messages():
    print(message.type, ":", message.content)
print(pipeline.invoke(inputs))
```

**Expected:** the printed system message contains "breadth-first search", and the final line is:

```text
OFFLINE MOCK received: Why does BFS use a queue?
```

The `|` operator connects runnables. The prompt turns a dictionary into a prompt value; the function receives that prompt value and returns a string.

This function echoes input. It does not understand BFS and is not an LLM. Its purpose is to make composition testable before introducing variable model responses.

## Replacing the mock later

A compatible chat model can occupy the next step in the pipeline. Its response is usually a message object rather than a plain string, so inspect the output type instead of assuming every component returns text.

The [optional model-backed example](05-ai-agents.md#optional---a-model-driven-agent) documents provider setup separately. You can complete the core track without it.

## Exercises

1. Change the topic to PyTorch and the human question to "What is a tensor?"
2. Leave out `topic`. Read the error and identify the missing input.
3. Add a required `audience` variable to the system template.
4. Replace the mock with a function that reports how many messages it received.

**Hints:** print the dictionary before invoking the prompt, then print the message objects. Debug one boundary at a time.

## Common mistakes

- Assuming a prompt variable is filled automatically from Python scope.
- Treating a deterministic mock's success as proof that a model will answer correctly.
- Connecting components without checking their expected types.

## Checkpoint

- [ ] I can trace dictionary -> prompt value -> function result.
- [ ] I can distinguish message roles and template variables.
- [ ] I can explain what the offline example does without calling it an AI model.

Reference: [LangChain models and message interfaces](https://docs.langchain.com/oss/python/langchain/models).

Next: [Tool calling](02-tool-calling.md). [Track index](README.md) | [Progress](progress.md).
