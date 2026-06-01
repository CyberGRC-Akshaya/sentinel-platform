# Stage 4 — Frontend AI Integration Prep

## Objective

Prepare for AI Assist UI integration without blindly modifying `frontend/app/page.tsx`.

## Why prep is required

`page.tsx` is still large and contains many states, fetch functions, tabs, actions, and render branches. A blind patch may break the working product.

## Safe sequence

1. Confirm backend AI service works and is committed.
2. Extract frontend state/function/render snippets.
3. Review exact insertion points.
4. Add AI Assist state variables.
5. Add `runAiAssist()` function.
6. Add one AI Assist button in the safest existing action area.
7. Render AI Assist output in a contained panel.
8. Test fallback mode first.
9. Commit only after app builds and endpoint works.

## AI UI principle

The UI must make it obvious that:

- AI output is assistive
- deterministic Sentinel scoring remains primary
- human review is required
- no score is automatically changed
- fallback mode is acceptable when AI is disabled

## Do not

- add a new tab yet
- redesign the screen
- replace existing Board Pack or Evidence Requests
- send secrets to frontend
- hardcode API keys
- require OpenAI key to use the app
