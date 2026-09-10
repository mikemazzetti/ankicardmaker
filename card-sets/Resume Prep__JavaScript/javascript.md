---
deck: "Resume Prep::JavaScript"
topic: "JavaScript"
tags: [ankicardmaker, resume-prep, javascript]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# JavaScript — Resume Prep

Source of truth for the `Resume Prep::JavaScript` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In the JS event loop, which runs first after the current synchronous task finishes: all queued microtasks, or the next macrotask?
   **A:** All queued microtasks (e.g. resolved Promise callbacks) run to completion before the next macrotask (e.g. <code>setTimeout</code> callback).

2. **Q:** How do you code a closure-based counter function that returns an incrementing count each call?
   **A:** <pre><code>function makeCounter() {
  let count = 0;
  return function () {
    count += 1;
    return count;
  };
}
const next = makeCounter();</code></pre>

3. **Q:** How is the value of <code>this</code> determined in a regular function vs an arrow function?
   **A:** A regular function's <code>this</code> is set by how it's called (call-site); an arrow function has no own <code>this</code> — it lexically inherits <code>this</code> from its enclosing scope.

4. **Q:** How do you code a constructor function <code>Dog</code> that adds a <code>bark</code> method to its prototype (not per-instance)?
   **A:** <pre><code>function Dog(name) {
  this.name = name;
}
Dog.prototype.bark = function () {
  return this.name + ' says woof';
};</code></pre>

5. **Q:** What is the key difference between <code>==</code> and <code>===</code> in JavaScript?
   **A:** <code>==</code> compares after coercing operands to a common type; <code>===</code> compares value and type with no coercion.

6. **Q:** What does 'hoisting' mean for <code>var</code> declarations and function declarations in JavaScript?
   **A:** Their declarations are moved to the top of their scope at compile time, so they can be referenced before the line they're written on (<code>var</code> is hoisted as <code>undefined</code>; function declarations are hoisted fully).

7. **Q:** How do you code an async function that fetches JSON from a URL and handles errors with try/catch?
   **A:** <pre><code>async function getData(url) {
  try {
    const res = await fetch(url);
    return await res.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
}</code></pre>

8. **Q:** What are the three states a Promise can be in?
   **A:** Pending, fulfilled, and rejected.

9. **Q:** How do you code a Promise-wrapped version of a callback-style delay function?
   **A:** <pre><code>function delay(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}</code></pre>

10. **Q:** How do you code a chain that filters an array for numbers over 10, then doubles them, using array methods?
   **A:** <pre><code>const result = nums.filter((n) => n > 10).map((n) => n * 2);</code></pre>

11. **Q:** How do you destructure an object <code>{ id, name }</code> from a function parameter directly?
   **A:** <pre><code>function printUser({ id, name }) {
  console.log(id, name);
}</code></pre>

12. **Q:** What does <code>Promise.all([p1, p2, p3])</code> do if one of the promises rejects?
   **A:** It immediately rejects with that first rejection reason, even if the other promises are still pending.

13. **Q:** Between a resolved Promise's <code>.then()</code> callback and a <code>setTimeout(fn, 0)</code> callback, which runs first and why?
   **A:** The <code>.then()</code> callback runs first — it's a microtask, and the microtask queue always drains completely before the next macrotask (<code>setTimeout</code>) runs.

14. **Q:** How can a closure cause a memory leak in JavaScript?
   **A:** If a closure keeps a reference to a large object (e.g. a DOM node or big array) and that closure itself is kept alive (e.g. attached as a long-lived event listener), the referenced object can't be garbage collected.

15. **Q:** How do you code a <code>debounce(fn, delay)</code> higher-order function using a closure?
   **A:** <pre><code>function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}</code></pre>

16. **Q:** When you access a property that isn't on an object directly, where does JavaScript look next?
   **A:** It walks up the object's prototype chain (via <code>[[Prototype]]</code> / <code>__proto__</code>) until it finds the property or reaches <code>null</code>.

17. **Q:** Arrow function *(reversed — tested both ways)*
   **A:** A function that does not have its own <code>this</code>, <code>arguments</code>, or prototype, and inherits <code>this</code> lexically from its enclosing scope.

18. **Q:** How do you code merging two arrays and adding one extra element using the spread operator?
   **A:** <pre><code>const merged = [...arr1, ...arr2, extraItem];</code></pre>

## Cloze cards

- A {{c1::closure}} is formed when an inner function retains access to variables from its enclosing function's scope even after that outer function has returned.
- <code>var</code> is {{c1::function-scoped}}, while <code>let</code> and <code>const</code> are {{c2::block-scoped}}; <code>let</code>/<code>const</code> also sit in a {{c3::temporal dead zone}} before their declaration line.
