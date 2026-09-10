---
deck: "Resume Prep::Node.js & Express"
topic: "Node.js & Express"
tags: [ankicardmaker, resume-prep, node-express]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Node.js & Express — Resume Prep

Source of truth for the `Resume Prep::Node.js & Express` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why is Node.js described as non-blocking / asynchronous I/O?
   **A:** Node uses a single-threaded event loop plus libuv's thread pool: I/O operations (file, network, DB) are dispatched and their callbacks run later when complete, so the main thread never blocks waiting on them.

2. **Q:** What is the Node.js event loop?
   **A:** A loop that continuously checks for and executes queued callbacks (timers, I/O completions, immediates) in phases, letting a single JS thread handle many concurrent operations without blocking.

3. **Q:** What's the key difference between CommonJS <code>require()</code> and ES Modules <code>import</code> in Node.js?
   **A:** <code>require()</code> loads modules synchronously and resolves at call time (can be conditional/dynamic); ESM <code>import</code> is statically analyzed at parse time and needs <code>"type": "module"</code> or a <code>.mjs</code> extension to use natively.

4. **Q:** How do you code a minimal Express server with a GET route?
   **A:** <pre><code>const express = require('express');
const app = express();

app.get('/health', (req, res) =&gt; {
  res.status(200).json({ status: 'ok' });
});

app.listen(3000);</code></pre>

5. **Q:** What is Express middleware?
   **A:** A function with the signature <code>(req, res, next)</code> that runs during the request/response cycle — it can inspect or modify req/res, end the cycle, or call <code>next()</code> to pass control to the next middleware.

6. **Q:** How do you code Express middleware that logs each request's method and URL?
   **A:** <pre><code>app.use((req, res, next) =&gt; {
  console.log(`${req.method} ${req.url}`);
  next();
});</code></pre>

7. **Q:** How do you code Express error-handling middleware, and what makes it different from regular middleware?
   **A:** It takes four arguments (err first); Express recognizes this arity and routes errors passed to <code>next(err)</code> here.<pre><code>app.use((err, req, res, next) =&gt; {
  console.error(err);
  res.status(500).json({ error: 'Internal error' });
});</code></pre>

8. **Q:** In an Express route handler, what do <code>req.params</code>, <code>req.query</code>, and <code>req.body</code> each represent?
   **A:** <code>req.params</code>: named URL path segments (e.g. <code>/users/:id</code>); <code>req.query</code>: the URL's query string key/values; <code>req.body</code>: the parsed request payload (needs a body-parsing middleware like <code>express.json()</code>).

9. **Q:** How do you code an Express route that reads a route param and a query param?
   **A:** <pre><code>app.get('/users/:id', (req, res) =&gt; {
  const { id } = req.params;
  const { active } = req.query;
  res.json({ id, active });
});</code></pre>

10. **Q:** What is a Node.js stream, and why use one for large files instead of reading the whole file into memory?
   **A:** A stream processes data in chunks over time (Readable, Writable, Duplex, Transform); it keeps memory usage low and lets processing start before the whole source has been read, unlike <code>fs.readFile</code>.

11. **Q:** How do you code piping a file read stream to an HTTP response in Node.js?
   **A:** <pre><code>const fs = require('fs');

app.get('/download', (req, res) =&gt; {
  fs.createReadStream('report.csv').pipe(res);
});</code></pre>

12. **Q:** What does the <code>package.json</code> <code>"dependencies"</code> vs <code>"devDependencies"</code> distinction control?
   **A:** <code>dependencies</code> are required at runtime in production; <code>devDependencies</code> are only needed for development, build, or test tooling and aren't installed with <code>npm install --production</code>.

13. **Q:** What does <code>package-lock.json</code> guarantee that a version range in <code>package.json</code> (e.g. <code>^4.2.0</code>) doesn't?
   **A:** It pins the exact resolved version (and full dependency tree) that was installed, so every install reproduces identical dependency versions across machines and CI.

14. **Q:** What's the idiomatic way to load environment-specific config (like DB URLs or API keys) into a Node.js app?
   **A:** Read from <code>process.env</code>, typically populated via a <code>.env</code> file loaded with a package like <code>dotenv</code> in development, and via real environment variables injected by the platform/CI in production — keeping secrets out of source control.

15. **Q:** Why can a single slow synchronous CPU-bound function block an entire Node.js server, even though I/O is non-blocking?
   **A:** Node runs JS on a single main thread; a long synchronous computation occupies that thread, so the event loop can't process other pending callbacks (other requests) until it finishes.

16. **Q:** In a Discord bot doing CRUD against a SQL backend (Node.js), why use parameterized queries instead of string-concatenating user input into SQL?
   **A:** Parameterized queries send user input separately from the SQL statement so the driver escapes it, preventing SQL injection from untrusted Discord command input.

17. **Q:** For a BMO-style Node.js backend modernized into serverless AWS Lambda functions, why does minimizing an Express app's dependencies matter for cold starts?
   **A:** Each Lambda cold start must load and initialize the Node.js runtime and all required modules before handling the first request, so fewer/lighter dependencies directly reduce cold-start latency.

## Cloze cards

- The Node.js event loop processes phases in this order each tick: {{c1::timers}} → pending callbacks → idle/prepare → {{c2::poll}} (I/O) → {{c3::check}} (setImmediate) → close callbacks.
