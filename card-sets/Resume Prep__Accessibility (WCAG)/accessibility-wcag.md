---
deck: "Resume Prep::Accessibility (WCAG)"
topic: "Accessibility (WCAG)"
tags: [ankicardmaker, resume-prep, accessibility]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Accessibility (WCAG) — Resume Prep

Source of truth for the `Resume Prep::Accessibility (WCAG)` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does WCAG stand for, and who publishes it?
   **A:** Web Content Accessibility Guidelines, published by the W3C's Web Accessibility Initiative (WAI).

2. **Q:** Which version of WCAG did the ServiceOntario TypeScript UI library target for compliance?
   **A:** WCAG 2.1.

3. **Q:** Give an example of a WCAG "Perceivable" requirement.
   **A:** Providing text alternatives (alt text) for non-text content, so information isn't conveyed through a sense (e.g. sight) that some users lack — it can be re-presented as speech, braille, etc.

4. **Q:** Give an example of a WCAG "Operable" requirement.
   **A:** All functionality must be operable through a keyboard alone, with no interaction that requires a mouse and no keyboard trap a user can't escape.

5. **Q:** What is the minimum WCAG AA contrast ratio for normal body text against its background?
   **A:** 4.5:1.

6. **Q:** What is the minimum WCAG AA contrast ratio for large text (roughly 18pt, or 14pt bold, and larger)?
   **A:** 3:1.

7. **Q:** Why prefer semantic HTML (e.g. <code>&lt;button&gt;</code>, <code>&lt;nav&gt;</code>) over a generic <code>&lt;div&gt;</code> with a click handler for interactive UI?
   **A:** Semantic elements come with built-in accessibility semantics — correct role, keyboard operability (Enter/Space), and focusability — for free. A <code>&lt;div onclick&gt;</code> has none of that; you'd have to manually add <code>role</code>, <code>tabindex</code>, and keyboard handlers to match what a real <code>&lt;button&gt;</code> already does.

8. **Q:** What does an ARIA <code>role</code> attribute do?
   **A:** It tells assistive technologies (like screen readers) what a custom or non-semantic element's purpose is — e.g. <code>role="button"</code> or <code>role="alert"</code> — when the native HTML element doesn't already convey that.

9. **Q:** What is the "first rule of ARIA use"?
   **A:** Don't use ARIA if a native HTML element or attribute already provides the needed semantics and behavior — e.g. use <code>&lt;button&gt;</code> instead of <code>&lt;div role="button"&gt;</code>.

10. **Q:** What's the difference between <code>aria-label</code> and <code>aria-labelledby</code>?
   **A:** <code>aria-label</code> supplies the accessible name directly as a string on the element itself. <code>aria-labelledby</code> instead points to the <code>id</code>(s) of other element(s) whose text content is used as the accessible name, e.g.:<br><pre><code>&lt;span id="lbl"&gt;Close&lt;/span&gt;
&lt;button aria-labelledby="lbl"&gt;X&lt;/button&gt;</code></pre>

11. **Q:** What should alt text describe, and when should it be empty (<code>alt=""</code>)?
   **A:** Alt text should describe the image's meaning or function in context (not just "image of..."). It should be left empty when the image is purely decorative, so screen readers skip it instead of announcing noise.

12. **Q:** How do you make a non-natively-focusable element keyboard-reachable, and what's the difference between <code>tabindex="0"</code> and <code>tabindex="-1"</code>?
   **A:** Add a <code>tabindex</code> attribute. <code>tabindex="0"</code> inserts the element into the natural tab order at its position in the DOM. <code>tabindex="-1"</code> makes it focusable only programmatically (e.g. via <code>element.focus()</code>), not by Tab key.

13. **Q:** Why is it important not to remove the default focus outline (e.g. <code>outline: none</code>) without replacing it?
   **A:** Sighted keyboard-only users rely on the visible focus indicator to know which element currently has focus. Remove it with nothing in its place and keyboard navigation becomes unusable — you can't tell where you are on the page.

14. **Q:** When a modal dialog opens, what focus-management behavior does accessibility best practice expect?
   **A:** Focus should move into the modal (typically its first focusable element or the dialog container) and be trapped there — Tab cycles only within the modal — until it closes, at which point focus returns to the element that triggered it.

15. **Q:** How does a screen reader primarily understand a webpage's structure, rather than its visual layout?
   **A:** It reads the browser's accessibility tree, built from semantic HTML and ARIA attributes, announcing each element's role, accessible name, and state as the user navigates by headings, landmarks, links, and tab order.

16. **Q:** Beyond usability for disabled users, why did WCAG 2.1 compliance matter for a Government of Ontario / ServiceOntario UI library specifically?
   **A:** It's a legal obligation: Ontario's Accessibility for Ontarians with Disabilities Act (AODA) requires public-sector digital services to meet WCAG 2.0/2.1 AA, so compliance is both a legal requirement and a way to ensure the service reaches every citizen, including those using assistive tech.

## Cloze cards

- WCAG is organized around four POUR principles: {{c1::Perceivable}}, {{c2::Operable}}, {{c3::Understandable}}, and {{c4::Robust}}.
- WCAG conformance levels, least to most strict: {{c1::A}} (minimum/essential), {{c2::AA}} (mid-level, the standard target for legal/industry compliance), {{c3::AAA}} (highest, not usually required for an entire site).
