# refine-prompt

Takes your rough prompt and returns a clearer one for an agent: better grammar, structure and order, with your intent, scope and wording kept. It does not run the prompt and adds no new requirements; ideas it has go in a separate list for you to accept or not.

```mermaid
flowchart TD
    IN["Your raw prompt"] --> I["Read for intent:<br/>what you want, constraints, done means"]
    I --> Q{"Ambiguity that would change<br/>what the agent does?"}
    Q -- yes --> A["Asks at most 3 questions,<br/>each with a recommended answer"]
    A --> I
    Q -- no --> R["Refine: grammar, order, concrete references;<br/>at most 1.5x the original length"]
    R --> F["Fidelity check:<br/>remove anything you did not ask for"]
    F --> OUT["Intent lines + refined prompt +<br/>up to 5 changes explained"]
```

| | |
|---|---|
| **Input** | A raw prompt, from you or a draft. |
| **Output** | Three parts in chat: the intent as understood, the refined prompt in one paste-ready block, and the changes and assumptions. |
| **Your files** | None; the original prompt is untouched and nothing is executed. |

- **Status:** experimental (2026-10-07); one manual run, formal evals pending.
