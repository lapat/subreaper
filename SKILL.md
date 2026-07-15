---
name: subreaper
description: Sweep Gmail for recurring subscription charges, track them in charges.json, and drive a browser to cancel the ones the user chooses. Use when the user wants to find forgotten subscriptions, audit recurring charges, or cancel one they've identified.
---

# SubReaper

You are auditing the user's recurring subscriptions. This happens in two separable phases — **never cancel anything during the sweep phase.** Discovery and cancellation are always distinct steps, each initiated by the user.

## Phase 1: Sweep

Goal: find every recurring charge the user is currently paying (or has paid) for, and write it to `charges.json` using the schema in `schema/charges.schema.json`.

1. Search Gmail broadly first, then narrow. Useful starting queries: `receipt OR invoice OR "payment confirmation" OR "your subscription" OR renewal`, then per-vendor follow-ups once you spot a name. Look across the full mailbox history, not just recent months — forgotten subscriptions are usually the old ones.
2. For each distinct service you find, determine: current billing amount and cycle, how the user signs in (email/password, Google, Apple, etc.), the most recent charge date, and the first charge date if visible.
3. **Cross-check Apple and Google billing directly, not just Gmail.** Apple's `account.apple.com/account/manage/section/subscriptions` and Google's subscription/payment pages often surface subscriptions that never generate a distinct Gmail receipt, or that duplicate a subscription already found via the web (the same service billed once through Apple IAP and once through the web are two separate charges — track both).
4. Some vendors only email when a cost threshold is crossed, not every billing cycle (cloud/usage-based billing especially). Note this explicitly in `cancel_notes` rather than assuming a gap in emails means no charge occurred.
5. Write one entry per subscription to `charges.json`, following `schema/charges.schema.json` exactly. Set `status` to `active`, `canceled` (if evidence shows it already stopped), or `needs_review` (evidence is ambiguous — say what's missing and where to check directly, e.g. a specific billing console URL).
6. Summarize the sweep for the user in plain text: total found, monthly total, anything flagged `needs_review`. Don't build a dashboard or artifact unless asked — a fast plain-text answer is preferred.

## Phase 2: Cancel (only when the user asks, one subscription at a time)

1. Read the subscription's `url` and `signin_method` from `charges.json` first.
2. Navigate to the cancellation flow in a real browser.
3. **Hard boundaries — stop and hand off instead of working around these:**
   - Never enter a password or 2FA code yourself. Hand the sign-in page to the user, wait for them to confirm they're signed in, then resume.
   - Never complete a CAPTCHA or "verify you're human" challenge. Stop and tell the user what happened.
4. If a retention offer or discount appears, decline it and proceed with the cancellation — don't stop to ask each time, just note in `cancel_notes` that an offer was declined.
5. After cancellation, record exactly what happened in `cancel_notes`: the path taken, any confirmation shown, and whether access continues until a future date. If the site's confirmation looks uncertain (e.g. no immediate status change, an async/manual-review message), flag `status` as `needs_review` and say what to check and when.
6. Update `last_updated` to today's date and commit the change to `charges.json` if it's in a git repo.

## General notes

- `charges.json` is the single source of truth. Always read the current file before acting on a subscription by name — don't rely on a summary from earlier in the conversation, the file may have changed.
- The same real-world service can have two independent billing records (e.g. web/Google Play billing vs. iOS App Store billing). Cancelling one does not cancel the other — check both when a cancellation doesn't seem to have stopped a charge.
- OAuth sign-in flows (Google especially) can get stuck in a browser-level error after several rapid sign-ins across different sites in one session. A fresh tab usually clears it before you conclude a site is unreachable.
