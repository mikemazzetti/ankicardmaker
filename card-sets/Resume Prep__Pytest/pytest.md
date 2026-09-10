---
deck: "Resume Prep::Pytest"
topic: "Pytest"
tags: [ankicardmaker, pytest]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Pytest — Resume Prep

Source of truth for the `Resume Prep::Pytest` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** By default, what filename pattern does pytest use to discover test files?
   **A:** <code>test_*.py</code> or <code>*_test.py</code>.

2. **Q:** By default, what naming rules does pytest use to discover test functions and test classes inside a file?
   **A:** Functions prefixed <code>test_</code>, and classes prefixed <code>Test</code> (with no <code>__init__</code> method) — methods inside them must also start with <code>test_</code>.

3. **Q:** What makes pytest's plain `assert` statements special compared to unittest's assertEqual/assertTrue/etc.?
   **A:** Pytest rewrites plain assert statements at import time to capture and display detailed introspection (actual vs expected values, diffs) on failure — no need for a family of assertX methods.

4. **Q:** What decorator turns a function into a pytest fixture?
   **A:** <code>@pytest.fixture</code>.

5. **Q:** Write a pytest fixture that provides a database connection to tests and closes it afterward.
   **A:** <pre><code>import pytest

@pytest.fixture
def db_conn():
    conn = connect_to_test_db()
    yield conn
    conn.close()

def test_insert(db_conn):
    db_conn.insert({"id": 1})
    assert db_conn.count() == 1</code></pre>

6. **Q:** What is the default scope of a pytest fixture if you don't specify one?
   **A:** <code>function</code> — it's created fresh for every test function that uses it.

7. **Q:** In a pytest fixture, how do you run teardown code after the test that used it finishes?
   **A:** Use <code>yield</code> instead of <code>return</code> — code before <code>yield</code> is setup, code after <code>yield</code> is teardown (runs even if the test fails, like try/finally).

8. **Q:** What decorator runs the same test function multiple times with different sets of input arguments?
   **A:** <code>@pytest.mark.parametrize</code>.

9. **Q:** Write a parametrized pytest test that checks square(n) for several (input, expected) pairs.
   **A:** <pre><code>import pytest

@pytest.mark.parametrize("n, expected", [
    (2, 4),
    (3, 9),
    (-1, 1),
])
def test_square(n, expected):
    assert square(n) == expected</code></pre>

10. **Q:** How do you register a custom pytest marker (e.g. @pytest.mark.slow) so it doesn't trigger an "unknown marker" warning?
   **A:** Declare it under <code>[markers]</code> in <code>pytest.ini</code>/<code>pyproject.toml</code>, or register it programmatically in <code>conftest.py</code> via a <code>pytest_configure</code> hook.

11. **Q:** What is conftest.py used for in pytest?
   **A:** A special file for sharing fixtures and hooks across every test file in its directory and subdirectories — pytest loads it automatically, with no import needed.

12. **Q:** Which built-in pytest fixture lets you patch attributes, environment variables, or dict/os values for a single test, auto-reverting afterward?
   **A:** <code>monkeypatch</code>.

13. **Q:** Write a pytest test that uses monkeypatch to set an environment variable for the duration of the test.
   **A:** <pre><code>def test_uses_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    assert get_client().api_key == "test-key-123"</code></pre>

14. **Q:** How do you assert that a block of code raises a specific exception in pytest?
   **A:** <pre><code>import pytest

def test_raises_on_negative():
    with pytest.raises(ValueError):
        sqrt(-1)</code></pre>

15. **Q:** Which built-in pytest fixture gives each test a unique temporary directory (as a pathlib.Path) that's cleaned up automatically?
   **A:** <code>tmp_path</code>.

16. **Q:** What tool/plugin measures test coverage when running pytest, and how do you invoke it?
   **A:** <code>pytest-cov</code> (built on <code>coverage.py</code>) — run <code>pytest --cov=mypackage</code>.

17. **Q:** What's the main practical advantage of pytest over the standard-library unittest module?
   **A:** Much less boilerplate — plain functions and bare asserts instead of TestCase subclasses and assertX methods — plus powerful fixtures, parametrization, and a large plugin ecosystem; pytest can still discover and run unittest-style tests.

## Cloze cards

- A fixture's {{c1::scope}} parameter (<code>function</code>, <code>class</code>, <code>module</code>, <code>session</code>) controls how often it is set up and torn down.
