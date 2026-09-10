---
deck: "System Design::Search Autocomplete (Typeahead)"
topic: "Search Autocomplete (Typeahead)"
tags: [ankicardmaker, sd-typeahead]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Search Autocomplete (Typeahead) — System Design

Source of truth for the `System Design::Search Autocomplete (Typeahead)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What is the core functional requirement of a search-typeahead system?
   **A:** Given a partial query prefix, return the top-k most relevant completed suggestions in real time as the user types.

2. **Q:** If a typeahead service handles 10,000 searches/sec and each keystroke can trigger its own request, roughly how many requests/sec hit the backend for a 5-character average query?
   **A:** ~50,000 requests/sec (10,000 × 5 keystrokes), since each keystroke can fire its own prefix lookup.

3. **Q:** Why do typeahead clients debounce/throttle keystroke requests?
   **A:** To avoid firing a backend request on every single keystroke, cutting request volume significantly while still feeling instant to the user.

4. **Q:** What does GET /suggestions?prefix=abc&limit=5 return?
   **A:** An ordered list of the top 5 suggested completions for the prefix 'abc', ranked by relevance/popularity.

5. **Q:** Trie (prefix tree) *(reversed — both ways)*
   **A:** A tree data structure where each path from the root spells out a string/term, enabling efficient prefix-based lookups.

6. **Q:** What additional data does each trie node/terminal store beyond the character itself, to support ranking?
   **A:** A frequency/popularity score (e.g. query count) for terms ending at or passing through that node, used to rank suggestions.

7. **Q:** Why is a plain trie alone often insufficient for production-scale typeahead over millions of terms?
   **A:** Traversing the full subtree under a prefix to find the top-k at query time is too slow; each node needs to precompute its own top-k so lookups are O(prefix length).

8. **Q:** What's the standard technique to make top-k retrieval at each trie node O(1) instead of scanning the whole subtree?
   **A:** Precompute and cache the top-k highest-scoring completions at every node during trie construction (bottom-up), so a query just reads that cached list.

9. **Q:** What data structure efficiently maintains the top-k items while merging children's top-k lists during offline trie construction?
   **A:** A min-heap of size k per node — new candidates from children are compared against the heap's minimum and swapped in if larger.

10. **Q:** Why cache popular prefixes (e.g. 'a', 'ap', 'app') at a fast cache layer in front of the trie service?
   **A:** A small number of short, high-frequency prefixes account for a disproportionate share of traffic (Zipfian), so caching them in Redis/CDN cuts trie-service load dramatically.

11. **Q:** Besides raw historical frequency, what signal helps rank typeahead suggestions for freshness (e.g. breaking news)?
   **A:** A time-decayed or recency-weighted score that boosts recently trending queries over older, high-frequency but stale ones.

12. **Q:** What personalization signal can re-rank typeahead suggestions per user?
   **A:** The user's own search history/context (location, past queries), blended with global popularity.

13. **Q:** Why rebuild the trie offline/periodically (e.g. every few minutes to hours) rather than updating it on every single query?
   **A:** Updating a shared ranked trie in real time under heavy read concurrency is expensive and complex; batch rebuilding keeps serving simple and fast while accepting slightly stale rankings.

14. **Q:** What might a typeahead trie node's struct look like, conceptually?
   **A:** <pre><code>class TrieNode {
  Map&lt;Character, TrieNode&gt; children;
  List&lt;String&gt; topK; // precomputed top-k completions
}</code></pre>

15. **Q:** What is the main scaling bottleneck when the full trie for millions of terms can't fit in one machine's memory?
   **A:** Memory capacity — the trie must be sharded, commonly by the first character(s) of the prefix, across multiple servers.

16. **Q:** What problem does sharding a trie by first letter create, and what's a mitigation?
   **A:** Uneven load since some letters (e.g. 's') are far more common than others; mitigate by sharding on a hash of a longer prefix or rebalancing shard boundaries based on traffic.

17. **Q:** What's the tradeoff of a longer trie-rebuild interval (e.g. daily vs every 5 minutes)?
   **A:** Lower system load and cost, but suggestions lag further behind real trending/newly popular queries.

18. **Q:** What's the tradeoff between exact-prefix matches only vs fuzzy/typo-tolerant matches?
   **A:** Fuzzy matching improves recall for misspellings but adds significant query-time complexity/latency (e.g. edit-distance search) versus a simple, very fast trie prefix walk.

19. **Q:** Why might a typeahead system trade strict consistency for eventual consistency across regions?
   **A:** New trending terms propagating a few minutes late to some regions is an acceptable tradeoff for keeping per-region latency low and services independently available.

## Cloze cards

- Typeahead systems require {{c1::very low latency}} (typically under 100ms), {{c2::high availability}}, and {{c3::freshness}} (trending queries surface quickly), often relaxing {{c4::strict consistency}}.
- Core components: a {{c1::query log aggregation pipeline}} (collects search frequency), an {{c2::offline trie-builder job}} (builds a ranked trie periodically), a {{c3::trie-serving cache layer}}, and an {{c4::API/load balancer}} in front of clients.
- The typeahead freshness pipeline is typically: {{c1::search queries logged in real time}} → {{c2::aggregated into frequency counts via stream processing}} → {{c3::periodically rebuilt into an updated trie}} → {{c4::the new trie is swapped into the serving layer}}.
