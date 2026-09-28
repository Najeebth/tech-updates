"""
Daily Tech Update Fetcher
Fetches RSS feeds and generates a structured Markdown report.

Sections:
  - Software Engineering
  - AI Models & Integration
  - Tech Stack Trends
  - Worth a Deeper Look (Cybersecurity & Privacy)
"""

import feedparser
import datetime
import os
import textwrap

# ─── Output directory ────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "updates")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── RSS Feed Sources ─────────────────────────────────────────────────────────
FEEDS = {
    "Software Engineering": [
        ("The GitHub Blog",        "https://github.blog/feed/"),
        ("Stack Overflow Blog",    "https://stackoverflow.blog/feed/"),
        ("InfoQ Software Dev",     "https://feed.infoq.com/"),
    ],
    "AI Models & Integration": [
        ("Google AI Blog",         "https://blog.google/technology/ai/rss/"),
        ("OpenAI News",            "https://openai.com/blog/rss.xml"),
        ("The Batch (DeepLearning.AI)", "https://www.deeplearning.ai/the-batch/feed/"),
    ],
    "Tech Stack Trends": [
        ("Dev.to",                 "https://dev.to/feed"),
        ("Hacker News Best",       "https://hnrss.org/best"),
        ("The Verge Tech",         "https://www.theverge.com/rss/index.xml"),
    ],
    "Worth a Deeper Look": [
        ("Krebs on Security",      "https://krebsonsecurity.com/feed/"),
        ("Schneier on Security",   "https://www.schneier.com/feed/atom/"),
        ("The Hacker News (Security)", "https://feeds.feedburner.com/TheHackersNews"),
    ],
}

MAX_ITEMS_PER_FEED = 3   # max articles per feed
MAX_ITEMS_PER_SECTION = 6  # max articles per section


# ─── Helpers ─────────────────────────────────────────────────────────────────

def fetch_feed(url: str, max_items: int = MAX_ITEMS_PER_FEED) -> list[dict]:
    """Parse an RSS/Atom feed and return a list of {title, link, summary}."""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:max_items]:
            title   = entry.get("title", "No title").strip()
            link    = entry.get("link", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            # Strip HTML tags simply
            import re
            summary = re.sub(r"<[^>]+>", "", summary)
            summary = " ".join(summary.split())  # collapse whitespace
            summary = textwrap.shorten(summary, width=200, placeholder="…")
            items.append({"title": title, "link": link, "summary": summary})
        return items
    except Exception as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}")
        return []


def build_section(section_name: str, feeds: list[tuple]) -> str:
    """Build a markdown section from multiple feeds."""
    lines = [f"\n## {section_name}\n"]
    collected = []

    for feed_name, url in feeds:
        items = fetch_feed(url)
        for item in items:
            collected.append((feed_name, item))
        if len(collected) >= MAX_ITEMS_PER_SECTION:
            break

    collected = collected[:MAX_ITEMS_PER_SECTION]

    if not collected:
        lines.append("- *No updates fetched — check feed URLs or network.*\n")
    else:
        for feed_name, item in collected:
            lines.append(f"- **[{item['title']}]({item['link']})**")
            if item["summary"]:
                lines.append(f"  > {item['summary']}")
            lines.append(f"  *Source: {feed_name}*\n")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    today = datetime.date.today()
    date_str = today.strftime("%B %d, %Y")       # e.g. September 29, 2026
    file_date = today.strftime("%Y-%m-%d")        # e.g. 2026-09-29
    output_path = os.path.join(OUTPUT_DIR, f"{file_date}.md")

    print(f"📰 Fetching tech updates for {date_str}…")

    # ── Header ────────────────────────────────────────────────────────────────
    content = f"# Tech Update — {date_str}\n"
    content += f"\n> 🗓️ Auto-generated on {date_str} | Daily Tech Digest\n"
    content += "\n---\n"

    # ── Sections ──────────────────────────────────────────────────────────────
    for section_name, feeds in FEEDS.items():
        print(f"  📡 Fetching: {section_name}")
        content += build_section(section_name, feeds)
        content += "\n---\n"

    # ── Footer ────────────────────────────────────────────────────────────────
    content += "\n*Generated automatically via GitHub Actions. Sources: RSS feeds.*\n"

    # ── Write file ────────────────────────────────────────────────────────────
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ Saved: {output_path}")


if __name__ == "__main__":
    main()
