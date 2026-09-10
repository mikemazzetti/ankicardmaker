---
deck: "System Design::Proximity Service (Nearby)"
topic: "Proximity Service (Nearby)"
tags: [ankicardmaker, sd-proximity]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Proximity Service (Nearby) — System Design

Source of truth for the `System Design::Proximity Service (Nearby)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the two core functional requirements of a Proximity/Nearby-Places service?
   **A:** 1) Given a user's location and a search radius, return nearby places (e.g., restaurants). 2) Business owners can add, update, and delete place data (CRUD).

2. **Q:** Should a proximity service be read-heavy or write-heavy, and why?
   **A:** Read-heavy — millions of users search constantly, but businesses are added/updated/deleted relatively rarely (low write:read ratio).

3. **Q:** If a proximity service has 100M DAU and each user performs 5 nearby-searches per day, what is the average search QPS?
   **A:** 100,000,000 x 5 / 86,400 ~ 5,800 QPS

4. **Q:** With 200M businesses, each needing ~100 bytes for id, name, lat/long, category, roughly how much raw storage is needed for the business dataset?
   **A:** 200,000,000 x 100 bytes ~ 20 GB

5. **Q:** What three endpoints does a proximity service typically expose for business owners to manage listings?
   **A:** <pre><code>POST /v1/business
PUT /v1/business/{id}
DELETE /v1/business/{id}</code></pre>

6. **Q:** What fields does a minimal 'Business' record need in a proximity service data model?
   **A:** business_id, name, category, latitude, longitude, address (plus optional attributes like rating, hours).

7. **Q:** What are the main components in a high-level proximity service architecture?
   **A:** Load balancer, stateless API/search servers, a geospatial index service (geohash/QuadTree), a business database, and a cache for hot queries.

8. **Q:** What is a geohash?
   **A:** An algorithm that encodes a 2D lat/long coordinate into a single alphanumeric string by interleaving bits of latitude and longitude, so nearby locations tend to share string prefixes.

9. **Q:** What is the main weakness of geohash for nearby search, and how is it fixed?
   **A:** Two points can be physically close but have very different geohash prefixes near boundary edges; fixed by also querying the 8 neighboring geohash cells, not just the exact match.

10. **Q:** What is a QuadTree and how does it help nearby search?
   **A:** A tree where each node represents a rectangular region, recursively split into 4 quadrants once a region holds more than a threshold of points — enabling fast range queries by pruning empty/sparse regions.

11. **Q:** Describe the basic algorithm for a 'search nearby places within radius R' query using a geohash index.
   **A:** 1) Compute the geohash of the user's location at a precision matching R. 2) Query that cell plus its 8 neighbors. 3) Filter candidates by exact distance <= R. 4) Return results.

12. **Q:** What is the primary scaling bottleneck as a proximity service's business count and QPS grow?
   **A:** The geospatial index (and DB) becomes too large/hot for a single server, requiring sharding of the geo-index by location and caching of dense/popular regions.

13. **Q:** Why is caching effective for a proximity service, and what should be cached?
   **A:** Search traffic clusters around dense urban geohash cells; caching popular (geohash cell -> nearby business list) query results in Redis/Memcached absorbs most read traffic and reduces DB/index load.

14. **Q:** What consistency tradeoff does a proximity service typically accept, and why is it acceptable?
   **A:** Eventual consistency for business updates (new/changed listings may take seconds to propagate to the index) — acceptable because slightly stale nearby results rarely harm the user experience.

## Cloze cards

- A proximity service favors {{c1::availability}} over strong consistency (slightly stale place data is fine), and demands {{c2::low latency}} — results should return within a couple hundred milliseconds.
- The main read endpoint of a proximity service is typically <pre><code>GET /v1/search?latitude={lat}&amp;longitude={lon}&amp;radius={r}</code></pre> which returns a list of {{c1::nearby place IDs (with distance), not full place details}}.
- Because place data is read-heavy, simple, and doesn't need complex joins or transactions, a proximity service can use either a {{c1::relational DB with geospatial indexing (e.g., PostGIS)}} or a {{c2::purpose-built geo-index/in-memory structure}} for the hot search path.
- Geohash precision is controlled by {{c1::string length}} — each additional character roughly {{c2::quarters the size of the bounding box}}, giving finer resolution.
- Geohash is {{c1::simpler to shard and cache (string-based keys, easy to distribute)}}, while a QuadTree {{c2::adapts to non-uniform data density, giving more balanced regions in dense cities vs. sparse rural areas}}.
- Beyond raw distance, nearby-search ranking typically also factors in {{c1::business rating/popularity}} and {{c1::relevance to the query (category match)}} — not just proximity.
- Because geohash strings encode location as a prefix, a proximity service can shard its geo-index {{c1::by geohash prefix}}, so nearby locations land on the same or adjacent shards, keeping range queries efficient.
- In dense cities, a single geohash cell can become a {{c1::hot spot}} with disproportionate query load; this is mitigated by using {{c2::finer-grained precision in dense areas and/or replicating hot cells across multiple cache nodes}}.
