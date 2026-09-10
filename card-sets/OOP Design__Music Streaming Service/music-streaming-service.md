---
deck: "OOP Design::Music Streaming Service"
topic: "Music Streaming Service"
tags: [ankicardmaker, ood-music-streaming]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-10
---

# Music Streaming Service — OOP Design

Source of truth for the `OOP Design::Music Streaming Service` deck (20 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** What are the core functional requirements to clarify for a Music Streaming Service OOD interview?
   **A:** 1) Browse/search a catalog of songs, albums, artists. 2) Play/pause/skip/seek playback. 3) Create, edit, and share playlists. 4) Follow artists and see a personalized feed. 5) Get song recommendations. 6) Support tiered subscriptions (free vs premium) affecting available features.

2. **Q:** What should you explicitly mark out of scope when designing a Music Streaming Service in an interview?
   **A:** The actual audio codec/streaming protocol (e.g. adaptive bitrate), DRM/licensing enforcement details, and the ML internals of a recommendation model &mdash; treat recommendation as a pluggable strategy interface instead of designing the model.

3. **Q:** What is the responsibility of the <code>User</code> class?
   **A:** Holds account/profile data, subscription tier, owned playlists, followed artists, and listening history &mdash; used as input to recommendations and to enforce feature gating (e.g. skip limits on the free tier).

4. **Q:** What is the responsibility of the <code>Playlist</code> class?
   **A:** An ordered collection of songs with a name, an owner, and optional collaborators; supports add/remove/reorder operations and knows nothing about how it is played back.

5. **Q:** What is the responsibility of the <code>Player</code> (playback engine) class?
   **A:** Manages the current play queue and playback position: <code>play()</code>, <code>pause()</code>, <code>skip()</code>, <code>seek()</code>; tracks the current <code>PlaybackState</code> and notifies observers when the now-playing song changes.

6. **Q:** How does <code>Playlist</code> relate to <code>Song</code>?
   **A:** Aggregation, not composition: a <code>Playlist</code> references existing <code>Song</code> objects (often via a <code>PlaylistEntry</code> wrapper that also stores position/order and who added it) &mdash; deleting a playlist must not delete the underlying songs.

7. **Q:** How does <code>User</code> relate to <code>Playlist</code>?
   **A:** One-to-many ownership: a <code>User</code> owns zero or more <code>Playlist</code>s. For collaborative playlists, a playlist instead holds a set of contributor <code>User</code>s in addition to a single owner.

8. **Q:** Which design pattern fits song recommendations, and why?
   **A:** <b>Strategy</b>. <code>RecommendationEngine</code> holds a <code>RecommendationStrategy</code> interface (e.g. genre-based, collaborative-filtering, recently-played-based); the concrete algorithm is swapped at runtime per user/experiment without changing the engine's calling code.

9. **Q:** Which design pattern fits the now-playing / live activity feature, and why?
   **A:** <b>Observer</b>. The <code>Player</code> (or a dedicated <code>NowPlayingSubject</code>) notifies registered listeners &mdash; a friend-activity feed, a lock-screen widget, analytics &mdash; whenever the current song changes, decoupling playback from every consumer of that event.

10. **Q:** Which design pattern fits playlist creation, and why?
   **A:** <b>Factory</b>. A <code>PlaylistFactory</code> centralizes construction of different playlist variants (plain user playlist, collaborative playlist, auto-generated smart mix) so client code calls one <code>createPlaylist(type, owner, name)</code> instead of knowing every concrete subclass.

11. **Q:** What is the shape of <code>RecommendationEngine</code>'s public API, given it uses the Strategy pattern?
   **A:** <code>getRecommendations(User user, int limit)</code> delegates to <code>strategy.recommend(user, library, limit)</code>; a <code>setStrategy(RecommendationStrategy)</code> method lets the engine swap algorithms at runtime (e.g. A/B testing).

12. **Q:** What four methods form the core playback API on <code>Player</code>?
   **A:** <code>play()</code>, <code>pause()</code>, <code>skip()</code>, and <code>seek(position)</code> &mdash; each updates <code>PlaybackState</code> and, on a song change, notifies now-playing observers.

13. **Q:** Edge case: a song is removed from the catalog (rights expired) while it still appears in thousands of user playlists. How should the design handle this?
   **A:** Soft-delete/tombstone the <code>Song</code> rather than hard-deleting it: mark it <code>unavailable</code>, keep the object (and its id) so playlists don't break, and have the <code>Player</code> skip unavailable songs during playback with a UI indicator instead of a crash.

14. **Q:** Edge case: the same account starts playback on a phone and then on a web browser. What should happen?
   **A:** Enforce a single active playback session per account (common for personal tiers): starting playback on the new device sends a stop/transfer signal to the previous device's <code>Player</code> instance, so only one device is ever actually streaming at a time.

15. **Q:** (Java) Implement the <code>RecommendationStrategy</code> interface and a <code>GenreBasedStrategy</code> concrete implementation.
   **A:** <pre><code>public interface RecommendationStrategy {
    List&lt;Song&gt; recommend(User user, MusicLibrary library, int limit);
}

public class GenreBasedStrategy implements RecommendationStrategy {
    @Override
    public List&lt;Song&gt; recommend(User user, MusicLibrary library, int limit) {
        Set&lt;String&gt; favoriteGenres = user.getTopGenres();
        return library.getAllSongs().stream()
            .filter(song -&gt; favoriteGenres.contains(song.getGenre()))
            .filter(song -&gt; !user.hasPlayed(song))
            .limit(limit)
            .collect(Collectors.toList());
    }
}</code></pre>

16. **Q:** (Python) Implement an Observer-pattern <code>NowPlayingSubject</code> that a <code>FriendActivityFeed</code> listener can subscribe to.
   **A:** <pre><code>class NowPlayingSubject:
    def __init__(self):
        self._observers = []
        self._current_song = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def set_current_song(self, song):
        self._current_song = song
        self._notify()

    def _notify(self):
        for observer in self._observers:
            observer.on_now_playing_changed(self._current_song)


class FriendActivityFeed:
    def on_now_playing_changed(self, song):
        print(f"Now playing: {song.title} by {song.artist}")</code></pre>

17. **Q:** (Java) Implement a <code>PlaylistFactory</code> that builds different playlist variants from a <code>PlaylistType</code> enum.
   **A:** <pre><code>public class PlaylistFactory {
    public static Playlist createPlaylist(PlaylistType type, User owner, String name) {
        switch (type) {
            case USER_CREATED:
                return new Playlist(name, owner, false);
            case COLLABORATIVE:
                return new CollaborativePlaylist(name, owner);
            case AUTO_GENERATED_MIX:
                return new SmartMixPlaylist(name, owner);
            default:
                throw new IllegalArgumentException("Unknown playlist type: " + type);
        }
    }
}</code></pre>

18. **Q:** (Python) Implement <code>Player.play()</code>, <code>pause()</code>, and <code>skip()</code> against a play queue.
   **A:** <pre><code>class Player:
    def __init__(self, queue):
        self.queue = queue
        self.state = PlaybackState.STOPPED
        self.current_index = 0

    def play(self):
        if not self.queue:
            return
        self.state = PlaybackState.PLAYING

    def pause(self):
        if self.state == PlaybackState.PLAYING:
            self.state = PlaybackState.PAUSED

    def skip(self):
        self.current_index = (self.current_index + 1) % len(self.queue)
        self.play()</code></pre>

## Cloze cards

- The core classes in a Music Streaming Service design are {{c1::User}}, {{c2::Song}} (with Album/Artist metadata), {{c3::Playlist}}, {{c4::Player}} (playback engine), {{c5::MusicLibrary}} (catalog/search), and {{c6::RecommendationEngine}}.
- The <code>PlaybackState</code> enum for the player is {{c1::PLAYING}}, {{c2::PAUSED}}, and {{c3::STOPPED}}.
