# Cursor Prompt — Stage 2 Codebase Analysis

You are helping stabilize Sentinel Evidence Defensibility Workbench.

Do not add features.

Analyze the repository and produce a refactor plan only.

Project goals:
- preserve current behavior
- reduce build break risk
- split large files safely
- improve maintainability
- keep Docker workflow working

Please inspect:
- frontend/app/page.tsx
- frontend/app/globals.css
- backend/app/main.py
- docker-compose.yml
- package.json
- requirements.txt

Output:
1. current structure summary
2. high-risk files
3. recommended split plan
4. safest first refactor
5. exact files to create
6. tests to run after each change

Do not modify files yet.
