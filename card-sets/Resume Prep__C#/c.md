---
deck: "Resume Prep::C#"
topic: "C#"
tags: [ankicardmaker, resume-prep, csharp]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# C# — Resume Prep

Source of truth for the `Resume Prep::C#` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What's the fundamental difference between a value type and a reference type in C#?
   **A:** A value type (<code>struct</code>, <code>int</code>, <code>bool</code>, <code>enum</code>) stores its data directly and is copied by value on assignment or when passed. A reference type (<code>class</code>, <code>string</code>, array) stores a reference pointing to heap data, so assignment copies the reference, not the data.

2. **Q:** Is a C# value type always allocated on the stack?
   **A:** No — it's on the stack only as a local variable or parameter. As a field of a class instance, or when boxed, a value type's data lives on the heap. 'Value type' describes copy semantics, not a storage-location guarantee.

3. **Q:** How do you declare an auto-implemented C# property <code>Name</code> of type <code>string</code> with a public getter and a private setter?
   **A:** <pre><code>public string Name { get; private set; }</code></pre>

4. **Q:** What does a C# auto-implemented property compile down to?
   **A:** A hidden private backing field plus compiler-generated <code>get_Name()</code>/<code>set_Name()</code> accessor methods — properties are syntactic sugar over accessor methods, not a distinct storage mechanism.

5. **Q:** When an <code>async</code> method hits <code>await</code> on an incomplete <code>Task</code>, what happens to the calling thread?
   **A:** Control returns to the caller immediately — the thread is not blocked. When the awaited Task completes, the rest of the method resumes (typically via the captured <code>SynchronizationContext</code> or a thread-pool thread) through a compiler-generated state machine.

6. **Q:** How do you write an async C# method that fetches a string body from a URL using <code>HttpClient</code>?
   **A:** <pre><code>public async Task&lt;string&gt; GetAsync(string url) {
    using var client = new HttpClient();
    return await client.GetStringAsync(url);
}</code></pre>

7. **Q:** What's the difference between <code>Task</code> and <code>Task&lt;T&gt;</code> in C#?
   **A:** <code>Task</code> represents an asynchronous operation with no return value (an awaitable void). <code>Task&lt;T&gt;</code> represents one that produces a result of type <code>T</code>, retrieved via <code>await</code> or <code>.Result</code>.

8. **Q:** Why is <code>async void</code> discouraged in C# except for UI event handlers?
   **A:** Exceptions thrown inside an <code>async void</code> method can't be caught by the caller — there's no Task to await or observe — and the caller has no way to know when it finishes. Use <code>async Task</code> everywhere else.

9. **Q:** How do you write a LINQ query that filters a <code>List&lt;int&gt;</code> for even numbers, ordered descending?
   **A:** <pre><code>var result = numbers
    .Where(n =&gt; n % 2 == 0)
    .OrderByDescending(n =&gt; n)
    .ToList();</code></pre>

10. **Q:** What does 'deferred execution' mean for a LINQ query like <code>var q = list.Where(x =&gt; x &gt; 5);</code>?
   **A:** The query isn't run when <code>q</code> is defined — it's an iterator/expression that only executes when enumerated (<code>foreach</code>, <code>ToList()</code>, etc.), so it re-evaluates against the source's current state each time it's iterated.

11. **Q:** How do you declare and raise a simple <code>EventHandler</code> event in a C# class?
   **A:** <pre><code>public event EventHandler Updated;

protected void OnUpdated() {
    Updated?.Invoke(this, EventArgs.Empty);
}</code></pre>

12. **Q:** What do <code>IDisposable</code> and a <code>using</code> statement guarantee together in C#?
   **A:** <code>IDisposable.Dispose()</code> releases unmanaged resources (file handles, connections, etc.). A <code>using</code> statement/declaration guarantees <code>Dispose()</code> runs deterministically when the block exits, even on an exception — equivalent to a try/finally.

13. **Q:** How do you open and read a file safely in C# using a <code>using</code> declaration?
   **A:** <pre><code>using var reader = new StreamReader(path);
string text = reader.ReadToEnd();
// reader.Dispose() runs automatically at scope end</code></pre>

14. **Q:** What is boxing in C#, and why is it costly?
   **A:** Boxing wraps a value type in an object on the managed heap so it can be used where a reference type is expected. It costs a heap allocation plus a copy and adds GC pressure — avoid it in hot paths (e.g. prefer generic collections over legacy <code>ArrayList</code>).

15. **Q:** How do C# generics avoid the boxing overhead that non-generic collections like <code>ArrayList</code> had for value types?
   **A:** A generic type like <code>List&lt;int&gt;</code> is compiled/specialized for the value type <code>T</code>, storing the raw ints directly instead of wrapping each one as an <code>object</code>, so no boxing/unboxing happens on add or retrieve.

16. **Q:** What compile-time problem do nullable reference types (<code>string?</code> vs <code>string</code>) in C# 8+ help catch?
   **A:** With the feature enabled, <code>string</code> is treated as non-nullable by default, and the compiler warns on any code path that could assign or dereference null on it; <code>string?</code> explicitly opts a variable into allowing null — catching potential <code>NullReferenceException</code>s earlier.

17. **Q:** How do you define a generic C# class <code>Box&lt;T&gt;</code> constrained so <code>T</code> must implement <code>IComparable&lt;T&gt;</code>?
   **A:** <pre><code>public class Box&lt;T&gt; where T : IComparable&lt;T&gt; {
    public T Value;
}</code></pre>

18. **Q:** What's the difference between a C# <code>class</code> and a <code>struct</code> in terms of inheritance and equality?
   **A:** A <code>struct</code> is a value type that cannot be inherited from or inherit (implicitly sealed) and has no reference equality by default. A <code>class</code> is a reference type that supports inheritance and virtual dispatch, with default <code>==</code> comparing reference identity unless overridden.

## Cloze cards

- In C#, a {{c1::delegate}} is a type-safe function pointer that can reference one or more methods with a matching signature; an {{c2::event}} is a delegate field with restricted access — outside the declaring class, code can only {{c3::subscribe and unsubscribe (+= / -=)}}, not invoke or reassign it.
