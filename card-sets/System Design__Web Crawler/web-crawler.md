---
deck: "System Design::Web Crawler"
topic: "Web Crawler"
tags: [ankicardmaker, sd-web-crawler]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Web Crawler — System Design

Source of truth for the `System Design::Web Crawler` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why is a web crawler designed for eventual freshness rather than strict real-time accuracy?
   **A:** The web changes constantly and is enormous, so a crawler can never have a perfectly up-to-date snapshot; it instead optimizes for periodically refreshing important or frequently-changing pages rather than guaranteeing real-time accuracy.

2. **Q:** If a crawler needs to crawl 1 billion pages per month, what is the approximate average crawl QPS?
   **A:** 1B / (30 x 86,400) ≈ 386 pages/sec on average, burstier in practice and split across many parallel workers.

3. **Q:** If the average page size is 500KB and the crawler stores 1 billion pages, what is the approximate raw storage requirement?
   **A:** 1B x 500KB = 500TB, before compression and replication.

4. **Q:** What would a typical internal API call from the crawler's scheduler to a fetcher worker look like?
   **A:** <pre><code>POST /fetch
{ url, crawlDepth, politenessDelay }
-&gt; returns { statusCode, htmlBody, headers }</code></pre>

5. **Q:** What internal endpoint would the content-processing service expose to receive raw fetched pages?
   **A:** <code>POST /pages/process</code>, accepting raw HTML plus the URL, and triggering parsing, dedup checking, and link extraction.

6. **Q:** Why store a content hash (e.g. SHA-256 of the page body) rather than comparing full page text for duplicate detection?
   **A:** Comparing fixed-length hashes is far cheaper, constant-time comparison and small storage, than comparing full HTML documents, while still reliably detecting exact duplicate content.

7. **Q:** Why does a crawler maintain its own DNS cache instead of relying on the OS resolver for every request?
   **A:** DNS lookups are relatively slow and a crawler issues an enormous volume of requests to many domains, so a local cache avoids repeated lookup latency and reduces load on DNS servers.

8. **Q:** Why is BFS generally preferred over DFS for the crawl frontier's traversal order?
   **A:** BFS discovers a broad, diverse set of pages early and naturally limits how deep any single crawl trap or link chain can pull the crawler before other sites get visited; DFS can get stuck following one deep path indefinitely.

9. **Q:** What is the purpose of respecting a site's robots.txt file?
   **A:** It specifies which paths a site owner disallows crawlers from accessing; respecting it is the standard politeness convention and avoids legal/ethical issues and IP bans.

10. **Q:** Besides robots.txt, what other mechanism enforces politeness toward a single web server?
   **A:** A per-host minimum delay between consecutive requests, and/or limiting concurrent connections per host, so the crawler doesn't overwhelm any one server with simultaneous requests.

11. **Q:** What is a Bloom filter and why is it used for URL dedup in a large-scale crawler?
   **A:** A probabilistic set-membership structure that uses far less memory than storing every visited URL exactly, at the cost of a small false-positive rate where it may wrongly claim a URL was already seen; ideal when memory efficiency matters more than perfect accuracy at billions-of-URLs scale.

12. **Q:** What is a crawler trap?
   **A:** A site structure such as infinite calendar pages, dynamically generated links, or session-ID URLs that generates an effectively infinite number of unique-looking URLs, which can trap a crawler in an endless loop if not detected.

13. **Q:** Name two mitigation strategies against crawler traps.
   **A:** Capping the maximum crawl depth per site, and limiting the number of pages crawled per domain, plus flagging URL patterns whose parameters or length grow unboundedly.

14. **Q:** What is the primary scaling bottleneck of a naive single-queue URL frontier at web scale?
   **A:** A single shared queue becomes a contention and throughput bottleneck and cannot enforce per-host politeness efficiently; the fix is partitioning the frontier into per-host queues distributed across multiple frontier servers or shards.

15. **Q:** What is the tradeoff of using a Bloom filter for dedup vs. an exact set (e.g. a hash set backed by a database)?
   **A:** A Bloom filter uses vastly less memory and is fast but allows a small false-positive rate that may wrongly skip a genuinely new URL; an exact set guarantees correctness but does not scale to tens of billions of URLs in memory.

## Cloze cards

- Core functional requirements for a web crawler: {{c1::discover and fetch web pages}} starting from seed URLs, {{c2::extract and store content}}, and {{c3::extract new links}} to crawl next.
- Key non-functional requirements: {{c1::scalability}} to billions of pages, {{c2::politeness}} (don't overload any single site), {{c3::extensibility}} for new content types, and {{c4::avoiding infinite loops/traps}}.
- A crawled-URL record typically stores the {{c1::URL}}, a {{c2::content hash/checksum}} (for dedup), a {{c3::last-crawled timestamp}}, and a {{c4::crawl status}} (pending/fetched/failed).
- Core components of a web crawler architecture: {{c1::URL frontier (queue)}}, {{c2::fetcher workers}}, {{c3::DNS resolver/cache}}, {{c4::content parser/extractor}}, {{c5::duplicate detector}}, and {{c6::storage}} for pages and metadata.
- The URL frontier is often implemented as {{c1::multiple priority queues}} (one per host or priority tier) feeding into {{c2::per-host queues}} that enforce a {{c3::politeness delay}} between requests to the same domain.
