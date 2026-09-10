---
deck: "System Design::File Storage (Dropbox)"
topic: "File Storage (Dropbox)"
tags: [ankicardmaker, sd-dropbox]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# File Storage (Dropbox) — System Design

Source of truth for the `System Design::File Storage (Dropbox)` deck (22 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements of a Dropbox-like file storage system?
   **A:** Upload/download files, sync changes across devices, share files/folders, and support offline edits that sync later.

2. **Q:** For 500M users averaging 10GB of storage each, roughly how much total storage capacity is needed?
   **A:** ~5 exabytes (500M × 10GB), before replication overhead.

3. **Q:** Why chunk files into fixed or variable-size blocks instead of storing each file whole?
   **A:** So only the changed chunks need to be re-uploaded/re-downloaded on an edit, and identical chunks across files or users can be deduplicated.

4. **Q:** Why does a sync API use a monotonic cursor/version token instead of timestamps to fetch changes?
   **A:** Timestamps can collide or skip changes due to clock issues; a monotonic cursor/version guarantees the client resumes exactly where it left off.

5. **Q:** In a chunked file storage design, what identifies a chunk for deduplication?
   **A:** A content hash (e.g. SHA-256) of the chunk's bytes — identical content produces the same hash regardless of source file.

6. **Q:** What does a file's metadata record typically store, apart from filename and owner?
   **A:** An ordered list of chunk hashes (the file's chunk manifest), a version number, size, and modification timestamp.

7. **Q:** Content-defined (variable-size) chunking *(reversed — both ways)*
   **A:** Splitting a file into chunks based on content patterns via a rolling hash (e.g. Rabin-Karp), so inserting a single byte doesn't shift every subsequent fixed-size chunk's boundary and hash.

8. **Q:** What is the benefit of global, cross-user chunk deduplication in a storage system like Dropbox?
   **A:** It massively reduces total storage — identical chunks (common files, OS images, duplicate uploads) are stored once and referenced by multiple files/users.

9. **Q:** What is the general pseudocode for handling a new chunk with content-hash dedup?
   **A:** <pre><code>chunk_hash = SHA256(chunk_bytes)
if chunk_store.exists(chunk_hash):
    increment_refcount(chunk_hash)
else:
    chunk_store.put(chunk_hash, chunk_bytes)</code></pre>

10. **Q:** Why is the metadata service typically backed by a strongly consistent database rather than the blob store itself?
   **A:** File/folder hierarchy, versions, and permissions need transactional, low-latency lookups and consistency guarantees that blob stores don't provide.

11. **Q:** What technique lets a Dropbox client detect local file changes efficiently instead of polling and re-hashing everything?
   **A:** OS-level filesystem watch APIs (e.g. inotify, FSEvents) for change notifications, combined with periodic reconciliation scans.

12. **Q:** What causes a sync conflict in a Dropbox-like system?
   **A:** Two devices edit the same file offline and both push updates based on the same base version, so their changes diverge (a concurrent write).

13. **Q:** What is the simplest conflict resolution strategy Dropbox actually uses for conflicting edits?
   **A:** Keep both — save the losing write as a separate 'conflicted copy' file rather than silently overwriting or auto-merging.

14. **Q:** How does the metadata service detect a conflicting write instead of just accepting whichever request arrives last?
   **A:** The client submits the base version number it expected; if it doesn't match the server's current version, the write is rejected as a conflict (optimistic concurrency control).

15. **Q:** What becomes a bottleneck if the metadata database stores the entire file hierarchy in one global table under heavy load?
   **A:** Hot partitions on popular folders/shared files; it needs sharding by user/namespace and caching of frequently accessed metadata.

16. **Q:** Why can notification fan-out be a bottleneck for a widely shared folder?
   **A:** A single edit must notify every collaborator's client; with thousands of watchers this needs a scalable pub/sub system rather than direct per-client pushes.

17. **Q:** What's the tradeoff of small chunk sizes (e.g. 256KB) vs large chunk sizes (e.g. 4MB)?
   **A:** Small chunks improve the dedup ratio and reduce re-sync bandwidth but increase metadata overhead (more chunk records per file); large chunks do the opposite.

18. **Q:** What's the tradeoff of client-side encryption before upload (zero-knowledge storage)?
   **A:** Better privacy since the server never sees plaintext, but it breaks server-side cross-user deduplication and complicates search/preview features.

## Cloze cards

- Dropbox-like systems require {{c1::high availability}}, {{c2::durability}} (no data loss), {{c3::low-bandwidth sync}} (only transfer diffs), and {{c4::per-user consistency}} across a user's own devices.
- A Dropbox-like API exposes {{c1::POST /files (upload)}}, {{c2::GET /files/{id} (download)}}, and {{c3::GET /files/{id}/changes?since=cursor (sync delta)}}.
- Core components: a {{c1::block/chunk storage service}} (e.g. a blob store like S3), a {{c2::metadata service}} (file-to-chunk mapping, versions), a {{c3::sync/notification service}}, and {{c4::client agents}} that watch the local filesystem.
- A typical sync flow is: {{c1::client detects a local change}} → {{c2::chunk and hash the file}} → {{c3::upload only the new/changed chunks}} → {{c4::update the metadata service}} → {{c5::notify other devices to pull the changes}}.
