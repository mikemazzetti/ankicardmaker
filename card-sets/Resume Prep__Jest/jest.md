---
deck: "Resume Prep::Jest"
topic: "Jest"
tags: [ankicardmaker, resume-prep, jest]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Jest — Resume Prep

Source of truth for the `Resume Prep::Jest` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What Jest function groups related test cases together under a shared label?
   **A:** <code>describe(name, fn)</code>

2. **Q:** What's the difference between Jest's <code>it()</code> and <code>test()</code> functions?
   **A:** None functionally &mdash; <code>it</code> is just an alias for <code>test</code>; both define a single test case. <code>it</code> reads naturally in sentences ("it should...").

3. **Q:** Write a Jest test asserting <code>sum(2, 3)</code> equals 5.
   **A:** <pre><code>test('adds 2 + 3 to equal 5', () =&gt; {
  expect(sum(2, 3)).toBe(5);
});</code></pre>

4. **Q:** What's the difference between Jest's <code>toBe</code> and <code>toEqual</code> matchers?
   **A:** <code>toBe</code> checks strict equality (<code>Object.is</code>, so reference equality for objects); <code>toEqual</code> recursively checks deep structural equality, so two different objects with the same fields pass <code>toEqual</code> but fail <code>toBe</code>.

5. **Q:** Write a Jest test that creates a mock function, calls it with 'hello', and asserts it was called with that argument.
   **A:** <pre><code>const callback = jest.fn();
callback('hello');
expect(callback).toHaveBeenCalledWith('hello');</code></pre>

6. **Q:** What does <code>jest.fn()</code> create?
   **A:** A mock function you can pass around (e.g. as a callback/prop) and later assert on &mdash; how many times it was called, what arguments it received, and control what it returns.

7. **Q:** What does <code>jest.mock('./module')</code> do to that module in the current test file?
   **A:** Auto-mocks it: every exported function becomes a <code>jest.fn()</code> stub, replacing the real implementation, so the test isn't affected by the module's actual behavior (e.g. real network/DB calls).

8. **Q:** How do you make a Jest mock function return a given value only on its <em>next</em> call?
   **A:** <code>mockFn.mockReturnValueOnce(value)</code>

9. **Q:** What is Jest snapshot testing used for?
   **A:** Serializing a component's/value's output once, saving it to a snapshot file, and automatically comparing future test runs against it &mdash; a diff means the output changed unexpectedly.

10. **Q:** Write a Jest snapshot test for a rendered <code>&lt;Greeting name="Ada" /&gt;</code> component.
   **A:** <pre><code>import renderer from 'react-test-renderer';

test('renders correctly', () =&gt; {
  const tree = renderer
    .create(&lt;Greeting name="Ada" /&gt;)
    .toJSON();
  expect(tree).toMatchSnapshot();
});</code></pre>

11. **Q:** Write a Jest test asserting that <code>riskyAsync()</code> rejects with an error.
   **A:** <pre><code>test('riskyAsync rejects', async () =&gt; {
  await expect(riskyAsync()).rejects.toThrow();
});</code></pre>

12. **Q:** Write a Jest test for an async function <code>fetchUser(1)</code> that resolves to <code>{ id: 1 }</code>.
   **A:** <pre><code>test('fetchUser resolves with user data', async () =&gt; {
  const data = await fetchUser(1);
  expect(data).toEqual({ id: 1 });
});</code></pre>

13. **Q:** In React Testing Library, what function renders a component into a virtual DOM for testing?
   **A:** <code>render(&lt;Component /&gt;)</code>, from <code>@testing-library/react</code>.

14. **Q:** What's React Testing Library's core querying philosophy &mdash; how should you find elements in a test?
   **A:** Query the way a user would perceive the page (by accessible role, label, or visible text via <code>getByRole</code>/<code>getByLabelText</code>/<code>getByText</code>), not by implementation details like class names or component internals.

15. **Q:** Write an RTL test that renders a <code>&lt;Button onClick={onClick} /&gt;</code>, clicks it, and asserts the handler fired once.
   **A:** <pre><code>test('calls onClick when clicked', () =&gt; {
  const onClick = jest.fn();
  render(&lt;Button onClick={onClick} /&gt;);
  fireEvent.click(screen.getByRole('button'));
  expect(onClick).toHaveBeenCalledTimes(1);
});</code></pre>

16. **Q:** What does running Jest with the <code>--coverage</code> flag report?
   **A:** Code coverage percentages for statements, branches, functions, and lines that were actually executed by the test suite.

17. **Q:** Which Jest matcher checks that an array or string includes a given item/substring?
   **A:** <code>toContain</code>, e.g. <code>expect(['a','b']).toContain('a')</code>.

## Cloze cards

- Jest's {{c1::beforeEach}} runs before every test in its scope, {{c2::afterEach}} runs after every test, and {{c3::beforeAll}} / {{c4::afterAll}} each run only once for the whole describe block.
