---
deck: "System Design::Instagram"
topic: "Instagram"
tags: [ankicardmaker, sd-instagram]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Instagram — System Design

Source of truth for the `System Design::Instagram` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Should an Instagram-like system support likes and comments as core functional requirements?
   **A:** Yes &mdash; likes and comments on posts are typically included as core functional requirements alongside upload and feed viewing.

2. **Q:** Why is durability an especially strict non-functional requirement for media storage in Instagram-like systems?
   **A:** User-generated photos/videos are irreplaceable &mdash; unlike a feed entry that can be regenerated, losing original media is permanent data loss, so storage must guarantee very high durability (e.g. 99.999999999%).

3. **Q:** If 50M photos are uploaded per day, what is the approximate write QPS for uploads?
   **A:** ~580 QPS (50,000,000 / 86,400 &asymp; 578).

4. **Q:** If the average photo size is 200KB and 50M photos are uploaded per day, what is the daily storage growth?
   **A:** ~10 TB/day (50M &times; 200KB = 10,000,000,000 KB &asymp; 10 TB).

5. **Q:** Why does read QPS for viewing photos vastly exceed write QPS for uploading them?
   **A:** Each uploaded photo is viewed by many followers, often repeatedly, so the read:write ratio for media viewing is much higher than 1:1 (commonly cited around 100:1 to 1000:1 depending on virality).

6. **Q:** Write the REST endpoint to upload a new photo post.
   **A:** <pre><code>POST /api/v1/posts
Content-Type: multipart/form-data
Fields: { "userId": "string", "caption": "string", "media": file }
Response: { "postId": "string", "mediaUrl": "string" }</code></pre>

7. **Q:** Write the REST endpoint to fetch a user's home feed.
   **A:** <pre><code>GET /api/v1/feed?userId={id}&amp;cursor={cursor}&amp;limit={n}
Response: { "posts": [ {...} ], "nextCursor": "string" }</code></pre>

8. **Q:** Write a minimal schema for the <code>posts</code> table (metadata only, not the media blob).
   **A:** <pre><code>posts(
  post_id    BIGINT PRIMARY KEY,
  user_id    BIGINT,
  media_url  TEXT,
  caption    VARCHAR(2200),
  created_at TIMESTAMP
)</code></pre>

9. **Q:** Where should the actual photo/video bytes be stored &mdash; in the relational/NoSQL database, or elsewhere?
   **A:** In object storage (e.g. S3/blob storage), not the database; the database only stores metadata plus a URL/key pointing to the object storage location.

10. **Q:** Why is media upload typically handled asynchronously (upload raw file, then process in the background)?
   **A:** Processing (resizing, transcoding, thumbnail generation) is slow and CPU-intensive; doing it synchronously would block the upload request for a long time, so the raw file is stored first and a background worker processes it, updating status when done.

11. **Q:** Why is object storage (e.g. S3) preferred over a filesystem or database for storing photos/videos at scale?
   **A:** Object storage is designed for cheap, durable, horizontally scalable storage of large binary blobs with simple key-based access, unlike a relational DB (poor at large blobs) or a single filesystem (doesn't scale/replicate easily).

12. **Q:** What is the role of a CDN in an Instagram-like architecture?
   **A:** The CDN caches media at edge locations close to users, so requests are served from a nearby edge server instead of round-tripping to origin object storage, cutting latency and origin load.

13. **Q:** Why does an upload pipeline generate multiple resolutions/thumbnails of the same image instead of storing just the original?
   **A:** Different clients/contexts (feed thumbnail, profile grid, full-screen view) need different sizes; serving a pre-resized image avoids sending an oversized original and re-scaling on the client, saving bandwidth and load time.

14. **Q:** Pre-signed URL (in the context of media upload) *(reversed — both ways)*
   **A:** A temporary, signed URL that grants a client direct, time-limited permission to upload/download an object directly to/from object storage, bypassing the application server for the actual file transfer.

15. **Q:** Why have clients upload directly to object storage via a pre-signed URL instead of routing the file through the app server?
   **A:** It avoids using app server bandwidth/CPU to proxy large media files, letting the app server just issue a signed URL while object storage handles the heavy data transfer directly.

16. **Q:** How does sharding the metadata database (e.g. by user_id or post_id) help scale an Instagram-like system?
   **A:** It spreads read/write load for post metadata across many database nodes instead of a single instance, avoiding a single point of contention as the number of posts grows.

17. **Q:** What is the tradeoff of generating many image resolutions at upload time vs. resizing on demand?
   **A:** Pre-generating at upload time costs extra storage and upfront processing but gives fast, consistent read latency; resizing on demand saves storage but adds latency and repeated CPU cost on every unique request.

18. **Q:** Why might an Instagram-like system choose eventual consistency for the feed instead of strong consistency across all replicas?
   **A:** Strong consistency would require synchronous replication before a post is visible anywhere, hurting availability and latency; eventual consistency lets a post appear slightly later in some replicas/feeds, an acceptable tradeoff for higher availability and throughput.

## Cloze cards

- Core functional requirements of an Instagram-like system include: {{c1::users can upload photos/videos}}, {{c2::users can follow other users}}, and {{c3::users can view a feed of posts from people they follow}}.
- Non-functional requirements for an Instagram-like system include: {{c1::high availability}}, {{c2::low latency media delivery (fast image/video load)}}, and {{c3::durability &mdash; uploaded media must never be lost}}.
- The high-level architecture of an Instagram-like system typically includes: {{c1::an upload/media service}}, {{c2::object/blob storage for media files}}, {{c3::a CDN for serving media}}, {{c4::a metadata database for posts}}, and {{c5::a feed service}}.
- Scaling bottlenecks and fixes for an Instagram-like system: {{c1::origin storage/bandwidth overload from popular media}} is fixed by {{c2::CDN edge caching}}; {{c3::the feed database becoming a hotspot for popular accounts}} is fixed by {{c4::caching feed data and sharding by user_id}}.
