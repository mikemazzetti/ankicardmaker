---
deck: "Resume Prep::Python"
topic: "Python"
tags: [ankicardmaker, resume-prep, python]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Python — Resume Prep

Source of truth for the `Resume Prep::Python` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In Python's data model, what is true of every value at runtime (functions, classes, ints included)?
   **A:** Every value is an object with an identity, a type, and a value (<code>id()</code>, <code>type()</code>).

2. **Q:** Which of these Python types are mutable: <code>list</code>, <code>tuple</code>, <code>dict</code>, <code>str</code>, <code>set</code>, <code>frozenset</code>?
   **A:** Mutable: <code>list</code>, <code>dict</code>, <code>set</code>. Immutable: <code>tuple</code>, <code>str</code>, <code>frozenset</code>.

3. **Q:** How do you code a list comprehension that squares only the even numbers in <code>nums</code>?
   **A:** <pre><code>squares = [n * n for n in nums if n % 2 == 0]</code></pre>

4. **Q:** Why prefer a generator expression over a list comprehension when streaming rows from a large ETL source file?
   **A:** A generator yields one row at a time and never materializes the whole dataset in memory, so memory use stays O(1) instead of O(n).

5. **Q:** How do you code a decorator <code>timer</code> that prints how long the wrapped function took?
   **A:** <pre><code>import time, functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, time.time() - start)
        return result
    return wrapper</code></pre>

6. **Q:** In a function signature, what does <code>*args</code> collect?
   **A:** Extra positional arguments, packed into a <code>tuple</code>.

7. **Q:** In a function signature, what does <code>**kwargs</code> collect?
   **A:** Extra keyword arguments, packed into a <code>dict</code>.

8. **Q:** What is the GIL (Global Interpreter Lock) in CPython?
   **A:** A mutex that allows only one thread to execute Python bytecode at a time in a single process, even on multi-core machines.

9. **Q:** Why doesn't the GIL prevent Python from benefiting from multiprocessing for CPU-bound ETL work (e.g. scoring rows in a pipeline)?
   **A:** The <code>multiprocessing</code> module runs separate processes, each with its own GIL and interpreter, so CPU-bound work can run truly in parallel across cores.

10. **Q:** How do you code a class-based context manager <code>Timer</code> usable with <code>with Timer():</code>?
   **A:** <pre><code>class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        return False</code></pre>

11. **Q:** How do you write a context manager using <code>contextlib.contextmanager</code> instead of a class?
   **A:** <pre><code>from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(time.time() - start)</code></pre>

12. **Q:** How do you code an f-string that prints a variable <code>name</code> and formats <code>price</code> to 2 decimal places?
   **A:** <pre><code>print(f"{name}: {price:.2f}")</code></pre>

13. **Q:** How do you code a set comprehension that returns the unique lengths of words in a list <code>words</code>?
   **A:** <pre><code>lengths = {len(w) for w in words}</code></pre>

14. **Q:** How would you code retry-with-backoff around an API call that may hit a rate limit (like the BUFFET pipeline hitting a comments API)?
   **A:** <pre><code>import time

for attempt in range(5):
    resp = call_api()
    if resp.status_code != 429:
        break
    time.sleep(2 ** attempt)</code></pre>

15. **Q:** What Python data structure would you use to deduplicate 63k+ scraped comments by ID before running sentiment analysis, and why?
   **A:** A <code>set</code> of seen IDs — O(1) average membership check and insertion, versus O(n) for a list.

16. **Q:** What is the difference between a shallow copy and a deep copy of a nested list?
   **A:** A shallow copy (<code>copy.copy</code>) copies the outer container only, so nested objects are still shared; a deep copy (<code>copy.deepcopy</code>) recursively copies every nested object too.

17. **Q:** What is the difference between <code>==</code> and <code>is</code> in Python?
   **A:** <code>==</code> compares value equality (calls <code>__eq__</code>); <code>is</code> compares object identity (same memory address).

18. **Q:** What two dunder methods make an object an iterator, and what does each do?
   **A:** <code>__iter__</code> returns the iterator itself; <code>__next__</code> returns the next value or raises <code>StopIteration</code>.

## Cloze cards

- A function containing a {{c1::yield}} statement becomes a {{c2::generator}} function, which returns a generator object instead of running immediately. <!-- Back Extra: Generators produce values lazily, one at a time, pausing execution at each yield. -->
- Using a {{c1::mutable}} object like a list or dict as a default argument value is a classic Python gotcha because the default is created {{c2::once, at function definition time}}, and mutations persist across calls. <!-- Back Extra: Fix: use <code>def f(x=None): x = x or []</code>. -->
