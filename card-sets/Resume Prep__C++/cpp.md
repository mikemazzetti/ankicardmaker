---
deck: "Resume Prep::C++"
topic: "C++"
tags: [ankicardmaker, resume-prep, cpp]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# C++ — Resume Prep

Source of truth for the `Resume Prep::C++` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the core difference between a pointer and a reference in C++?
   **A:** A reference must be bound at declaration, can never be null, and can never be rebound to alias a different object. A pointer can be reassigned, can be null, and requires explicit dereferencing (<code>*p</code>) to access the pointee.

2. **Q:** What does RAII stand for, and what problem does it solve in C++?
   **A:** Resource Acquisition Is Initialization — a resource (memory, file handle, lock) is acquired in a constructor and released in the destructor, so it's automatically freed when the owning object goes out of scope, even if an exception unwinds the stack.

3. **Q:** How do you write a minimal RAII wrapper around a raw <code>FILE*</code> handle in C++?
   **A:** <pre><code>class FileGuard {
    FILE* fp;
public:
    explicit FileGuard(const char* path) : fp(fopen(path, "r")) {}
    ~FileGuard() { if (fp) fclose(fp); }
    FILE* get() const { return fp; }
};</code></pre>

4. **Q:** What's the key ownership difference between <code>std::unique_ptr</code> and <code>std::shared_ptr</code>?
   **A:** <code>unique_ptr</code> has sole, non-copyable ownership (move-only), with near-zero overhead over a raw pointer. <code>shared_ptr</code> uses atomic reference counting so multiple owners can share the object, which is freed only when the last <code>shared_ptr</code> is destroyed.

5. **Q:** How do you create a <code>std::unique_ptr&lt;Widget&gt;</code> and move ownership into a function taking it by value?
   **A:** <pre><code>auto w = std::make_unique&lt;Widget&gt;(args);
takeOwnership(std::move(w));
// w is now null; caller must not use it</code></pre>

6. **Q:** What memory-leak risk does <code>std::weak_ptr</code> solve when two objects hold <code>std::shared_ptr</code>s to each other?
   **A:** A reference cycle between two <code>shared_ptr</code>s means their counts never reach zero, leaking both objects. <code>weak_ptr</code> holds a non-owning reference that doesn't affect the count; call <code>.lock()</code> to get a temporary <code>shared_ptr</code> only if the object is still alive.

7. **Q:** What is an rvalue reference (<code>T&amp;&amp;</code>) used for in C++?
   **A:** It binds to temporaries/movable values so a function overload can detect 'this object is about to be destroyed anyway' and steal (move) its internal resources instead of deep-copying them.

8. **Q:** How do you implement a move constructor for a class that owns a raw heap buffer <code>data</code> and size <code>len</code>?
   **A:** <pre><code>MyBuf(MyBuf&amp;&amp; other) noexcept
    : data(other.data), len(other.len) {
    other.data = nullptr;
    other.len = 0;
}</code></pre>

9. **Q:** What is the Rule of Zero in C++?
   **A:** Prefer composing a class entirely from members that already manage their own resources (smart pointers, containers, strings) so you never write any of the five special member functions — the compiler-generated versions are already correct.

10. **Q:** Why does declaring a custom destructor implicitly disable the compiler-generated move constructor in C++?
   **A:** A user-declared destructor signals custom resource-management logic, so the compiler won't risk synthesizing a possibly-unsafe move constructor. Moves then silently fall back to copies unless you define the move constructor yourself (or explicitly <code>= default</code> it).

11. **Q:** What does <code>const</code> on a C++ member function guarantee?
   **A:** It promises not to modify any non-<code>mutable</code> member of the object — the implicit <code>this</code> becomes a pointer-to-const — which is what allows the function to be called on const instances and const references.

12. **Q:** Between <code>const int* p</code> and <code>int* const p</code>, which one is a pointer that cannot itself be reassigned (but may modify the pointed-to int)?
   **A:** <code>int* const p</code> — the <code>const</code> binds to <code>p</code> itself. <code>const int* p</code> is the opposite: a reassignable pointer to a constant int.

13. **Q:** How do you declare a C++ function template that returns the larger of two values of any comparable type?
   **A:** <pre><code>template &lt;typename T&gt;
T max_of(const T&amp; a, const T&amp; b) {
    return (a &gt; b) ? a : b;
}</code></pre>

14. **Q:** What is a vtable in C++, and when does a class get one?
   **A:** A per-class array of function pointers used to resolve virtual calls at runtime. A class gets a vtable (and each instance a hidden vptr) as soon as it declares or inherits at least one <code>virtual</code> function.

15. **Q:** Why should a base class's destructor be <code>virtual</code> if you plan to <code>delete</code> a derived object through a base class pointer?
   **A:** Without a virtual destructor, <code>delete basePtr</code> only invokes the base class's destructor and skips the derived class's cleanup — undefined behavior, typically a resource leak.

16. **Q:** What's the core tradeoff between stack and heap allocation in C++?
   **A:** Stack: fixed size, automatic lifetime tied to scope, very fast (just a pointer bump), but limited (~MB). Heap: manually managed via <code>new</code>/<code>delete</code> or smart pointers, flexible size, slower due to allocator bookkeeping, lifetime independent of scope.

17. **Q:** Give an example of undefined behavior in C++ that the compiler is not required to diagnose.
   **A:** Dereferencing a null or dangling pointer, signed integer overflow, or reading an uninitialized variable — the standard places no requirement on the outcome, so the compiler may optimize as if it never happens, sometimes with surprising results.

18. **Q:** How do you iterate a <code>std::vector&lt;int&gt;</code> and erase all even elements using the erase-remove idiom?
   **A:** <pre><code>v.erase(
    std::remove_if(v.begin(), v.end(),
        [](int x) { return x % 2 == 0; }),
    v.end());</code></pre>

19. **Q:** What STL container gives O(log n) sorted insertion/lookup, and which alternative gives O(1)-average lookup with no ordering guarantee?
   **A:** <code>std::map</code>/<code>std::set</code> (red-black tree, O(log n), kept sorted). <code>std::unordered_map</code>/<code>std::unordered_set</code> give O(1) average via hashing but no ordering guarantee.

## Cloze cards

- The Rule of Five says a class that manages a resource manually should typically define all of: {{c1::destructor}}, {{c2::copy constructor}}, {{c3::copy assignment operator}}, {{c4::move constructor}}, and {{c5::move assignment operator}}.
