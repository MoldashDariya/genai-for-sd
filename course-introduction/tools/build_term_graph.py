"""
Builds the term relationship graph for the Course Introduction assignment.

Reads genai-applications-report.md, counts how often every glossary term is used:
  - explicit mention: the term itself or its abbreviation (e.g. "RAG", "LLM");
  - implicit mention: the idea is used without the term (e.g. "invents a policy" -> hallucination).
Two terms are related when they are used in the same section of the report;
the weight of the relation is the number of such sections.

Output (next to the report):
  term-graph.html   - interactive SVG graph + table of counts
  term-mentions.md  - the same counts as a Markdown table

Standard library only:  python3 tools/build_term_graph.py
"""
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "genai-applications-report.md"

# term -> (category, explicit pattern, implicit pattern)
# Explicit mentions of ALL terms are masked before implicit patterns are searched,
# so one word is never counted twice.
TERMS = {
    "Generative AI": ("concept", r"generative ai|\bgenai\b", r"ai-generated|generated content|creates? (texts|content)"),
    "LLM": ("concept", r"large language models?|\bllms?\b", r"\b(the|a|this) model\b|language model"),
    "Token": ("concept", r"\btokens?\b", r"pieces? of text"),
    "Context window": ("concept", r"context window", r"does not fit|do not fit|fit completely|amount of text the model can"),
    "Prompt engineering": ("technique", r"prompt engineering", r"carefully designed|clear instructions"),
    "Prompt injection": ("risk", r"prompt injection", r"manipulated|new attacks|malicious"),
    "Prompt": ("concept", r"\bprompts?\b", r"instruct\w*|natural language"),
    "Hallucination": ("risk", r"hallucinat\w*",
                      r"invents?\b|invented|looks correct but|confidently gives a wrong|do(es)? not exist|never said|wrong explanations"),
    "RAG": ("technique", r"retrieval-augmented generation|\brag\b",
            r"retriev\w*|find the answer in|answers? from|grounded in sources|based only on"),
    "Embedding": ("technique", r"embeddings?", r"most similar|similar by meaning"),
    "Vector database": ("technique", r"vector databases?", r"\bindex(ed|ing)?\b"),
    "Fine-tuning": ("technique", r"fine-tun\w*", r"retrain\w*"),
    "Inference": ("concept", r"\binference\b", r"fraction of a second|computing power|instantly"),
    "Agentic workflow": ("agents", r"agentic workflows?", r"\bplan(s|ning)?\b|many steps|repeats?\b|until the task"),
    "AI agent": ("agents", r"ai agents?|\bagents?\b", r"by itself|autonomous|whole tasks"),
    "Tool calling": ("agents", r"tool calling|tool use",
                     r"use tools|runs? commands|executes real commands|through apis|integrations?"),
    "Copilot": ("agents", r"copilots?", r"assistants?\b|suggest\w*"),
    "Multimodal model": ("technique", r"multimodal", r"images?\b|video|voice|speech"),
    "Guardrails": ("risk", r"guardrails?", r"filters?|prevent the bot|limits on"),
    "Human-in-the-loop": ("risk", r"human-in-the-loop",
                          r"review\w*|to a person|doctor (checks|must)|in control|signs it"),
}

CATEGORY_COLORS = {
    "concept": "#4f6bd8",
    "technique": "#1a9e77",
    "agents": "#d97706",
    "risk": "#d1435b",
}


def load_sections(text):
    """Splits the report into sections by '## ' headings; URLs are removed."""
    text = re.sub(r"https?://\S+", " ", text)
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    sections = []
    for i, part in enumerate(parts):
        title = "Header" if i == 0 else part.splitlines()[0].strip()
        sections.append((title, part if i == 0 else part[len(part.splitlines()[0]):]))
    return sections


def count_section(body):
    """Returns {term: (explicit, implicit)} for one section."""
    masked = body.lower()
    explicit = {}
    # Longer explicit patterns first ("prompt injection" before "prompt").
    for term, (_, pattern, _) in sorted(TERMS.items(), key=lambda kv: -len(kv[1][1])):
        found = re.findall(pattern, masked)
        explicit[term] = len(found)
        masked = re.sub(pattern, lambda m: " " * len(m.group(0)), masked)
    result = {}
    for term, (_, _, implicit_pattern) in TERMS.items():
        implicit = len(re.findall(implicit_pattern, masked))
        result[term] = (explicit[term], implicit)
    return result


def analyse():
    sections = load_sections(REPORT.read_text(encoding="utf-8"))
    totals = {t: [0, 0] for t in TERMS}
    presence = {t: set() for t in TERMS}
    for index, (_, body) in enumerate(sections):
        for term, (exp, imp) in count_section(body).items():
            totals[term][0] += exp
            totals[term][1] += imp
            if exp + imp:
                presence[term].add(index)
    edges = []
    names = list(TERMS)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            weight = len(presence[a] & presence[b])
            if weight >= 2:
                edges.append((a, b, weight))
    return totals, presence, edges, len(sections)


def write_markdown(totals, presence):
    rows = sorted(TERMS, key=lambda t: -(totals[t][0] + totals[t][1]))
    lines = [
        "# Term mentions in the report",
        "",
        "Generated by `tools/build_term_graph.py` from `genai-applications-report.md`.",
        "",
        "- **Explicit** - the term or its abbreviation is written in the text.",
        "- **Implicit** - the idea is used without naming the term (for example *\"invents a policy\"* → Hallucination).",
        "",
        "| Term | Explicit | Implicit | Total | Sections |",
        "|---|---:|---:|---:|---:|",
    ]
    for t in rows:
        e, i = totals[t]
        lines.append(f"| {t} | {e} | {i} | {e + i} | {len(presence[t])} |")
    (ROOT / "term-mentions.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_html(totals, presence, edges, section_count):
    # Wide margins so that labels on the left and right sides fit inside the picture.
    size, center, radius = 1000, 500, 330
    names = sorted(TERMS, key=lambda t: (list(CATEGORY_COLORS).index(TERMS[t][0]), t))
    pos = {}
    for k, t in enumerate(names):
        angle = 2 * math.pi * k / len(names) - math.pi / 2
        pos[t] = (center + radius * math.cos(angle), center + radius * math.sin(angle))
    max_total = max(sum(v) for v in totals.values()) or 1
    max_weight = max((w for *_, w in edges), default=1)

    svg = [f'<svg viewBox="0 0 {size} {size}" role="img" aria-label="Term relationship graph">']
    for a, b, w in sorted(edges, key=lambda e: e[2]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        svg.append(f'<line class="edge" data-a="{html.escape(a)}" data-b="{html.escape(b)}" '
                   f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke-width="{0.6 + 3.4 * w / max_weight:.2f}" '
                   f'stroke-opacity="{0.12 + 0.5 * w / max_weight:.2f}">'
                   f'<title>{html.escape(a)} — {html.escape(b)}: together in {w} sections</title></line>')
    for t in names:
        x, y = pos[t]
        e, i = totals[t]
        r = 9 + 22 * math.sqrt((e + i) / max_total)
        color = CATEGORY_COLORS[TERMS[t][0]]
        anchor = "start" if x > center + 5 else "end" if x < center - 5 else "middle"
        dx = (r + 6) * (1 if anchor == "start" else -1 if anchor == "end" else 0)
        dy = 4 if anchor != "middle" else (-(r + 8) if y < center else r + 16)
        svg.append(f'<g class="node" data-term="{html.escape(t)}" tabindex="0">'
                   f'<title>{html.escape(t)}: {e} explicit, {i} implicit</title>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/>'
                   f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{html.escape(t)} '
                   f'<tspan class="muted">{e}+{i}</tspan></text></g>')
    svg.append("</svg>")

    rows = "".join(
        f"<tr><td><span class='dot' style='background:{CATEGORY_COLORS[TERMS[t][0]]}'></span>{html.escape(t)}</td>"
        f"<td>{totals[t][0]}</td><td>{totals[t][1]}</td><td>{sum(totals[t])}</td><td>{len(presence[t])}</td></tr>"
        for t in sorted(TERMS, key=lambda t: -sum(totals[t])))
    legend = "".join(f"<span><span class='dot' style='background:{c}'></span>{k}</span>"
                     for k, c in CATEGORY_COLORS.items())

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GenAI Term Graph</title>
<style>
:root {{ --bg:#fbfbfd; --fg:#1d1f24; --muted:#6b7080; --line:#9aa0b4; --card:#ffffff; --border:#e3e5ec; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#14161b; --fg:#e8e9ee; --muted:#9a9fb0; --line:#7c8297; --card:#1c1f26; --border:#2c303a; }} }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:15px/1.5 system-ui, -apple-system, sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:24px; margin:0 0 4px; }}
p {{ color:var(--muted); margin:4px 0 16px; }}
.layout {{ display:grid; grid-template-columns: minmax(0,1.4fr) minmax(0,1fr); gap:20px; align-items:start; }}
@media (max-width: 860px) {{ .layout {{ grid-template-columns: 1fr; }} }}
.card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:12px; }}
svg {{ width:100%; height:auto; display:block; }}
.edge {{ stroke:var(--line); transition: stroke-opacity .15s; }}
.node text {{ font-size:16px; fill:var(--fg); }}
.node circle {{ stroke:var(--card); stroke-width:2; cursor:pointer; }}
.muted {{ fill:var(--muted); }}
svg.focus .edge {{ stroke-opacity:.04 !important; }}
svg.focus .edge.on {{ stroke-opacity:.85 !important; stroke:var(--fg); }}
svg.focus .node {{ opacity:.25; }}
svg.focus .node.on {{ opacity:1; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th, td {{ padding:6px 8px; border-bottom:1px solid var(--border); text-align:right; }}
th:first-child, td:first-child {{ text-align:left; }}
.dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }}
.legend {{ display:flex; flex-wrap:wrap; gap:14px; font-size:13px; color:var(--muted); margin:8px 4px 0; }}
</style></head>
<body><main>
<h1>Relationships between GenAI terms</h1>
<p>Built automatically from <code>genai-applications-report.md</code> ({section_count} sections) by
<code>tools/build_term_graph.py</code>. Node size = total mentions, label = explicit + implicit.
A line connects two terms used together in at least 2 sections; thicker = more sections.
Hover or tap a term to highlight its connections.</p>
<div class="layout">
<div class="card">{''.join(svg)}<div class="legend">{legend}</div></div>
<div class="card"><table><thead><tr><th>Term</th><th>Explicit</th><th>Implicit</th><th>Total</th><th>Sections</th></tr></thead>
<tbody>{rows}</tbody></table></div>
</div>
</main>
<script>
const svg = document.querySelector('svg');
function focus(term) {{
  if (!term) {{ svg.classList.remove('focus'); return; }}
  svg.classList.add('focus');
  const linked = new Set([term]);
  svg.querySelectorAll('.edge').forEach(e => {{
    const on = e.dataset.a === term || e.dataset.b === term;
    e.classList.toggle('on', on);
    if (on) {{ linked.add(e.dataset.a); linked.add(e.dataset.b); }}
  }});
  svg.querySelectorAll('.node').forEach(n => n.classList.toggle('on', linked.has(n.dataset.term)));
}}
svg.querySelectorAll('.node').forEach(n => {{
  n.addEventListener('mouseenter', () => focus(n.dataset.term));
  n.addEventListener('focus', () => focus(n.dataset.term));
  n.addEventListener('click', ev => {{ ev.stopPropagation(); focus(n.dataset.term); }});
}});
svg.addEventListener('mouseleave', () => focus(null));
document.addEventListener('click', () => focus(null));
</script>
</body></html>
"""
    (ROOT / "term-graph.html").write_text(page, encoding="utf-8")


def main():
    totals, presence, edges, section_count = analyse()
    write_markdown(totals, presence)
    write_html(totals, presence, edges, section_count)
    for t in sorted(TERMS, key=lambda t: -sum(totals[t])):
        print(f"{t:20s} explicit={totals[t][0]:3d} implicit={totals[t][1]:3d} sections={len(presence[t])}")
    print(f"edges: {len(edges)}")


if __name__ == "__main__":
    main()
