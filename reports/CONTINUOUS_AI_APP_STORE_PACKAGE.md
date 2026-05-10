# Continuous AI App Store / TestFlight Package Draft

## Current Status

- App name: Continuous AI
- Current build type in workspace: web app / Base44 app, not a native iOS Xcode project
- Local grounding bridge: `http://localhost:8787`
- Local bridge state: working in development on this laptop
- Current Cloudflare bridge: `https://helping-cells-separately-eggs.trycloudflare.com`
- Bridge mode: temporary quick tunnel for immediate app/browser testing

## Latest Readiness Findings

The latest mobile-readiness report identifies these blocking issues for App Store / TestFlight readiness:

| Area | Status | Notes |
| --- | --- | --- |
| Safe area handling | Blocking | Layouts need safe-area-aware spacing on iPhone. |
| User account deletion | Blocking | A working account deletion path is required if login exists. |
| Unified navigation / back stack | Blocking | Child pages need explicit back navigation and preserved stack behavior. |
| Bottom tabs / stack preservation | Blocking | Tab switching should not destroy nested route state. |
| Overscroll / sticky elements | Blocking | Mobile scrolling behavior needs cleanup. |
| System gestures / selection interference | Blocking | Unwanted gesture capture and selection blocking must be removed or constrained. |
| Dark mode | Warning | Must render cleanly in dark mode. |
| Dropdowns / selection controls | Warning | Touch targets and mobile interaction need polish. |
| Screen transitions | Warning | Animations should remain smooth and app-like. |
| Pull-to-refresh | Pass | Keep as-is. |
| Performance | Pass | Keep current performance characteristics. |
| Responsiveness | Pass | Mobile-first layout is already solid. |
| Accessibility / UX polish | Pass | Preserve current polish while fixing blockers. |

## Known Failure Mode

The current query fallback that shows a “Resolution Assurance Notice” appears when the grounding/search path cannot complete. That path should preserve the user’s question, offer retry, and avoid clearing state so the app never feels like it lost the request.

## Important Distribution Constraint

The grounding bridge now has a Cloudflare tunnel in front of it for browser access. That is fine for immediate testing, but the current quick tunnel is **not** suitable as the only backend for an App Store release or for external TestFlight testers.

For public distribution, we need one of these:

1. A hosted API endpoint accessible from testers' devices.
2. An on-device/offline mode that does not depend on the local laptop.
3. A hybrid build where local mode is dev-only and public mode uses a hosted bridge.

## Existing IPA Caveat

There is an `.ipa` file in the workspace (`ios-2.117896.1.ipa`), but it belongs to `RelayLife` rather than Continuous AI, so it cannot be used as the App Store binary for this app without major rework.

## What Is Ready

- Product scope and app direction are defined.
- Bridge contract is known:
  - `GET /stats`
  - `POST /ground`
  - `GET /question-capsules`
  - `POST /answer`
- Functional areas already mapped:
  - Dashboard
  - Emails
  - Files
  - Contacts
  - Analytics
  - Pricing
  - Settings
  - Privacy
  - Help
  - Login / Sign Up

## What Still Needs To Happen Before Submission

| Item | Status | Notes |
| --- | --- | --- |
| Native iOS wrapper / Xcode project | Missing | Needed for App Store / TestFlight upload |
| Hosted production API | Missing | Cannot rely on local laptop for public build |
| Apple Developer account | Needed | Required for App Store Connect and signing |
| App Store Connect API key | Optional but helpful | Helps automate metadata and build upload |
| Bundle ID / signing assets | Needed | Required for code signing and upload |
| App icon | Needed | Required for App Store listing |
| Screenshots | Needed | Required for App Store listing |
| Privacy policy URL | Needed | Required for listing review |
| Support URL | Needed | Required for listing review |

## Suggested Screenshot Set

### iPhone

Capture these states in the app:

1. Dashboard with Bridge Status connected
2. AI composer open with grounded answer preview
3. Upload flow showing files ingested
4. Emails view showing triage and reply drafting
5. Files view showing summaries and extracted actions
6. Contacts view showing linked people and history
7. Analytics view showing usage and completion metrics
8. Settings / Privacy view showing delete and consent controls
9. Pricing view showing Free / Pro / Enterprise
10. Offline / disconnected bridge state with retry button

### Recommended Sizes

- If the app runs on iPhone, App Store Connect commonly expects 6.9-inch screenshots for the current iPhone set, with other sizes scaled as needed.
- If the app runs on iPad, add iPad screenshots too.

## Suggested Store Metadata

| Field | Draft |
| --- | --- |
| App Name | Continuous AI |
| Subtitle | Grounded AI office assistant |
| Category | Productivity |
| Secondary Category | Business |
| Description | A grounded AI workspace for emails, files, contacts, and action items. Continuous AI helps you organise, summarise, draft replies, and ask questions about your working set with evidence-backed responses and clear status handling. |
| Keywords | email, assistant, productivity, files, contacts, grounded AI, office, workflow, summaries, drafts |
| Age Rating | 4+ or 12+ depending on final content review |
| Support URL | To be set |
| Privacy Policy URL | To be set |

## TestFlight Notes

- Internal testing can be used to verify the build before broader release.
- External TestFlight testers require Apple review of the beta build and metadata.
- The build should open, log in, upload files, and reach a grounded answer state without relying on my laptop being present.

## Submission Package Contents

- App icon set
- App Store description and keywords
- Privacy policy
- Support contact
- Screenshots for required device sizes
- Signed iOS build or TestFlight build
- App Review notes
- Demo account credentials if review login is required

## Next Best Step

If you want this live, the fastest path is:

1. Add or generate a native iOS wrapper around the app.
2. Move the grounding bridge to a hosted endpoint or add a public-mode fallback.
3. Build the iOS binary.
4. Upload the build to App Store Connect or TestFlight.
5. Finish metadata and screenshots.
