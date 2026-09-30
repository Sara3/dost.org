# Dost website

A portable redesign of the existing website. Open `index.html` in a browser to use it on your laptop. There is no installation or build step needed to view it. Images and styling are local. Internet is only needed for donations, original Medium reports, Partiful events, and contact messages.

## Add photos, videos and reports by year

Drop public media into `media/2025/`, `media/2026/`, or another four-digit year folder. Double-click **Update website.command** to resize photos, prepare videos and rebuild the website. For automatic updates while you add files, open **Watch media.command** and leave its Terminal window running. Then refresh the preview. Nothing is published automatically.

Original files stay untouched. Web copies, thumbnails and video posters are organized under `assets/media/YEAR/`, with a generated catalog in `content/media-generated.json`. The year appears beneath each gallery item and becomes available in the gallery's year selector. Optional `captions.json` files let you customize titles, descriptions, ordering and exclusions. Put a public `report.pdf` inside the year folder to add a downloadable report and update its archive status. See [the full media instructions](media/README.md).

The downloadable website includes optimized media and the updater, with empty year folders for future additions; it excludes original inbox files. Viewing remains installation-free. Updating media requires Python, Pillow and FFmpeg, all currently available on this laptop.

## Organization

- `index.html` — homepage, work, community, and team.
- `reports/` — annual archive and one page per year, 2018–2026.
- `content/reports.json` — editable report titles, summaries, amounts, sources, and record status.
- `content/media.json` — manually curated original gallery items. New year-folder media is added automatically from `content/media-generated.json`; do not edit that generated file. A null year displays an explicit unconfirmed-date label.
- `content/home.html` — editable homepage content.
- `assets/` — shared design, interactions, and the video poster extracted from the original recording.
- `downloads/dost-report-archive.zip` — portable summaries, organized into year folders. Unzip and open `START-HERE.html`.
- `api/` — existing organization photographs, preserved from the original repository.
- `scripts/build.py` — standard-library generator for the pages and archive.

After editing `content/reports.json` or page templates in `scripts/build.py`, run `python3 scripts/build.py`. Shared CSS and JavaScript can be edited directly. The generated annual pages support Print / Save as PDF.

To preview through a local web address, run `python3 -m http.server 4173 --bind 127.0.0.1`, then visit http://127.0.0.1:4173.

## Facts and sources

All annual numbers link to the source report. The legal 501(c)(3) description comes from the organization owner and the existing site; it has not been independently verified against an IRS record. Sara Daqiq and Shakiba Daqiq’s names and roles are retained from the repository. Gulafroz Dailey’s profile was removed at the owner’s request. Ahmad Zia Arman’s name and Country Coordinator role in Afghanistan were supplied by the owner, including responsibility for receiving donated funds, distribution and reporting back. Photographs are from the existing repository and are not assigned an unverified year.

The archive includes distribution reports for 2018, 2019, 2020, 2021, 2022 and 2025. Owner-supplied Facebook records dated May 28, 2021 and April 1, 2022 document assistance for 80 and 110 families respectively. The 2021 follow-up supersedes the earlier 60-family target as the reported outcome. The 2023 Zeffy page documents a project plan, not final distribution results. A retrospective 2024 update, supplied by Dost, records a private campaign funded directly by friends and family; no public annual report was published then. The 2026 update confirms funds were collected during Ramadan and distribution is in progress; a final distribution account is still to add. No missing annual totals, founding date or EIN has been invented. The owner confirmed support@dostforgood.org as the public contact address.

`content/reports.json` supports narrative sections, lists, budget tables, multiple source links and expandable source screenshots. Screenshot evidence is preserved unchanged in `assets/records/YEAR/` and included in the offline report archive. The 2018 Facebook appeal and the 2020 GoFundMe campaign provide additional historical context. `content/programs.json` generates the Afghan Girls Build education-project page, based on the original program website and public Facebook page; it does not announce current enrollment.

The old “since 2010,” “over 50,000 lives,” and “100% direct donations” claims were removed because they were not supported by the supplied reports. The 2025 expenses are shown explicitly. Historical snapshots are not presented as live 2026 fundraising numbers. Current campaign totals and supporter counts are omitted at the owner’s request. Earlier financial details remain in their dated reports; the 2026 distribution account is still outstanding.

Original sources:
- https://sadaqiq0.medium.com/how-your-donation-made-a-big-difference-ee44fb5dec5d
- https://sadaqiq0.medium.com/eid-gift-2019-97668ddd575d
- https://sadaqiq0.medium.com/dear-friends-and-family-5a08e8f1f98f
- https://sadaqiq0.medium.com/eid-gift-2021-7f90825af13f
- https://sadaqiq0.medium.com/eid-gift-2025-5b5ec5480628
- https://www.zeffy.com/en-US/fundraising/0fe4cdad-3011-4ddf-8d08-f602f7d797f9 (2023 project plan)
- https://www.gofundme.com/f/aa42a-eid-gift (2020 campaign)
- https://advanceweb-1fe40.firebaseapp.com/ (Afghan Girls Build)
- https://www.facebook.com/people/Afghan-Girls-Build/100064091859169/
- https://givebutter.com/dost2026
- https://partiful.com/e/FpdCN9VsM3NM3NyAMmSJ (March 14, 2025)
- https://partiful.com/e/56K53FUVIIo8VudnjrxN (March 14, 2026)

## Before publishing

1. Confirm the legal name, EIN and legal documents you want public. Add these to the footer and contact page.
2. Confirm current team roles and photograph permissions.
3. Add the 2023 completion update and any earlier records. The 2024 entry is an owner-supplied retrospective update. Keep donation amounts, expenses, money transferred, final distributions, and family counts separate.
4. The contact page and all footers link directly to `support@dostforgood.org`, using the owner’s existing catch-all routing. The unverified Formspree form has been removed. No test message has been sent; mail routing is managed outside this repository.
5. Confirm the preferred domain. Existing redirects refer to `wearedost.org`, while the requested domain is `dostforgood.org`; the donation campaign also links to the older domain. Do not change DNS or redirects until the intended hosting setup is confirmed.
6. Add the final 2026 distribution report once distribution is complete. The current status is owner-confirmed: funds collected during Ramadan, distribution in progress.

Updating the repository does not itself confirm a production deployment. Preview locally and review the items above before publishing the site. The previous design remains available in Git history.

## Private records

Keep internal records outside the public website folder and outside Git. A useful laptop folder structure is `Dost Records / YEAR / Reports`, `Finance`, `Distribution`, `Photos`, and `Events`, with a separate `Governance` folder for organization documents. Only approved public summaries, photos, and redacted documents should be copied into the website. No donor lists or beneficiary case files are included here.

## Research-led content revision

The rationale, primary sources, comparison sites, and proposed donor testing tasks are in `docs/design-research.md`. This is desk research, not a completed study with Dost donors. The homepage copy now lives in `content/home.html`; edit it there and rebuild. The homepage introduces the organization through its areas of support, approach, leadership and reporting. Family-dinner details and the organizers’ personal schedules are not part of the public introduction. Community appeals are secondary to the organization’s work. No full-time staffing, unpaid-staff policy or unsupported scale is implied.

## Archive gallery

The gallery uses original local media, rounded frames, a subtle CSS color treatment, and visible neighboring cards. It supports arrows, direct thumbnail selection, keyboard navigation, and horizontal dragging/swiping on photos. Videos use native controls; moving to another item pauses playback. No automatic movement or playback is used, and reduced-motion preferences are respected.

Media years are awaiting owner confirmation. The files have no date metadata, and the selected photographs were not matched to the supplied public reports. Do not infer a recording year from a repository commit, upload date, or visual similarity. Set each verified `year` in `content/media.json`, then rebuild. The local video also needs an accurate transcript/captions before claiming full media accessibility.


## Country coordination and portrait

Ahmad Zia Arman is included in the team section with the responsibilities provided by the owner. The edited portrait is `assets/ahmad-zia-arman-headshot.png`; the original user-supplied image was not overwritten. The built-in image generator replaced the background and adjusted the lighting and framing. The exact prompt is recorded in `docs/ahmad-portrait-edit.txt`.

The introduction identifies Dost as a grassroots organization committed to women’s education and basic needs, following the owner’s description. The hero and first gallery image come from the existing teaching archive. They are not assigned an unverified year, course subject or current program status. A blanket donation-allocation percentage is awaiting clarification because the 2025 report includes costs deducted from donations.

The photo and video gallery appears immediately after the homepage introduction, followed by the 2025/2024 annual-record carousel and a visible 2018–2026 archive timeline. The timeline distinguishes completed distribution reports, the 2023 project plan, the 2024 private campaign update and the ongoing 2026 distribution. It does not claim nine completed distribution reports. The 2024 card links to the retrospective yearly update. The introduction now uses a separate text column and an unobstructed photograph, stacking on mobile. The team currently presents Sara Daqiq, Shakiba Daqiq and Ahmad Zia Arman.


## Team biographies

`content/team.json` is the source for all three matching team cards, biography dialogs and standalone pages in `team/`. Clicking a card opens its biography; Escape or Close returns focus to the card. Normal profile-page links work without JavaScript and in the laptop download. Sara’s and Shakiba’s biographies were recovered from the original repository and edited for clarity; the original wording is preserved in `docs/original-team-biographies.txt`. Their public LinkedIn profiles are linked from the biographies. Ahmad’s profile uses the role and responsibilities supplied by the owner; additional career or education details have not been supplied.
