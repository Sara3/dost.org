# Add photos, videos and reports

1. Put public website material in its year folder, for example `media/2025/` or `media/2026/`. Create another four-digit year folder whenever needed. Photos and videos can go together. Subfolders are supported.
2. Double-click **Update website.command** in the main Dost folder. Refresh the website when it says “Website updated.”
3. For automatic updates while adding files, double-click **Watch media.command** instead and keep that Terminal window open. It waits for file copying to settle, then prepares files and rebuilds the site. Control+C stops it. It does not upload or publish anything.

The originals stay untouched. Smaller photos, thumbnails, browser-compatible MP4 videos and video posters are written to `assets/media/YEAR/`. The year folder supplies the date shown on the website. All new media appears in the gallery, newest year first, with a year selector. Unchanged files are reused, so subsequent updates are faster.

## File names and captions

Use descriptive filenames such as `01-literacy-class.jpg` and `02-food-distribution.mov`. The website uses these as initial titles. Camera filenames receive a neutral title such as “Photograph from 2025.” It does not guess who appears in an image or what happened.

For custom descriptions, add an optional `captions.json` inside that year folder:

```json
{
  "01-literacy-class.jpg": {
    "title": "Learning together",
    "caption": "Add your accurate description of this activity.",
    "alt": "Describe what is visible in the photograph.",
    "order": 1
  },
  "photo-to-hold-back.jpg": { "include": false }
}
```

Use the relative path for files in subfolders, such as `education/class.jpg`. Caption edits do not re-encode media. Delete a source from this public folder to remove it from the next build; only its generated copies are removed. Keep your master archive elsewhere.

## Annual reports

Place the public PDF for a year at `media/YEAR/report.pdf`. The updater adds its download to that year's report page and archive. It does not invent a summary or extract financial figures. Existing sourced summaries stay in `content/reports.json`; edit that file to add context. A report PDF makes a previously missing year available, and updates its timeline status.

## Supported formats and setup

- Photos: JPG, JPEG, PNG, WebP, TIFF, HEIC and HEIF. Long edge capped at 1,600 pixels; smaller images are not enlarged. Orientation is corrected, proportions preserved and EXIF/location metadata removed from the web copy.
- Videos: MP4, MOV, M4V, WebM and MKV. Converted to H.264/AAC MP4 with a maximum 1,280-pixel long edge, original aspect ratio and a still preview. Native player controls remain available. Add accurate captions/transcripts separately when needed.
- Reports: `report.pdf` in the year folder. Other PDFs and unsupported files are not imported.

This laptop already has Python, Pillow and FFmpeg. On another laptop, install Python 3.10+, Pillow (`python3 -m pip install Pillow`), and FFmpeg. On macOS, HEIC uses the built-in image converter when needed; on other systems also install `pillow-heif`. Viewing the packaged website needs none of these tools and works offline.

This is a public-media inbox. The download includes optimized assets, not these originals or caption-source files. Keep donor lists, private case records and unapproved media in a separate private folder.
