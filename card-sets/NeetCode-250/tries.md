---
deck: "NeetCode 250::Tries"
topic: "NeetCode 250 — Tries"
tags: [ankicardmaker, neetcode250, tries]
note_type: Basic
created: 2026-09-09
---

# NeetCode 250 — Tries

Story front hides the technique; back reveals the mapping, approach, and complexity.

## 1. Implement Trie Prefix Tree  ·  _Medium_

**Scenario:** A librarian builds a card-catalog gadget that stores words letter by letter along shared branching paths, so common beginnings are stored only once. It must support filing a new word, checking whether an exact word was filed, and checking whether any filed word begins with a given opening. Design this gadget.

- **Maps to:** Trie / prefix tree with per-node children and end-of-word flag (Implement Trie).
- **Model it:** Build a structure supporting insert, exact-word search, and prefix search over strings.
- **Approach & variations:**
  - Each node holds up to 26 child links and a boolean marking a complete word ends there.
  - Insert walks/creates a path of nodes letter by letter, flagging the last.
  - search returns the end flag at the path's terminal; startsWith just checks the path exists.
- **Time:** O(L) per insert/search/startsWith for a word of length L.
- **Space:** O(total characters inserted) across all trie nodes.

## 2. Design Add And Search Words Data Structure  ·  _Medium_

**Scenario:** A stamp collector files words into a catalog and later looks them up, but a lookup query may contain a wildcard mark that matches any single letter in that position. Design a catalog supporting filing a word and answering whether any filed word matches a possibly-wildcarded query.

- **Maps to:** Trie with DFS for wildcard positions (Add and Search Words / WordDictionary).
- **Model it:** Store words and answer search where '.' matches any single character.
- **Approach & variations:**
  - Insert like a normal prefix tree along letter paths.
  - Search walks the trie; on a wildcard, recurse into every existing child at that position.
  - Match succeeds only if a path consumes the whole query and ends on a word-end flag.
- **Time:** O(L) for a concrete query; up to O(26^L) worst case when many wildcards force branching.
- **Space:** O(total characters stored) for the trie, plus O(L) recursion for wildcard search.

## 3. Extra Characters in a String  ·  _Medium_

**Scenario:** A proofreader has a banner of letters and a dictionary of valid words. She may carve the banner into non-overlapping pieces that are each a dictionary word; any leftover letters not covered by a chosen word are wasted. What is the fewest leftover letters possible?

- **Maps to:** DP over indices with a trie (or dictionary set) for word lookups (Extra Characters in a String).
- **Model it:** Segment a string into dictionary words minimizing the count of uncovered characters.
- **Approach & variations:**
  - Let dp[i] be the fewest extras for the suffix starting at i.
  - Option one: waste character i (1 + dp[i+1]); option two: for any dictionary word matching at i, take dp[i + wordLen].
  - A trie over the dictionary lets you scan all words starting at i in one walk; take the minimum.
- **Time:** O(n^2) checking substrings, or O(n * maxWordLen) with a trie walk from each index.
- **Space:** O(n) for the dp array plus O(dictionary size) for the trie.

## 4. Word Search II  ·  _Hard_

**Scenario:** A grid of lettered tiles sits on a table alongside a long shopping list of target words. A player traces each word by stepping between edge-adjacent tiles without reusing a tile in a single trace. Which words from the list can be found somewhere on the board? Report all of them efficiently, not one slow search per word.

- **Maps to:** Trie of the word list plus DFS backtracking over the grid (Word Search II).
- **Model it:** Find which of many words appear as adjacent-cell paths in a character grid, searching all words at once.
- **Approach & variations:**
  - Build a trie from the word list so one board traversal checks all words simultaneously.
  - DFS from each cell, descending the trie by the current letter; record a word when a node marks a word end.
  - Mark cells visited during a path and restore on backtrack; prune trie leaves after finding to speed up.
- **Time:** O(m * n * 4^Lmax) worst case, but the trie prunes dead prefixes sharply.
- **Space:** O(total letters in the word list) for the trie plus O(Lmax) recursion.
