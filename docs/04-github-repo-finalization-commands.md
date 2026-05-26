# GitHub Repo Finalization Commands

After screenshots are saved:

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
git status
git add README.md docs github-assets
git commit -m "Polish Sentinel GitHub presentation and demo assets"
git push
git tag -a v10.3.1-launch-execution -m "Sentinel v10.3.1 - Launch execution assets"
git push origin v10.3.1-launch-execution
```
