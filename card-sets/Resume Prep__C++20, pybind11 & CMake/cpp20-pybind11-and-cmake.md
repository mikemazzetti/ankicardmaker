---
deck: "Resume Prep::C++20, pybind11 & CMake"
topic: "C++20, pybind11 & CMake"
tags: [ankicardmaker, cpp20-pybind11]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# C++20, pybind11 & CMake — Resume Prep

Source of truth for the `Resume Prep::C++20, pybind11 & CMake` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Write a C++20 function template constrained to only accept integral types using a concept.
   **A:** <pre><code>template &lt;std::integral T&gt;
T add(T a, T b) {
    return a + b;
}</code></pre>

2. **Q:** Write a C++20 ranges pipeline that filters a vector of ints for even numbers, then squares them.
   **A:** <pre><code>auto result = nums
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; });</code></pre>

3. **Q:** Which three keywords, if any one appears in a function body, make that function a C++20 coroutine?
   **A:** <code>co_await</code>, <code>co_yield</code>, and <code>co_return</code>.

4. **Q:** What's the main build-system benefit of C++20 modules over textual #include headers?
   **A:** Faster compilation (no re-parsing headers per translation unit) and no macro/preprocessor leakage between files — imports are isolated, not textually pasted in.

5. **Q:** What operator does C++20 add for three-way comparison, and what is it commonly called?
   **A:** <code>&lt;=&gt;</code>, the "spaceship operator" — a single overload can generate <code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code> automatically.

6. **Q:** Write a C++20 struct that gets all six comparison operators for free using the spaceship operator.
   **A:** <pre><code>struct Money {
    long cents;
    auto operator&lt;=&gt;(const Money&amp;) const = default;
};</code></pre>

7. **Q:** What does <code>std::span&lt;T&gt;</code> provide?
   **A:** A lightweight, non-owning view (pointer + length) over a contiguous sequence — works over arrays, vectors, etc. without copying data.

8. **Q:** Write a C++20 function signature that accepts a read-only view over any contiguous container of doubles using std::span.
   **A:** <pre><code>double sum(std::span&lt;const double&gt; values);</code></pre>

9. **Q:** BMO's C++20 financial calculation engine cut transaction batch-processing latency by how much, and across how many daily account records?
   **A:** 42% latency reduction across 2.5M+ daily account records.

10. **Q:** What macro defines the entry point pybind11 uses to build a Python extension module from C++?
   **A:** <code>PYBIND11_MODULE(module_name, m)</code> — <code>m</code> is the module object you attach functions/classes to.

11. **Q:** Write a minimal pybind11 snippet exposing a C++ function "add" to Python.
   **A:** <pre><code>#include &lt;pybind11/pybind11.h&gt;
namespace py = pybind11;

int add(int a, int b) { return a + b; }

PYBIND11_MODULE(fastmath, m) {
    m.doc() = "fast C++ math functions";
    m.def("add", &amp;add, "Add two integers");
}</code></pre>

12. **Q:** Which pybind11 template class exposes a C++ class to Python, and how do you bind a method with it?
   **A:** <pre><code>py::class_&lt;Ledger&gt;(m, "Ledger")
    .def(py::init&lt;&gt;())
    .def("post_entry", &amp;Ledger::postEntry);</code></pre>

13. **Q:** Why must pybind11 code explicitly release the GIL before running a long, CPU-bound C++ computation?
   **A:** By default the GIL stays held during the C++ call, blocking every other Python thread. Releasing it lets other Python threads run concurrently while the C++ work executes.

14. **Q:** Which pybind11 type lets a C++ function accept or return a NumPy array without copying its data?
   **A:** <code>py::array_t&lt;T&gt;</code> (from <code>&lt;pybind11/numpy.h&gt;</code>).

15. **Q:** What tool exposed BMO's C++20 financial calculation engine to Python callers?
   **A:** pybind11 bindings.

16. **Q:** Write the minimal CMakeLists.txt to build a C++20 executable named "app" from main.cpp.
   **A:** <pre><code>cmake_minimum_required(VERSION 3.20)
project(app LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(app main.cpp)</code></pre>

17. **Q:** What does target_link_libraries(target PRIVATE dep) do, and what does the PRIVATE/PUBLIC/INTERFACE keyword control?
   **A:** Links `dep` into `target` and propagates its include dirs/compile flags; PRIVATE = used only inside target's own build, PUBLIC = also propagated to anything that links target, INTERFACE = propagated but not used by target itself.

## Cloze cards

- C++20 {{c1::concepts}} constrain template parameters with named, checkable requirements, giving much clearer compiler errors than <code>std::enable_if</code>/SFINAE.
- <code>constexpr</code> marks a function/variable that {{c1::MAY}} be evaluated at compile time (falls back to runtime), while <code>consteval</code> marks an "immediate function" that {{c2::MUST}} be evaluated at compile time.
- CMake's {{c1::CMAKE_BUILD_TYPE}} setting controls optimization: <code>Debug</code> adds symbols and disables optimization, while <code>Release</code> enables optimizations and strips debug info. <!-- Extra: Why use CMake at all? It's a cross-platform build-system generator — one CMakeLists.txt can produce Makefiles, Ninja files, or IDE projects on Linux/macOS/Windows, and it manages dependencies and flags consistently. -->
