# VS Code Setup Guide for Sentinel

## Step 1 — Open project

Open VS Code.

Go to:

```text
File → Open Folder
```

Select:

```text
C:\Users\Akshaya\Desktop\EyeOnBits-Sentinel
```

## Step 2 — Open terminal

In VS Code:

```text
Terminal → New Terminal
```

If terminal does not open in the project folder, type:

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
```

## Step 3 — Recommended VS Code extensions

Free extensions only:

| Extension | Why |
|---|---|
| Python | FastAPI/backend editing |
| Pylance | Python IntelliSense |
| ESLint | Frontend code checks |
| Prettier | Formatting |
| Docker | View containers/files |
| GitLens | Git history visibility |
| Markdown All in One | Docs editing |

Do not install paid tools unless you decide later.

## Step 4 — Run app

```powershell
docker compose down --remove-orphans
docker compose up --build
```

Open:

```text
http://localhost:3000
http://localhost:8000/api/health
```

## Step 5 — Stop app

In the running terminal:

```text
Ctrl + C
```

Then:

```powershell
docker compose down --remove-orphans
```
