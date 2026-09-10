---
deck: "System Design::Video Streaming (YouTube)"
topic: "Video Streaming (YouTube)"
tags: [ankicardmaker, sd-youtube]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Video Streaming (YouTube) — System Design

Source of truth for the `System Design::Video Streaming (YouTube)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** Why do video streaming systems generally favor availability over strong consistency for metadata like view counts and comments?
   **A:** Users tolerate briefly stale counts/comments, but any downtime for playback directly hurts UX and revenue, so the system favors an AP (available, eventually consistent) design for non-critical metadata.

2. **Q:** If a video platform has 2B total users and 5% watch videos daily, what is the approximate DAU?
   **A:** 2B x 5% = ~100 million daily active users.

3. **Q:** Given 100M DAU each watching 5 videos/day, what is the approximate average read QPS for video views?
   **A:** 100M x 5 / 86,400s ≈ 5,787 QPS (roughly 6K QPS).

4. **Q:** If 1M videos are uploaded daily averaging 300MB each, what is the approximate daily raw storage need (before replication)?
   **A:** 1M x 300MB = 300TB/day.

5. **Q:** Why is peak QPS often estimated as 2-3x the average QPS when sizing a video streaming system?
   **A:** Traffic is not uniform across the day; evening and weekend peaks can be several times the daily average, so capacity must be provisioned for bursts, not just the mean.

6. **Q:** What would a resumable video upload API call look like in a YouTube-like system?
   **A:** <pre><code>POST /videos/upload
{ title, description, tags }
-&gt; returns uploadId, presigned URL</code></pre>

7. **Q:** What API endpoint would a client call to fetch the streaming manifest for a given video?
   **A:** <code>GET /videos/{videoId}/manifest</code> returns the master playlist (e.g. HLS .m3u8) listing the available bitrate variants.

8. **Q:** In the video metadata table, what primary key design is typically used, and why?
   **A:** A globally unique videoId (UUID or Snowflake-style ID) generated at upload time, avoiding collisions across distributed upload servers and decoupling the ID from any single database's auto-increment.

9. **Q:** Why does the upload flow write the raw video to blob storage before transcoding, rather than transcoding inline during upload?
   **A:** It decouples upload latency from transcoding time, which can take minutes; the client gets a fast upload confirmation while transcoding happens asynchronously via a queue and worker pool.

10. **Q:** What role does a message queue (e.g. Kafka/SQS) play between the upload service and the transcoding workers?
   **A:** It buffers upload events so transcoding workers can pull jobs at their own pace, smoothing bursty upload traffic and allowing independent horizontal scaling of the worker pool.

11. **Q:** Why is an uploaded video split into small segments before/during transcoding?
   **A:** It enables parallel encoding across multiple workers, and adaptive bitrate clients need short segments to switch quality mid-playback without re-downloading the whole file.

12. **Q:** What two adaptive bitrate streaming protocols are most commonly used today?
   **A:** HLS (HTTP Live Streaming, Apple) and MPEG-DASH, both using a manifest file (.m3u8 / .mpd) that points to segmented bitrate variants.

13. **Q:** Why does a CDN dramatically reduce origin server load and latency for video delivery?
   **A:** It caches video segments at edge servers geographically close to viewers, so most playback requests are served from a nearby edge cache instead of round-tripping to the origin blob storage.

14. **Q:** Why is a pull CDN generally preferred over a push CDN for a platform with millions of long-tail videos?
   **A:** A push CDN would waste storage replicating rarely-watched videos to every edge node; a pull CDN only caches content at edges where it is actually requested, matching cache usage to real demand.

15. **Q:** What is the main scaling bottleneck for the transcoding pipeline as upload volume grows?
   **A:** Compute throughput of the transcoding workers; video encoding is CPU/GPU-intensive, so worker pool size and queue depth become the limiting factor under high upload volume.

16. **Q:** Why can the video metadata database become a bottleneck at YouTube scale, and what is a common fix?
   **A:** Billions of video rows under heavy read traffic overload a single database; the fix is sharding by videoId/uploaderId plus read replicas and caching hot metadata.

17. **Q:** What is the tradeoff between transcoding a video into many resolution variants vs. just a few?
   **A:** More variants improve playback quality-adaptation and bandwidth efficiency for viewers, but increase storage cost and transcoding compute time.

## Cloze cards

- Core functional requirements for a video streaming system include {{c1::video upload}}, {{c2::video streaming/playback}}, and {{c3::video search}}.
- Key non-functional requirements for a video streaming platform: {{c1::high availability}}, {{c2::low latency streaming (fast start, smooth playback)}}, and {{c3::durability of stored video}} (no data loss).
- A video metadata record typically stores {{c1::videoId}}, {{c2::uploaderId}}, {{c3::title/description}}, {{c4::duration}}, {{c5::status (processing/ready)}}, and {{c6::CDN URLs per resolution}}.
- Core components of a video streaming architecture: {{c1::upload service}}, {{c2::transcoding/encoding pipeline}}, {{c3::metadata database}}, {{c4::blob storage (e.g. S3)}}, and {{c5::CDN}} for delivery.
- Adaptive bitrate streaming works by encoding the same video into {{c1::multiple resolution/bitrate variants}}, splitting each into short {{c2::segments}}, and having the client {{c3::dynamically switch}} between variants based on measured network bandwidth.
