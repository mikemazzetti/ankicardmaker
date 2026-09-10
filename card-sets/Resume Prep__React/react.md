---
deck: "Resume Prep::React"
topic: "React"
tags: [ankicardmaker, resume-prep, react]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# React — Resume Prep

Source of truth for the `Resume Prep::React` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is JSX in React?
   **A:** A syntax extension that lets you write HTML-like markup inside JavaScript; it compiles to <code>React.createElement()</code> calls.

2. **Q:** How do you code a functional React component that displays a greeting for a <code>name</code> prop?
   **A:** <pre><code>function Greeting({ name }) {
  return &lt;h1&gt;Hello, {name}!&lt;/h1&gt;;
}</code></pre>

3. **Q:** In React, what's the core difference between props and state?
   **A:** Props are read-only data passed from a parent to configure a component; state is data owned and managed inside a component that can change over time and triggers a re-render when updated.

4. **Q:** How do you code a component that increments a counter on button click using <code>useState</code>?
   **A:** <pre><code>function Counter() {
  const [count, setCount] = useState(0);
  return (
    &lt;button onClick={() =&gt; setCount(c =&gt; c + 1)}&gt;
      {count}
    &lt;/button&gt;
  );
}</code></pre>

5. **Q:** What does the dependency array argument to <code>useEffect</code> control?
   **A:** When the effect re-runs: an empty array <code>[]</code> runs it once on mount; omitting the array runs it after every render; listing values re-runs it whenever any of those values change.

6. **Q:** How do you code a <code>useEffect</code> that subscribes to a window resize event and cleans up on unmount?
   **A:** <pre><code>useEffect(() => {
  const onResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', onResize);
  return () => window.removeEventListener('resize', onResize);
}, []);</code></pre>

7. **Q:** What common bug happens when a <code>useEffect</code> reads a state variable but omits it from the dependency array?
   **A:** A 'stale closure': the effect keeps using the value from the render it was created in, so it never sees later updates to that variable until something else forces a re-run.

8. **Q:** What problem does <code>useMemo</code> solve?
   **A:** It memoizes the result of an expensive computation, recomputing it only when its dependencies change, avoiding unnecessary recalculation on every render.

9. **Q:** What problem does <code>useCallback</code> solve?
   **A:** It memoizes a function reference itself so it isn't recreated on every render, preventing unnecessary re-renders of child components that receive it as a prop (e.g. with <code>React.memo</code>).

10. **Q:** What is the virtual DOM in React?
   **A:** An in-memory, lightweight representation of the real DOM tree that React updates first; React then diffs it against the previous version (reconciliation) to compute the minimal set of real DOM mutations needed.

11. **Q:** Why does React require a stable, unique <code>key</code> prop when rendering a list of elements?
   **A:** Keys let React's reconciler match array items between renders so it can detect insertions, removals, and reorders correctly instead of mismatching or needlessly re-creating DOM nodes.

12. **Q:** What's a common pitfall of using the array index as a React list <code>key</code>?
   **A:** If the list is reordered, filtered, or items are inserted/removed, indices shift and no longer identify the same item, causing React to reuse DOM nodes/state for the wrong items.

13. **Q:** How do you code a controlled text input in React?
   **A:** <pre><code>function NameInput() {
  const [value, setValue] = useState('');
  return (
    &lt;input
      value={value}
      onChange={e =&gt; setValue(e.target.value)}
    /&gt;
  );
}</code></pre>

14. **Q:** What makes an input 'controlled' vs 'uncontrolled' in React?
   **A:** A controlled input's value is driven by React state via the <code>value</code> prop and updated through <code>onChange</code>; an uncontrolled input manages its own value in the DOM and is read via a <code>ref</code>.

15. **Q:** What is 'lifting state up' in React?
   **A:** Moving shared state from child components to their closest common ancestor so multiple sibling components can read and update the same data via props.

16. **Q:** How do you code sharing a value with deeply nested components without prop drilling, using Context?
   **A:** <pre><code>const ThemeContext = createContext('light');

function App() {
  return (
    &lt;ThemeContext.Provider value="dark"&gt;
      &lt;Toolbar /&gt;
    &lt;/ThemeContext.Provider&gt;
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return &lt;div&gt;{theme}&lt;/div&gt;;
}</code></pre>

## Cloze cards

- In React, calling {{c1::useState}} returns a pair: the current state value and a function to update it, e.g. <code>const [count, setCount] = useState(0);</code>
- The Rules of Hooks state you must only call hooks at the {{c1::top level}} of a component (never inside loops, conditions, or nested functions), and only from {{c2::React function components or custom hooks}}.
