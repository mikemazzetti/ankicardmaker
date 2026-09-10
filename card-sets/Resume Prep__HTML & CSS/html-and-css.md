---
deck: "Resume Prep::HTML & CSS"
topic: "HTML & CSS"
tags: [ankicardmaker, resume-prep, html-css]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# HTML & CSS — Resume Prep

Source of truth for the `Resume Prep::HTML & CSS` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Give three semantic HTML5 tags you'd use instead of generic <code>&lt;div&gt;</code>s for a page's structure.
   **A:** <code>&lt;header&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;article&gt;</code>, <code>&lt;section&gt;</code>, <code>&lt;footer&gt;</code> (any three).

2. **Q:** How do you code a flex container that centers its child both horizontally and vertically?
   **A:** <pre><code>.center {
  display: flex;
  justify-content: center;
  align-items: center;
}</code></pre>

3. **Q:** How do you code a CSS grid container with 3 equal-width columns and a 16px gap?
   **A:** <pre><code>.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}</code></pre>

4. **Q:** Ranked highest to lowest, what is the CSS specificity order for inline styles, ID selectors, class/attribute/pseudo-class selectors, and element selectors?
   **A:** Inline style &gt; ID selector &gt; class/attribute/pseudo-class selector &gt; element/pseudo-element selector.

5. **Q:** What's the difference between <code>position: absolute</code> and <code>position: relative</code>?
   **A:** <code>relative</code> positions an element relative to its own normal position, without removing it from the document flow; <code>absolute</code> removes it from flow and positions it relative to its nearest positioned ancestor.

6. **Q:** What's the difference between <code>position: fixed</code> and <code>position: sticky</code>?
   **A:** <code>fixed</code> is always positioned relative to the viewport, ignoring scroll; <code>sticky</code> behaves like <code>relative</code> until a scroll threshold is crossed, then sticks like <code>fixed</code> within its containing block.

7. **Q:** What do the CSS units <code>rem</code>, <code>em</code>, and <code>%</code> each size relative to?
   **A:** <code>rem</code> is relative to the root (<code>&lt;html&gt;</code>) font size; <code>em</code> is relative to the current element's own (or inherited) font size; <code>%</code> is relative to the corresponding property of the parent element.

8. **Q:** How do you code a media query that sets <code>.container</code> to full width on screens 600px wide or narrower?
   **A:** <pre><code>@media (max-width: 600px) {
  .container {
    width: 100%;
  }
}</code></pre>

9. **Q:** How do you code an accessible icon-only button using an ARIA attribute so screen readers announce its purpose?
   **A:** <pre><code><button aria-label="Close dialog">
  &times;
</button></code></pre>

10. **Q:** What does the <code>aria-label</code> attribute do?
   **A:** It provides an accessible name for an element that screen readers announce, used when there's no visible text (or the visible text isn't descriptive enough).

11. **Q:** How do you code a form input properly associated with its visible label for accessibility?
   **A:** <pre><code><label for="email">Email</label>
<input id="email" type="email" name="email" /></code></pre>

12. **Q:** What does <code>box-sizing: border-box</code> change about how an element's <code>width</code> is calculated?
   **A:** <code>width</code> includes the padding and border, so the element's total rendered width stays equal to the declared <code>width</code> (instead of content-box, where padding/border are added on top).

13. **Q:** How do you code a flex row that spaces its items evenly with equal gaps between them (not at the edges)?
   **A:** <pre><code>.row {
  display: flex;
  justify-content: space-between;
}</code></pre>

14. **Q:** What's the difference between <code>visibility: hidden</code> and <code>display: none</code>?
   **A:** <code>visibility: hidden</code> hides the element but it still occupies layout space and is present in the accessibility tree in some contexts; <code>display: none</code> removes it from layout entirely and from the accessibility tree.

15. **Q:** For <code>z-index</code> to have any effect on an element, what other CSS property must be set on it?
   **A:** <code>position</code> must be set to something other than <code>static</code> (e.g. <code>relative</code>, <code>absolute</code>, <code>fixed</code>, or <code>sticky</code>).

16. **Q:** How do you code an <code>&lt;img&gt;</code> that scales down responsively but never exceeds its container's width?
   **A:** <pre><code>img {
  max-width: 100%;
  height: auto;
}</code></pre>

17. **Q:** What is the default value of <code>flex-direction</code> on a flex container?
   **A:** <code>row</code> (items laid out left to right along the main axis).

18. **Q:** In <code>grid-template-columns: 2fr 1fr</code>, how is the available space divided between the two columns?
   **A:** Into 3 fractional shares total; the first column gets 2/3 of the remaining space, the second gets 1/3.

19. **Q:** Why is a <code>&lt;button&gt;</code> preferable to a <code>&lt;div onClick&gt;</code> for a clickable action, from an accessibility standpoint?
   **A:** <code>&lt;button&gt;</code> is natively focusable, keyboard-activatable (Enter/Space), and announced with the 'button' role by screen readers; a <code>&lt;div&gt;</code> gets none of that for free and needs <code>tabindex</code>, key handlers, and <code>role="button"</code> to match.

## Cloze cards

- From innermost to outermost, the CSS box model layers are: {{c1::content}}, {{c2::padding}}, {{c3::border}}, {{c4::margin}}.
