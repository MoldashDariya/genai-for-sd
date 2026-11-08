# Course Introduction: GenAI Applications Research

Practical assignment of the Course Introduction module.

| File | Content |
|---|---|
| [`genai-applications-report.md`](genai-applications-report.md) | **Report** on 8 GenAI use cases: business value, technical challenges, weaknesses and real products (name, link, description) for each |
| [`glossary.md`](glossary.md) | **Glossary**: 20 GenAI terms from the report, explained in my own words |
| [`term-graph.png`](term-graph.png) · [`term-graph.html`](term-graph.html) | **Term relationship graph** (optional task): how often each term is used in the report, explicitly and implicitly, and which terms appear together |
| [`term-mentions.md`](term-mentions.md) | The same counts as a table |
| [`tools/build_term_graph.py`](tools/build_term_graph.py) | Script that builds the graph and the table from the report automatically |

## Term relationship graph

![Term relationship graph](term-graph.png)

- **Explicit mention**: the term or its abbreviation is written in the text (*"RAG"*, *"LLM"*).
- **Implicit mention**: the idea is used without naming the term
  (*"the bot invents a policy that does not exist"* → Hallucination, *"a person reviews the result"* → Human-in-the-loop).
  Explicit matches are masked first, so one phrase is never counted twice.
- Two terms are connected when they are used in the same section of the report (at least 2 sections);
  a thicker line means more shared sections.

The interactive version is `term-graph.html`: download it and open it in a browser, then hover over a term
to highlight its connections.

## Rebuild

```bash
python3 tools/build_term_graph.py
```

Python 3.9+, standard library only.
