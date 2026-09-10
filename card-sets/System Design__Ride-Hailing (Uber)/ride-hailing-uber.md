---
deck: "System Design::Ride-Hailing (Uber)"
topic: "Ride-Hailing (Uber)"
tags: [ankicardmaker, sd-uber]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Ride-Hailing (Uber) — System Design

Source of truth for the `System Design::Ride-Hailing (Uber)` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why does driver-rider matching favor low latency over strict global optimality?
   **A:** Riders expect a match within seconds; computing a globally optimal assignment across all drivers and riders would be too slow, so systems use fast local/greedy matching within a geographic cell instead.

2. **Q:** If a ride-hailing app has 5M daily active riders each requesting about 0.5 rides/day, what is the approximate ride-request QPS?
   **A:** 5M x 0.5 / 86,400 ≈ 29 QPS on average (much higher and spikier during rush hour).

3. **Q:** If 3M active drivers each send a location update every 4 seconds, what is the approximate location-update QPS?
   **A:** 3M / 4 ≈ 750,000 updates/sec, the dominant write load in the system.

4. **Q:** Why is location-update traffic, not ride requests, usually the primary scaling bottleneck in ride-hailing systems?
   **A:** Every active driver streams a GPS ping every few seconds continuously, producing orders of magnitude more writes than the comparatively rare ride-request events.

5. **Q:** What API call would a driver's app make to report its current location?
   **A:** <pre><code>POST /drivers/{driverId}/location
{ lat, lng, timestamp, heading }</code></pre>

6. **Q:** What API would a rider's app call to fetch nearby available drivers?
   **A:** <code>GET /riders/nearby-drivers?lat=..&amp;lng=..&amp;radius=..</code> returns a list of candidate drivers for matching.

7. **Q:** Why is driver location data usually stored in-memory (e.g. Redis) rather than in a traditional disk-based relational database?
   **A:** Location changes constantly and must be read/written with very low latency for real-time matching; an in-memory store gives the required speed, and stale entries are quickly overwritten so durability matters less.

8. **Q:** Why do ride-hailing systems partition the world into geographic regions run by separate services?
   **A:** Matching only needs nearby drivers, so partitioning by geography lets each regional service handle a bounded, local dataset independently, enabling horizontal scaling.

9. **Q:** What problem does a geospatial index (QuadTree/geohash) solve in ride-hailing matching?
   **A:** It efficiently answers 'which drivers are within X km of this rider?' without scanning every driver's location, reducing a full table scan to a fast spatial range query.

10. **Q:** What is geohashing?
   **A:** An encoding that maps a (lat, lng) pair into a short base32 string where nearby locations share common string prefixes, enabling proximity search via simple string prefix matching.

11. **Q:** Why does geohash have an edge-case weakness at the boundaries of grid cells?
   **A:** Two points can be physically very close but fall into adjacent geohash cells with completely different prefixes, so a naive prefix search can miss nearby matches near cell edges; mitigated by also checking neighboring cells.

12. **Q:** Why is a greedy 'nearest available driver' approach often preferred over a globally optimal assignment algorithm for matching?
   **A:** Global optimization (e.g. the Hungarian algorithm) is computationally expensive and slow at scale; a greedy nearest-match runs in real time and is good enough since driver availability changes every few seconds anyway.

13. **Q:** Why do ride-hailing systems route location updates through a message queue (e.g. Kafka) before updating the geospatial index?
   **A:** Buffering through a queue smooths bursty write traffic and decouples ingestion rate from index update rate, letting the index consumer update asynchronously without falling behind under load.

14. **Q:** What happens to a QuadTree-based geospatial index during a surge event (e.g. a concert letting out), and how is it mitigated?
   **A:** A dense cluster of riders/drivers in one small area creates a hotspot where one leaf node or server handles disproportionate load; mitigated by dynamically re-partitioning or further subdividing hot cells, or sharding by finer geohash precision.

15. **Q:** What is the tradeoff between more frequent driver location updates (e.g. every 1s) vs. less frequent (e.g. every 10s)?
   **A:** More frequent updates give more accurate real-time matching and ETAs but multiply write load and battery/bandwidth usage on the driver's device; less frequent updates reduce load but risk stale positions.

## Cloze cards

- Core functional requirements for a ride-hailing system: {{c1::riders request rides}}, {{c2::drivers accept or reject rides}}, {{c3::real-time location tracking}}, and {{c4::fare calculation}}.
- Key non-functional requirements: {{c1::low latency matching}} (seconds, not minutes), {{c2::high availability}}, and {{c3::strong consistency for billing/payments}} (must be accurate).
- A driver location record typically includes {{c1::driverId}}, {{c2::latitude/longitude}}, {{c3::timestamp}}, and {{c4::status (available/en route/offline)}}.
- Core components of a ride-hailing architecture: {{c1::location ingestion service}}, {{c2::geospatial index}}, {{c3::matching service}}, {{c4::trip/fare service}}, and {{c5::notification service}} to alert driver/rider.
- A QuadTree recursively divides a 2D map into {{c1::four quadrants}}, subdividing further only in {{c2::densely populated}} areas, so each leaf node holds roughly {{c3::a small, bounded number}} of drivers.
