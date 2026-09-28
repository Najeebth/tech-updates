# 📰 Daily Tech Updates

Automatically generated daily tech digest, saved as Markdown files in `updates/`.

## 📋 Sections Covered

| Section | Topics |
|---|---|
| **Software Engineering** | GitHub, Stack Overflow, InfoQ |
| **AI Models & Integration** | Google AI, OpenAI, DeepLearning.AI |
| **Tech Stack Trends** | Dev.to, Hacker News, The Verge |
| **Worth a Deeper Look** | Krebs on Security, Schneier, The Hacker News |

## ⏰ Schedule

Runs every day at **8:00 AM IST** via GitHub Actions (no PC required).

## 📁 Output

Each day's update is saved as:
```
updates/YYYY-MM-DD.md
```
Example: `updates/2026-09-29.md`

## 🚀 Manual Trigger

You can manually trigger a run from the **Actions** tab on GitHub → `Daily Tech Update` → `Run workflow`.

## 💻 Run Locally

```bash
pip install feedparser requests
python fetch_updates.py
```
