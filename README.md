# SubReaper

Find every recurring subscription buried in your inbox, track it in one file, and cancel the ones you don't want — with Claude doing the searching, tracking, and clicking.

SubReaper isn't an app you install. It's a **skill** (a set of instructions) that you hand to [Claude Code](https://claude.com/product/claude-code) or claude.ai. Claude does the actual work live, in your own Gmail and your own browser — nothing about your subscriptions ever leaves your machine or gets sent to a third-party server.

## What it does

1. **Sweep** — searches your Gmail for receipts, renewal notices, and billing emails to build a list of every recurring charge it can find (subscriptions you signed up for years ago and forgot about included).
2. **Track** — writes everything to a single `charges.json` file: name, amount, billing cycle, how you sign in, current status, and the evidence it found. This file is yours, lives in your own repo, and is the source of truth going forward.
3. **Act** — on request, drives a real browser to cancel a subscription, declining retention offers unless you say otherwise, and updates the tracker with what actually happened.

## What it will never do

- Enter your password or 2FA code. When a site needs sign-in, it hands you the page, you sign in yourself, then it resumes.
- Solve a CAPTCHA or "verify you're human" check. It stops and tells you instead.
- Cancel anything without being asked. Discovery and cancellation are separate steps — it only tracks by default.
- Send your subscription data anywhere. Everything stays in the `charges.json` file in your own repo.

## Quickstart

1. Clone this repo (or just copy `SKILL.md` and `schema/` into a project).
2. Open the project in Claude Code.
3. Ask Claude to run a subscription sweep of your Gmail, using `SKILL.md` as the instructions and `schema/charges.schema.json` as the format for the tracker file it creates.
4. Review the `charges.json` it produces. Ask it to cancel whatever you don't want, one at a time.

See `schema/example-charges.json` for what a populated tracker looks like (fake data).

## Why this exists

Built out of a real cleanup: sweeping years of inbox history surfaced dozens of subscriptions that were still being charged monthly and long forgotten. SubReaper is that same workflow, generalized so anyone can run it on their own inbox.

## License

MIT — see `LICENSE`.
