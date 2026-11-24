param(
  [string]$RepositoryUrl = 'https://github.com/khant735/WCW-Backstage-Assault-RECOMP.git',
  [string]$Branch = 'main'
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git must be installed and available in PATH.' }
if (-not (Test-Path 'README.md') -or -not (Test-Path 'generated/SLUS_012.74_dispatch.c')) { throw 'Source export incomplete.' }
Write-Host 'Please create an EMPTY GitHub repository first (no README or .gitignore).' -ForegroundColor Yellow
Write-Host "Target remote: $RepositoryUrl"
$ok = Read-Host 'Publish this local source folder to that remote? Type YES'
if ($ok -cne 'YES') { Write-Host 'Cancelled'; exit 0 }
if (-not (Test-Path '.git')) { & git init -b $Branch; if ($LASTEXITCODE -ne 0) { throw 'git init failed' } }
& git add -A; if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
& git diff --cached --stat
& git commit -m 'Initial WCW Backstage Assault recompilation source, Stage 15B.3'
if ($LASTEXITCODE -ne 0) { throw 'git commit failed: configure git user.name and user.email, or check existing commits.' }
$remote = & git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0 -and $remote -ne $RepositoryUrl) { throw "Origin already points to $remote; refusing to replace it." }
if ($LASTEXITCODE -ne 0) { & git remote add origin $RepositoryUrl; if ($LASTEXITCODE -ne 0) { throw 'git remote add failed' } }
& git push -u origin $Branch
if ($LASTEXITCODE -ne 0) { throw 'Push failed. Verify the empty repository exists and your GitHub credentials have write access.' }
Write-Host "Published to $RepositoryUrl" -ForegroundColor Green
