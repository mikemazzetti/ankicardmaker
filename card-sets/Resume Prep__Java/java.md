---
deck: "Resume Prep::Java"
topic: "Java"
tags: [ankicardmaker, resume-prep, java]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Java — Resume Prep

Source of truth for the `Resume Prep::Java` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** In the Java Memory Model, what does the <code>volatile</code> keyword actually guarantee?
   **A:** Visibility and ordering, not atomicity: a write to a volatile field is immediately visible to all threads and can't be reordered across the access (happens-before edge). It does NOT make compound operations like <code>i++</code> atomic.

2. **Q:** Besides mutual exclusion, what memory-model guarantee does <code>synchronized</code> provide?
   **A:** Visibility: entering and exiting a synchronized block on the same lock establishes a happens-before relationship, so changes made inside are guaranteed visible to the next thread that acquires that lock.

3. **Q:** Java's <code>final</code> keyword applied to a variable *(reversed — tested both ways)*
   **A:** The variable's reference (or primitive value) can be assigned only once; for object references, the referenced object's own internal state can still be mutated unless it's independently immutable.

4. **Q:** What is the fundamental compiler-enforced difference between checked and unchecked exceptions in Java?
   **A:** Checked exceptions (subclasses of <code>Exception</code> but not <code>RuntimeException</code>, e.g. <code>IOException</code>) must be caught or declared with <code>throws</code> or the code won't compile. Unchecked exceptions (<code>RuntimeException</code>/<code>Error</code> subclasses, e.g. <code>NullPointerException</code>) are never enforced by the compiler.

5. **Q:** How do you open and read a file in Java so the reader is automatically closed even if an exception is thrown?
   **A:** Use try-with-resources: <pre><code>try (BufferedReader br = new BufferedReader(new FileReader("data.txt"))) {
    String line = br.readLine();
    System.out.println(line);
} catch (IOException e) {
    e.printStackTrace();
}</code></pre>

6. **Q:** What is the contract between <code>equals()</code> and <code>hashCode()</code> in Java?
   **A:** If two objects are equal per <code>equals()</code>, they MUST return the same <code>hashCode()</code>. The converse isn't required (unequal objects may share a hash). Violating the forward rule silently breaks hash-based collections like <code>HashMap</code>/<code>HashSet</code>.

7. **Q:** How do you correctly override <code>equals()</code> and <code>hashCode()</code> for a class with fields <code>x</code> and <code>y</code>?
   **A:** <pre><code>@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Point p)) return false;
    return x == p.x &amp;&amp; y == p.y;
}

@Override
public int hashCode() {
    return Objects.hash(x, y);
}</code></pre>

8. **Q:** What does the Java compiler auto-generate for you when you declare a <code>record</code>?
   **A:** A canonical constructor, private final fields for each component, public accessor methods (named after the components, not getX()), plus <code>equals()</code>, <code>hashCode()</code>, and <code>toString()</code> derived from the component list — the type is implicitly immutable.

9. **Q:** How do you declare an immutable <code>Point</code> record with int components <code>x</code> and <code>y</code>?
   **A:** <pre><code>public record Point(int x, int y) {}</code></pre>

10. **Q:** What does the bound in <code>&lt;T extends Comparable&lt;T&gt;&gt;</code> mean for a Java generic method?
   **A:** T must be a type that implements <code>Comparable&lt;T&gt;</code>, so the method body is allowed to call <code>compareTo()</code> on values of type T.

11. **Q:** How do you write a generic Java method that returns the larger of two Comparable values?
   **A:** <pre><code>public static &lt;T extends Comparable&lt;T&gt;&gt; T max(T a, T b) {
    return a.compareTo(b) &gt;= 0 ? a : b;
}</code></pre>

12. **Q:** Why do generational garbage collectors run frequent young-generation (minor) collections instead of scanning the whole heap each time?
   **A:** Most objects die young, so a minor GC only has to copy the small fraction of still-live objects out of a small young-gen region — fast and frequent, avoiding the expense of scanning the entire heap on every collection.

13. **Q:** When should you prefer <code>ArrayList</code> over <code>LinkedList</code> in Java?
   **A:** When you need fast random access — <code>get(i)</code> is O(1) on <code>ArrayList</code> (backed by a resizable array) vs O(n) on <code>LinkedList</code>. Prefer <code>LinkedList</code> only for frequent insert/remove at arbitrary positions via an iterator, since ArrayList shifts elements on insert/remove.

14. **Q:** How do you use the Stream API to keep only strings longer than 3 characters and collect them into a new List?
   **A:** <pre><code>List&lt;String&gt; result = names.stream()
    .filter(s -&gt; s.length() &gt; 3)
    .collect(Collectors.toList());</code></pre>

15. **Q:** What does Spring's <code>@Async</code> annotation do, and how was it used in the Government of Ontario eForm validation microservice?
   **A:** It runs the annotated method on a separate thread from Spring's task executor, returning control to the caller immediately (often returning a <code>CompletableFuture</code>) instead of blocking. It enabled non-blocking I/O in the high-throughput validation microservice, cutting latency ~40%.

16. **Q:** What is the N+1 select problem, and what JPQL fix resolves it (as used at ServiceOntario to cut read latency 40%)?
   **A:** Lazily fetching N parent entities triggers 1 query for the parents plus N extra queries — one per parent — to load each one's association. Fix: add <code>JOIN FETCH</code> to the JPQL query (e.g. <code>SELECT e FROM Entity e JOIN FETCH e.children</code>) so the association loads in the same query, plus tuning Hibernate's batch-fetch size for remaining lazy loads.

17. **Q:** In a Spring Boot service, what does a Resilience4j <code>CircuitBreaker</code> do once a downstream call's failure rate crosses its configured threshold?
   **A:** It trips to the OPEN state and short-circuits further calls immediately (fast-fail, no wasted latency waiting on a failing dependency) for a wait duration, then moves to HALF_OPEN to test a limited number of calls before deciding whether to close again.

18. **Q:** What role does Caffeine caching play in a Spring Boot backend, and what eviction strategies does it support?
   **A:** It's an in-memory cache (plugged in via Spring's cache abstraction) that avoids repeated expensive calls/DB hits. It supports size-based and time-based eviction (<code>expireAfterWrite</code>/<code>expireAfterAccess</code>) using a near-optimal Window TinyLFU eviction policy.

## Cloze cards

- The JVM divides its runtime data areas into the {{c1::heap}} (shared object storage, garbage collected), the per-thread {{c2::stack}} (local variables and call frames), and the {{c3::method area/metaspace}} (class metadata and static fields).
- The core Java Collections Framework interfaces are {{c1::List}} (ordered, duplicates allowed), {{c2::Set}} (no duplicate elements), and {{c3::Map}} (key-value pairs; not itself a subtype of Collection).
