// TriggerMap review page: highlights, editable checklist, save and export.
// Every node is built with createElement/textContent: advisory text is never parsed as HTML.
(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("payload").textContent);
  const state = structuredClone(data.state);
  const reasons = data.reasons || {};
  const text = data.text;
  let mode = data.mode;
  let reviewId = data.review_id;
  let pendingKey = null; // reused when a save is retried, so retries never duplicate
  let nextHuman = 1;
  const QUESTIONS = {
    CONFIGURATION: "Does your configuration match this?",
    USAGE: "Does your application do this?",
    ACCESS: "Could an attacker have this access?",
    PLATFORM: "Does your environment match this?",
  };
  const ROLE_HEADINGS = {
    REQUIRED: "Required for exposure",
    EXCEPTION: "Not exposed if",
    NOT_REQUIRED: "Explicitly not required",
    UNCERTAIN: "Role unclear: review",
  };
  const GROUP_HEADINGS = {
    ALL: "All of these must hold",
    ANY: "Any one of these is enough",
    UNRESOLVED: "Related conditions: logic unclear",
  };

  const el = (tag, props = {}, children = []) => {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props)) {
      if (key === "text") node.textContent = value;
      else if (key === "dataset") Object.assign(node.dataset, value);
      else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value);
    }
    for (const child of children) node.append(child);
    return node;
  };
  const surface = (c) => text.slice(c.span[0], c.span[1]);
  const status = (message, isError = false) => {
    const line = document.getElementById("status-line");
    line.hidden = !message;
    line.textContent = message || "";
    line.classList.toggle("error", isError);
  };

  // -- highlights in the advisory text
  const segments = [...document.querySelectorAll(".seg")];
  function renderMarks() {
    const ordered = [...state.conditions].sort((a, b) => a.span[0] - b.span[0]);
    for (const seg of segments) {
      const start = Number(seg.dataset.start);
      const end = Number(seg.dataset.end);
      seg.replaceChildren();
      let cursor = start;
      for (const c of ordered) {
        const [s, e] = c.span;
        if (e <= start || s >= end) continue;
        if (s > cursor) seg.append(document.createTextNode(text.slice(cursor, s)));
        seg.append(
          el("mark", {
            id: `mark-${c.id}`,
            class: c.category.toLowerCase(),
            dataset: { cond: c.id },
            text: text.slice(Math.max(s, start), Math.min(e, end)),
            onclick: () => focusItem(c.id),
          }),
        );
        cursor = Math.min(e, end);
      }
      if (cursor < end) seg.append(document.createTextNode(text.slice(cursor, end)));
    }
  }
  function focusMark(id) {
    const mark = document.getElementById(`mark-${id}`);
    if (!mark) return;
    mark.scrollIntoView({ behavior: "smooth", block: "center" });
    mark.classList.remove("flash");
    void mark.offsetWidth;
    mark.classList.add("flash");
  }
  function focusItem(id) {
    const item = document.querySelector(`.item[data-cond="${CSS.escape(id)}"]`);
    if (!item) return;
    item.scrollIntoView({ behavior: "smooth", block: "center" });
    item.classList.add("active");
    setTimeout(() => item.classList.remove("active"), 1600);
  }

  // -- checklist
  const select = (options, value, onchange) =>
    el("select", { onchange: (e) => onchange(e.target.value) },
      options.map((o) => {
        const option = el("option", { value: o, text: o.replace("_", " ") });
        if (o === value) option.selected = true;
        return option;
      }));

  function itemNode(c) {
    const flags = reasons[c.id] || [];
    const answers = el("div", { class: "answers", role: "radiogroup", "aria-label": `Answer for ${c.id}` },
      ["PRESENT", "ABSENT", "UNKNOWN"].map((value) => {
        const input = el("input", { type: "radio", name: `answer-${c.id}`, value,
          onchange: () => { c.answer = value; } });
        if (c.answer === value) input.checked = true;
        return el("label", {}, [input, el("span", { text: value[0] + value.slice(1).toLowerCase() })]);
      }));
    const top = el("div", { class: "top" }, [
      el("input", { type: "checkbox", class: "pick", "aria-label": `Select ${c.id} for grouping`, dataset: { cond: c.id } }),
      Object.assign(select(data.labels.categories, c.category, (v) => { c.category = v; render(); }),
        { className: `chip-select ${c.category.toLowerCase()}`, title: "Category" }),
      Object.assign(select(data.labels.roles, c.role, (v) => { c.role = v; render(); }), { title: "Role" }),
      ...(c.source === "human" ? [el("span", { class: "human", text: "added by you" })] : []),
      ...(flags.length ? [el("span", { class: "flag", title: flags.join(", "), text: "review required" })] : []),
      el("span", { class: "grow" }),
      el("button", { type: "button", class: "remove", title: "Remove this condition", "aria-label": `Remove ${c.id}`,
        text: "×", onclick: () => removeCondition(c.id) }),
    ]);
    return el("div", { class: "item", dataset: { cond: c.id } }, [
      top,
      el("div", { class: "surface", text: `“${surface(c)}”`, onclick: () => focusMark(c.id) }),
      el("div", { class: "hint", text: QUESTIONS[c.category] }),
      ...(flags.length ? [el("div", { class: "hint", text: `Review: ${flags.map((f) => f.replace("_", " ")).join(", ")}` })] : []),
      answers,
    ]);
  }

  function renderChecklist() {
    const box = document.getElementById("items");
    box.replaceChildren();
    if (!state.conditions.length) {
      box.append(el("div", { class: "notice", text:
        "No explicit conditions found. This does not mean the conditions do not apply: the advisory may simply not state them." }));
    }
    const byId = Object.fromEntries(state.conditions.map((c) => [c.id, c]));
    const grouped = new Set();
    for (const g of state.groups) {
      const members = g.members.map((m) => byId[m]).filter(Boolean);
      members.forEach((m) => grouped.add(m.id));
      box.append(el("div", { class: "section group" }, [
        el("h4", {}, [el("span", { class: "op", text: g.operator }), document.createTextNode(GROUP_HEADINGS[g.operator])]),
        ...members.map(itemNode),
      ]));
    }
    for (const role of data.labels.roles) {
      const loose = state.conditions.filter((c) => !grouped.has(c.id) && c.role === role);
      if (loose.length) box.append(el("div", { class: "section" }, [el("h4", { text: ROLE_HEADINGS[role] }), ...loose.map(itemNode)]));
    }
    const counts = data.labels.roles.map((r) => `${state.conditions.filter((c) => c.role === r).length} ${r.toLowerCase().replace("_", " ")}`);
    document.getElementById("counts").textContent = counts.join(" · ");
  }

  function render() {
    state.groups = state.groups.filter((g) => g.members.length >= 2);
    renderMarks();
    renderChecklist();
  }

  // -- edits
  function removeCondition(id) {
    state.conditions = state.conditions.filter((c) => c.id !== id);
    state.groups.forEach((g) => { g.members = g.members.filter((m) => m !== id); });
    render();
  }

  function selectionOffsets() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return null;
    const segOf = (node) => (node.nodeType === 1 ? node : node.parentElement)?.closest(".seg");
    const seg = segOf(selection.anchorNode);
    if (!seg || seg !== segOf(selection.focusNode)) return { error: "Select text within one line of the advisory." };
    const offsetIn = (node, offset) => {
      const walker = document.createTreeWalker(seg, NodeFilter.SHOW_TEXT);
      let total = 0;
      while (walker.nextNode()) {
        if (walker.currentNode === node) return total + offset;
        total += walker.currentNode.textContent.length;
      }
      return null;
    };
    const a = offsetIn(selection.anchorNode, selection.anchorOffset);
    const b = offsetIn(selection.focusNode, selection.focusOffset);
    if (a === null || b === null) return { error: "Select plain advisory text." };
    let start = Number(seg.dataset.start) + Math.min(a, b);
    let end = Number(seg.dataset.start) + Math.max(a, b);
    while (start < end && /\s/.test(text[start])) start += 1;
    while (end > start && /\s/.test(text[end - 1])) end -= 1;
    if (start >= end) return { error: "The selection is empty." };
    if (text.slice(start, end).includes("\n")) return { error: "A condition must stay within one line." };
    return { start, end };
  }

  document.getElementById("add-selection").addEventListener("click", () => {
    const sel = selectionOffsets();
    if (!sel) return status("Select the condition's text in the advisory first.", true);
    if (sel.error) return status(sel.error, true);
    if (state.conditions.some((c) => sel.start < c.span[1] && sel.end > c.span[0])) {
      return status("That text overlaps an existing condition. Remove or change that one first.", true);
    }
    while (state.conditions.some((c) => c.id === `h${nextHuman}`)) nextHuman += 1;
    state.conditions.push({ id: `h${nextHuman}`, span: [sel.start, sel.end], category: "USAGE",
      role: "REQUIRED", source: "human", answer: "UNANSWERED", confidence: null });
    state.conditions.sort((a, b) => a.span[0] - b.span[0]);
    if (state.document_status === "NO_EXPLICIT_CONDITION") state.document_status = "HAS_CONDITIONS";
    window.getSelection().removeAllRanges();
    status("Condition added. Set its category and role.");
    syncStatus();
    render();
  });

  const picked = () => [...document.querySelectorAll(".pick:checked")].map((box) => box.dataset.cond);
  function group(operator) {
    const ids = picked();
    if (ids.length < 2) return status("Tick at least two conditions to group them.", true);
    state.groups.forEach((g) => { g.members = g.members.filter((m) => !ids.includes(m)); });
    const order = (id) => state.conditions.findIndex((c) => c.id === id);
    state.groups.push({ operator, members: ids.sort((a, b) => order(a) - order(b)) });
    status(`Grouped ${ids.length} conditions as ${operator}.`);
    render();
  }
  document.getElementById("group-all").addEventListener("click", () => group("ALL"));
  document.getElementById("group-any").addEventListener("click", () => group("ANY"));
  document.getElementById("ungroup").addEventListener("click", () => {
    const ids = picked();
    state.groups.forEach((g) => { g.members = g.members.filter((m) => !ids.includes(m)); });
    render();
  });

  const statusSelect = document.getElementById("doc-status");
  function syncStatus() {
    statusSelect.replaceChildren(...data.labels.statuses.map((s) => {
      const option = el("option", { value: s, text: s.replaceAll("_", " ").toLowerCase() });
      if (s === state.document_status) option.selected = true;
      return option;
    }));
  }
  statusSelect.addEventListener("change", (e) => { state.document_status = e.target.value; });
  const notes = document.getElementById("notes");
  notes.value = state.notes || "";
  notes.addEventListener("input", () => { state.notes = notes.value || null; });

  // -- save
  function currentState() {
    if (!state.conditions.length && state.document_status === "HAS_CONDITIONS") state.document_status = "NO_EXPLICIT_CONDITION";
    if (state.conditions.length && state.document_status === "NO_EXPLICIT_CONDITION") state.document_status = "HAS_CONDITIONS";
    syncStatus();
    return {
      document_status: state.document_status,
      conditions: state.conditions.map(({ id, span, category, role, source, answer, confidence }) =>
        ({ id, span, category, role, source, answer, confidence })),
      groups: state.groups.map(({ operator, members }) => ({ operator, members })),
      notes: state.notes || null,
    };
  }
  async function save() {
    if (!data.logged_in) return status("Sign in to save reviews. You can still export this one.", true);
    pendingKey = pendingKey || crypto.randomUUID();
    const body = mode === "saved"
      ? { state: currentState(), note: "revised in the review page" }
      : { ...data.source.advisory_id ? { advisory_id: data.source.advisory_id } : { text: data.source.text },
          title: data.title, ...data.meta, state: currentState() };
    const url = mode === "saved" ? `/v1/reviews/${encodeURIComponent(reviewId)}/revisions` : "/v1/reviews";
    status("Saving…");
    try {
      const response = await fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json", "Idempotency-Key": pendingKey },
        body: JSON.stringify(body),
      });
      const result = await response.json();
      if (!response.ok) return status(`Not saved: ${result.error?.message || response.statusText}`, true);
      pendingKey = null;
      if (mode !== "saved") {
        mode = "saved";
        reviewId = result.review_id;
        history.replaceState(null, "", `/ui/reviews/${encodeURIComponent(reviewId)}`);
      }
      status(result.created === false ? "Already saved." : "Saved.");
    } catch (error) {
      status("Network error: not saved. Press Save again to retry safely.", true);
    }
  }
  document.getElementById("save").addEventListener("click", save);

  // -- export (server export for saved reviews; a local copy otherwise)
  function download(name, type, content) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const a = el("a", { href: url, download: name });
    document.body.append(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }
  function localRecord() {
    return { review_format: 1, exported_at: new Date().toISOString(), saved: false,
      advisory_id: data.source.advisory_id, title: data.title, ...data.meta,
      ...currentState(), conditions: currentState().conditions.map((c) => ({ ...c, surface: text.slice(c.span[0], c.span[1]) })) };
  }
  function localMarkdown() {
    const r = localRecord();
    const lines = [`# Exposure review: ${r.title}`, "", `- Advisory: ${r.advisory_id || "pasted text"}`,
      `- Model ${r.model_id}, preprocessing ${r.preprocessing_version}, policy ${r.review_policy_version}`,
      `- Advisory text SHA-256: ${r.content_hash}`, `- Document status: ${r.document_status}`, "- Not saved: local export", ""];
    if (!r.conditions.length) lines.push("No explicit conditions were found. This does not mean the conditions do not apply.", "");
    for (const c of r.conditions) lines.push(`- [${c.answer}] ${c.category} / ${c.role}: "${c.surface}"${c.source === "human" ? " (added by reviewer)" : ""}`);
    for (const g of r.groups) lines.push(`- Group ${g.operator}: ${g.members.join(", ")}`);
    if (r.notes) lines.push("", "## Notes", "", r.notes);
    return lines.join("\n") + "\n";
  }
  const base = `${data.source.advisory_id || "advisory"}-review`;
  document.getElementById("export-json").addEventListener("click", () => {
    if (mode === "saved") window.location.href = `/v1/reviews/${encodeURIComponent(reviewId)}/export?format=json`;
    else download(`${base}.json`, "application/json", JSON.stringify(localRecord(), null, 2));
  });
  document.getElementById("export-md").addEventListener("click", () => {
    if (mode === "saved") window.location.href = `/v1/reviews/${encodeURIComponent(reviewId)}/export?format=markdown`;
    else download(`${base}.md`, "text/markdown", localMarkdown());
  });

  if (data.history?.length) {
    document.getElementById("history").textContent =
      `Saved versions: ${data.history.map((h) => `#${h.seq} ${h.created_at}`).join(" · ")}`;
  }
  syncStatus();
  render();
})();
