# Installs every skill in this repo, replacing older copies:
#   ~/.claude/skills  -> Claude Code (Copilot in VS Code also reads it)
#   ~/.agents/skills  -> ChatGPT desktop / Codex (Copilot in VS Code also reads it)
# and builds ZIPs in dist/ to upload to Claude Desktop / claude.ai
# (Settings > Capabilities > Skills).
param(
    [switch]$SkipZips
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem

$repo = $PSScriptRoot
$skills = @(Get-ChildItem $repo -Directory |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
    Select-Object -ExpandProperty Name)

$targets = @(
    (Join-Path $HOME '.claude\skills'),
    (Join-Path $HOME '.agents\skills')
)

foreach ($target in $targets) {
    New-Item -ItemType Directory -Force $target | Out-Null
    foreach ($skill in $skills) {
        $dest = Join-Path $target $skill
        if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
        Copy-Item -Recurse (Join-Path $repo $skill) $dest
        Write-Host "installed $skill -> $dest"
    }
}

if ($SkipZips) { return }

$dist = Join-Path $repo 'dist'
New-Item -ItemType Directory -Force $dist | Out-Null

foreach ($skill in $skills) {
    # Build the ZIP by hand so entry paths use forward slashes.
    $zipPath = Join-Path $dist "$skill.zip"
    if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
    $zip = [IO.Compression.ZipFile]::Open($zipPath, 'Create')
    try {
        Get-ChildItem (Join-Path $repo $skill) -Recurse -File | ForEach-Object {
            $relative = $_.FullName.Substring($repo.Length + 1).Replace('\', '/')
            [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $relative) | Out-Null
        }
    } finally {
        $zip.Dispose()
    }
    Write-Host "built $zipPath"
}
