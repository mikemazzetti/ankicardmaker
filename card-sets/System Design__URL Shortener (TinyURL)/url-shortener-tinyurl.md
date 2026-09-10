---
deck: "System Design::URL Shortener (TinyURL)"
topic: "URL Shortener (TinyURL)"
tags: [ankicardmaker, sd-url-shortener]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# URL Shortener (TinyURL) — System Design

Source of truth for the `System Design::URL Shortener (TinyURL)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Should short URLs in a URL shortener system expire?
   **A:** Optionally yes &mdash; support a configurable expiration/TTL per link, after which the short link becomes invalid.

2. **Q:** Why must a URL shortener prioritize availability over strong consistency?
   **A:** Redirects are on the critical read path for every click; an outage breaks all shared links, so the system favors AP (availability) in the CAP tradeoff, tolerating brief staleness of newly created links across replicas.

3. **Q:** In a typical URL shortener capacity estimate, if there are 100M new URLs created per month, what is the approximate write QPS?
   **A:** ~40 writes/sec (100,000,000 / (30&times;24&times;3600) &asymp; 38.6 &asymp; ~40 QPS).

4. **Q:** If the read:write ratio for a URL shortener is 100:1 and write QPS is ~40, what is the approximate read QPS?
   **A:** ~4,000 QPS (100 &times; 40).

5. **Q:** Estimate storage needed for 100M URLs/month over 5 years if each record is ~500 bytes.
   **A:** 100M &times; 12 &times; 5 = 6B records &times; 500 bytes &asymp; 3 TB total.

6. **Q:** Write the REST endpoint to create a short URL, given a long URL and optional custom alias/expiration.
   **A:** <pre><code>POST /api/v1/shorten
Request body: { "longUrl": "string", "customAlias": "string (optional)", "expiresAt": "datetime (optional)" }
Response: { "shortUrl": "string" }</code></pre>

7. **Q:** Write the REST endpoint used to redirect a short URL to its long URL.
   **A:** <pre><code>GET /{shortCode}
Response: 301/302 redirect to longUrl</code></pre>

8. **Q:** Should the redirect endpoint use a 301 or 302 HTTP status, and why does it matter?
   **A:** 302 (temporary redirect) is generally preferred &mdash; it keeps every click hitting the server for analytics. 301 (permanent) lets browsers cache the redirect, saving server load but losing per-click analytics.

9. **Q:** Write a minimal schema for the <code>urls</code> table in a URL shortener.
   **A:** <pre><code>urls(
  short_code VARCHAR(7) PRIMARY KEY,
  long_url   TEXT NOT NULL,
  user_id    BIGINT,
  created_at TIMESTAMP,
  expires_at TIMESTAMP NULL
)</code></pre>

10. **Q:** Why is a key-value store (e.g. DynamoDB/Cassandra) often preferred over a relational DB for the URL mapping table?
   **A:** The access pattern is a simple key lookup (short_code &rarr; long_url) at huge read scale with no complex joins/transactions needed, so a KV store scales horizontally more easily and cheaply than a relational DB.

11. **Q:** Why add a cache (e.g. Redis) in front of the URL mapping database?
   **A:** Redirect traffic follows a hot-key distribution &mdash; a small percentage of URLs get most of the clicks &mdash; so caching hot mappings drastically cuts database read load and latency.

12. **Q:** What alphabet does base62 encoding use for short URL codes?
   **A:** 62 characters: a-z, A-Z, 0-9 (26+26+10).

13. **Q:** How many unique short codes does a 7-character base62 string provide?
   **A:** 62^7 &asymp; 3.5 trillion unique codes.

14. **Q:** Describe the counter + base62 approach to generating short URLs.
   **A:** Maintain a globally unique, monotonically increasing counter (e.g. via a distributed ID generator or a DB auto-increment range), then base62-encode the counter value to produce the short code &mdash; this guarantees uniqueness with no collision checking needed.

15. **Q:** What is a drawback of using a simple auto-increment counter for short codes, and how is it mitigated?
   **A:** Sequential codes are predictable/guessable, letting users enumerate all URLs. Mitigate by pre-shuffling the ID space (e.g. a random permutation, or hashing the counter before encoding) so codes appear random while staying unique.

16. **Q:** Describe the alternative hash-based (MD5/SHA + truncate) approach to generating short codes, and its main problem.
   **A:** Hash the long URL (e.g. MD5), base62-encode it, and take the first 7 characters. Problem: truncated hashes can collide, so you must check the DB for an existing code and retry with a salt/suffix on collision.

17. **Q:** How can the database layer be scaled once a single instance can't handle URL mapping read volume?
   **A:** Horizontally shard the key-value store (e.g. by a hash of short_code) and add read replicas, so reads are distributed across many nodes.

18. **Q:** What is the main tradeoff when choosing a 301 (permanent) redirect over a 302 for short links?
   **A:** 301 improves performance (browsers cache it, reducing server hits) but sacrifices the ability to track every click for analytics, since cached redirects never reach the server again.

## Cloze cards

- The two core functional requirements of a URL shortener are: {{c1::generate a unique short URL for a given long URL}} and {{c2::redirect a short URL to its original long URL}}.
- Non-functional requirements for a URL shortener include {{c1::high availability}}, {{c2::low latency redirection}}, and {{c3::the short URL should not be easily predictable/guessable}}.
- The high-level architecture of a URL shortener typically includes: {{c1::a load balancer}}, {{c2::stateless application servers}}, {{c3::a key-value store for URL mappings}}, and {{c4::a cache layer (e.g. Redis) in front of the database}}.
- Key scaling bottlenecks in a URL shortener and their fixes: {{c1::hot-key read traffic}} is fixed by {{c2::a caching layer (e.g. Redis) plus CDN edge caching}}; {{c3::a single ID-generation service becoming a bottleneck}} is fixed by {{c4::pre-allocating ID ranges per server or using a distributed ID generator like Snowflake}}.
