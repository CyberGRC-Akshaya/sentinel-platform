# GitHub Commit Commands

After applying this pack:

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
git add README.md docs launch-assets
git commit -m "Prepare Sentinel text-first launch assets"
git push
git tag -a v10.4-text-first-launch -m "Sentinel v10.4 - Text-first launch assets"
git push origin v10.4-text-first-launch
```

If Git says nothing to commit, run:

```powershell
git status
```
