#!/usr/bin/env bash
# Fetch a video + its metadata for 拉片 analysis.
#
# Why these exact flags: as of 2026 YouTube forces "SABR" streaming for the
# default web client, which makes yt-dlp fail with "The page needs to be
# reloaded" or skip all formats. Passing the android/ios/web player clients
# works around it. We grab format 18 (360p mp4 WITH audio, small + fast) or the
# worst mp4 as fallback — 360p is plenty to read on-screen UI/spec text from
# montages, and small files dodge the aggressive throttling on big ones.
#
# Usage:  get_video.sh <youtube-url-or-id> <output-dir>
# Writes: <output-dir>/vid.mp4  and prints title/duration/etc to stdout.

set -uo pipefail
URL="${1:?usage: get_video.sh <url> <out-dir>}"
OUT="${2:?usage: get_video.sh <url> <out-dir>}"
mkdir -p "$OUT"

# Prefer python module form so it works regardless of PATH.
YTDLP="python3 -m yt_dlp"

echo "=== metadata ==="
$YTDLP --skip-download --dump-json \
  --extractor-args "youtube:player_client=android,ios" "$URL" 2>/dev/null \
| python3 -c "
import json,sys
d=json.load(sys.stdin)
for k in ['title','uploader','channel','upload_date','duration','view_count']:
    print(f'{k}:', d.get(k))
print('description:', (d.get('description') or '').replace(chr(10),' ')[:400])
" || echo "(metadata fetch failed — continuing to download)"

echo "=== downloading (360p w/ audio) ==="
$YTDLP -f "18/worst[ext=mp4]/worst" \
  --extractor-args "youtube:player_client=android,ios,web" \
  --socket-timeout 30 -R 10 --no-playlist \
  -o "$OUT/vid.%(ext)s" "$URL"

echo "=== done: $(ls -la "$OUT"/vid.mp4 2>/dev/null | awk '{print $5}') bytes ==="
