---
deck: "Resume Prep::Web & API Fundamentals"
topic: "Web & API Fundamentals"
tags: [ankicardmaker, resume-prep, web-fundamentals]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Web & API Fundamentals — Resume Prep

Source of truth for the `Resume Prep::Web & API Fundamentals` deck (19 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What does "statelessness" mean in REST?
   **A:** Each request from client to server must contain all the information needed to understand and process it. The server keeps no client session state between requests.

2. **Q:** At BMO, 20+ legacy APIs were modernized into serverless AWS Lambda functions behind API Gateway. Why does REST's statelessness constraint matter for that architecture?
   **A:** Because no session state lives on any one server, any Lambda invocation (cold or warm, on any instance) can handle any request. That's what allows API Gateway + Lambda to scale horizontally on demand without sticky sessions or shared in-memory state.

3. **Q:** What's the key difference between PUT and PATCH?
   **A:** PUT replaces the entire resource with the representation sent in the request body. PATCH applies a partial modification to the existing resource.

4. **Q:** What's the difference between HTTP 401 Unauthorized and 403 Forbidden?
   **A:** 401 means the request has no (or invalid) authentication credentials. 403 means the credentials are valid, but that identity isn't allowed to access the resource.

5. **Q:** Why is JSON the dominant payload format for REST APIs, more than XML?
   **A:** It's lightweight and maps directly onto native objects/arrays in JS and most languages, so it's cheap to parse and produces smaller payloads than the more verbose, tag-heavy XML format.

6. **Q:** What problem does CORS (Cross-Origin Resource Sharing) solve, and who enforces it?
   **A:** <p>It lets a server explicitly allow a web page loaded from one origin (scheme+host+port) to make requests to a different origin, which browsers block by default (the same-origin policy).</p><p>CORS is enforced by the <b>browser</b>, not the server — the server just sends headers like <code>Access-Control-Allow-Origin</code>. For "non-simple" requests, the browser first sends an automatic <code>OPTIONS</code> preflight request to check permission before the real request.</p>

7. **Q:** Authentication *(reversed — tested both ways)*
   **A:** Verifying <i>who</i> a user or system is — confirming identity (e.g. via password, token, certificate).

8. **Q:** Authorization *(reversed — tested both ways)*
   **A:** Verifying <i>what</i> an already-authenticated identity is allowed to do — checking permissions/access rights.

9. **Q:** What three parts make up a JWT (JSON Web Token)?
   **A:** <p>A base64url-encoded <b>Header</b>.<b>Payload</b>.<b>Signature</b>, dot-separated:</p><pre><code>eyJhbGciOiJIUzI1NiJ9.  &lt;- header (alg, type)
eyJzdWIiOiIxMjM0In0.    &lt;- payload (claims)
SflKxwRJSMeKKF2QT4fw    &lt;- signature</code></pre>

10. **Q:** How does a server trust a JWT's claims without a database lookup?
   **A:** It recomputes the signature over the header+payload using its secret (HMAC) or public key (RSA/ECDSA) and checks it matches the token's signature. If it matches, the header and payload haven't been tampered with since they were signed.

11. **Q:** Architecturally, what's the core difference between session-based auth and token-based (JWT) auth?
   **A:** Sessions store state server-side (a session ID maps to data in memory or a shared store), requiring a lookup on every request and often sticky routing. JWTs are self-contained and stateless — any server instance can validate one on its own, which fits horizontally-scaled/serverless APIs better.

12. **Q:** What's a security trade-off of storing a JWT in localStorage vs. an httpOnly cookie?
   **A:** localStorage is readable by any JavaScript on the page, so an XSS bug can steal the token. An httpOnly cookie can't be read by JS (mitigating XSS theft) but is sent automatically by the browser, making it vulnerable to CSRF unless mitigated (e.g. SameSite, CSRF tokens).

13. **Q:** What does HTTPS add on top of plain HTTP, and how is the connection secured?
   **A:** TLS encryption of the traffic. The TLS handshake uses asymmetric crypto (the server's certificate/public key) to safely negotiate a symmetric session key, which then encrypts the actual data — giving confidentiality, integrity, and server authentication.

14. **Q:** What is the purpose of API rate limiting?
   **A:** To cap how many requests a client can make in a given time window, protecting the backend from overload/abuse and keeping usage fair across clients (often returning 429 Too Many Requests once exceeded).

15. **Q:** Name two common ways to version a REST API.
   **A:** URI versioning (e.g. <code>/v1/orders</code>, <code>/v2/orders</code>) or header-based versioning (e.g. a custom <code>Api-Version</code> header or an <code>Accept</code> media-type parameter), so breaking changes don't disrupt existing clients.

## Cloze cards

- REST's architectural constraints include: {{c1::client-server}} separation, {{c2::statelessness}}, {{c3::cacheability}}, a {{c4::uniform interface}}, and a {{c5::layered system}}. <!-- Back Extra: An optional sixth constraint is 'code on demand' (rarely used in practice). -->
- Idempotent HTTP methods (repeating the request leaves the server in the same state as doing it once): {{c1::GET}}, {{c2::PUT}}, {{c3::DELETE}}, {{c4::HEAD}}. {{c5::POST}} is generally NOT idempotent. <!-- Back Extra: PATCH is also generally not idempotent, since it can apply an incremental change (e.g. "increment counter by 1") that produces a different result each time it's repeated. -->
- HTTP status code ranges: {{c1::2xx}} = success, {{c2::3xx}} = redirection, {{c3::4xx}} = client error, {{c4::5xx}} = server error. <!-- Back Extra: A REST API creating a resource via POST should return 201 Created, with a Location header pointing at the new resource's URI. -->
- Common HTTP headers: {{c1::Authorization}} carries credentials such as a Bearer token; {{c2::Content-Type}} describes the media type of the request/response body (e.g. application/json); {{c3::Accept}} tells the server what response format(s) the client can handle.
