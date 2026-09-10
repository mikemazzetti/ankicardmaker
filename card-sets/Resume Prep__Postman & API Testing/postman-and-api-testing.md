---
deck: "Resume Prep::Postman & API Testing"
topic: "Postman & API Testing"
tags: [ankicardmaker, resume-prep, api-testing]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# Postman & API Testing — Resume Prep

Source of truth for the `Resume Prep::Postman & API Testing` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** When should you use HTTP <code>GET</code>?
   **A:** To retrieve a resource without causing side effects. Safe (no server state change) and idempotent; no request body.

2. **Q:** When should you use HTTP <code>POST</code>?
   **A:** To create a new resource or trigger a non-idempotent action (e.g. submit an order). Not safe, not guaranteed idempotent &mdash; repeating it can create duplicates.

3. **Q:** When should you use HTTP <code>PUT</code>?
   **A:** To replace a resource entirely at a known URI. Idempotent: sending the same PUT twice leaves the resource in the same state as sending it once.

4. **Q:** When should you use HTTP <code>PATCH</code>?
   **A:** To apply a partial update to a resource (only the changed fields). Not guaranteed idempotent &mdash; depends on how the server implements the patch.

5. **Q:** When should you use HTTP <code>DELETE</code>?
   **A:** To remove the resource at a given URI. Idempotent: deleting an already-deleted resource still leaves it gone.

6. **Q:** Idempotent (HTTP request) *(reversed — tested both ways)*
   **A:** Making the identical request multiple times leaves the server in the same state as making it once. GET, PUT, and DELETE are idempotent; POST is not.

7. **Q:** What status code should a successful <code>POST</code> that creates a new resource return?
   **A:** <code>201 Created</code> (often with a <code>Location</code> header pointing to the new resource).

8. **Q:** What status code means the request succeeded but there is no body to send back (e.g. a successful DELETE)?
   **A:** <code>204 No Content</code>

9. **Q:** What's the difference between <code>401 Unauthorized</code> and <code>403 Forbidden</code>?
   **A:** 401 = the request lacks valid authentication ("who are you?"). 403 = the server knows who you are but you don't have permission for this resource ("you can't do that").

10. **Q:** What does a <code>429</code> status code indicate?
   **A:** Too Many Requests &mdash; the client has exceeded a rate limit and should back off/retry later (often per a <code>Retry-After</code> header).

11. **Q:** What are the main components you configure on a request in Postman?
   **A:** Method + URL, query Params, Headers, Body (raw/JSON/form-data), and Authorization.

12. **Q:** In Postman, what's the difference between a Collection and an Environment?
   **A:** A Collection groups related requests together (plus their scripts/tests, run in sequence). An Environment holds a set of variables (base URL, tokens, IDs) that requests reference, so you can switch the same collection between dev/staging/prod by swapping environments.

13. **Q:** Write a Postman test script asserting the response status code is 200.
   **A:** <pre><code>pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});</code></pre>

14. **Q:** Write a Postman test script asserting the JSON response body has an <code>id</code> property.
   **A:** <pre><code>pm.test("Response has id property", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
});</code></pre>

15. **Q:** How do you save a value from a Postman response (e.g. an auth token) into an environment variable for later requests to use?
   **A:** <pre><code>pm.environment.set("token", pm.response.json().token);</code></pre> Later requests can then reference it as <code>{{token}}</code>.

16. **Q:** What's the difference between Bearer Token auth and Basic auth?
   **A:** Basic auth sends a base64-encoded <code>username:password</code> on every request. Bearer auth sends a previously-issued token (e.g. JWT from OAuth/login) in the <code>Authorization</code> header, without resending raw credentials each time.

17. **Q:** In Postman, what are pre-request scripts used for?
   **A:** JavaScript that runs before the request is sent &mdash; e.g. computing a timestamp/signature, generating dynamic test data, or setting an auth header/variable that the request needs.

## Cloze cards

- HTTP status codes are grouped by their first digit: {{c1::2xx}} = success, {{c2::3xx}} = redirection, {{c3::4xx}} = client error, {{c4::5xx}} = server error.
