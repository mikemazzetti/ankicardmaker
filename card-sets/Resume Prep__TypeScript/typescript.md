---
deck: "Resume Prep::TypeScript"
topic: "TypeScript"
tags: [ankicardmaker, resume-prep, typescript]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# TypeScript — Resume Prep

Source of truth for the `Resume Prep::TypeScript` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the main practical difference between <code>type</code> and <code>interface</code> in TypeScript for object shapes?
   **A:** <code>interface</code>s can be reopened and merged via declaration merging; <code>type</code> aliases cannot be merged but can express unions, intersections, and other non-object types that <code>interface</code> can't.

2. **Q:** How do you code a generic function <code>first</code> that returns the first element of an array of any type <code>T</code>?
   **A:** <pre><code>function first<T>(arr: T[]): T {
  return arr[0];
}</code></pre>

3. **Q:** How do you write the intersection type of <code>HasId</code> and <code>HasName</code> as one type?
   **A:** <pre><code>type Entity = HasId & HasName;</code></pre>

4. **Q:** What is the key difference between <code>unknown</code> and <code>any</code> in TypeScript?
   **A:** <code>any</code> disables type checking entirely; <code>unknown</code> is type-safe — you must narrow it (e.g. with a type guard) before you can use it as anything specific.

5. **Q:** How do you narrow a variable <code>value: unknown</code> to a string using <code>typeof</code>?
   **A:** <pre><code>if (typeof value === 'string') {
  console.log(value.toUpperCase());
}</code></pre>

6. **Q:** How do you code a custom type guard function <code>isAdmin</code> that narrows a <code>User</code> to an <code>Admin</code>?
   **A:** <pre><code>function isAdmin(user: User): user is Admin {
  return (user as Admin).permissions !== undefined;
}</code></pre>

7. **Q:** What does the utility type <code>Partial&lt;T&gt;</code> do?
   **A:** It produces a type identical to <code>T</code> but with every property made optional.

8. **Q:** How do you code a type that keeps only the <code>id</code> and <code>email</code> fields from a <code>User</code> type?
   **A:** <pre><code>type UserPreview = Pick<User, 'id' | 'email'>;</code></pre>

9. **Q:** How do you code a type that is <code>User</code> minus its <code>password</code> field?
   **A:** <pre><code>type SafeUser = Omit<User, 'password'>;</code></pre>

10. **Q:** What is a key gotcha of numeric TypeScript enums compared to string enums?
   **A:** Numeric enums are reverse-mapped (both name-to-value and value-to-name exist), and any number is structurally assignable to them, so invalid numeric values can slip through type checking. String enums don't have this problem.

11. **Q:** What does 'structural typing' mean in TypeScript?
   **A:** Type compatibility is based on the shape (members) a type has, not on its declared name — two differently-named types with the same members are interchangeable.

12. **Q:** What does enabling <code>"strict": true</code> in <code>tsconfig.json</code> do?
   **A:** It turns on a bundle of stricter checks, including <code>strictNullChecks</code>, <code>noImplicitAny</code>, and strict function types, catching many more potential bugs at compile time.

13. **Q:** How do you code a discriminated union for a <code>Shape</code> that is either a <code>Circle</code> or a <code>Square</code>, keyed on a <code>kind</code> field?
   **A:** <pre><code>type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'square'; side: number };

function area(s: Shape) {
  return s.kind === 'circle' ? Math.PI * s.radius ** 2 : s.side ** 2;
}</code></pre>

14. **Q:** How do you type the props of a reusable, accessible UI component (e.g. for a WCAG-compliant button library) so it requires an <code>aria-label</code> when there's no visible text child?
   **A:** <pre><code>type ButtonProps =
  | { children: string; 'aria-label'?: string }
  | { children?: never; 'aria-label': string };</code></pre>

15. **Q:** How do you code a generic React component's props type <code>ListProps&lt;T&gt;</code> that takes an array of items and a render function?
   **A:** <pre><code>type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => JSX.Element;
};

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}</code></pre>

16. **Q:** What does the <code>readonly</code> modifier do on a TypeScript interface property?
   **A:** It prevents that property from being reassigned after the object is created, catching accidental mutation at compile time (it does not deep-freeze the object).

17. **Q:** What does appending <code>as const</code> to an array or object literal do to its inferred type?
   **A:** It infers the narrowest possible literal types and makes all properties <code>readonly</code>, instead of widening to general types like <code>string[]</code>.

18. **Q:** What does the <code>never</code> type represent in TypeScript, and where does it commonly show up?
   **A:** A type with no possible values — it shows up as the return type of a function that always throws, and is useful for exhaustiveness checks in a <code>switch</code> over a union.

19. **Q:** How do you write an exhaustiveness check in a <code>switch</code> over a discriminated union so TypeScript errors if a new variant is added later?
   **A:** <pre><code>default: {
  const _exhaustive: never = s;
  throw new Error('Unhandled shape');
}</code></pre>

## Cloze cards

- A {{c1::union}} type (<code>A | B</code>) means a value is A or B; an {{c2::intersection}} type (<code>A & B</code>) means a value must satisfy both A and B at once.
