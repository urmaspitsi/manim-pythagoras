param(
    [ValidateSet("low", "medium", "high")]
    [string]$Quality = "medium",
    [string]$Scene = "PythagoreanShortsPrototype",
    [string]$File = "shorts_pythagoras.py",
    [switch]$Fresh
)

$ErrorActionPreference = "Stop"

$manimPath = Join-Path $PSScriptRoot ".venv\Scripts\manim.exe"
$mediaBase = [System.IO.Path]::GetFileNameWithoutExtension($File)
$mediaRoot = Join-Path $PSScriptRoot "media\videos\$mediaBase"

if (-not (Test-Path $manimPath)) {
    throw "Manim executable not found at $manimPath"
}

$qualityFlag = switch ($Quality) {
    "low" { "-ql" }
    "medium" { "-qm" }
    "high" { "-qh" }
}

$args = @($qualityFlag)

if ($Fresh) {
    if (Test-Path $mediaRoot) {
        Get-ChildItem -Path $mediaRoot -Recurse -Directory |
            Where-Object { $_.Name -eq $Scene -and $_.Parent.Name -eq "partial_movie_files" } |
            ForEach-Object {
                Remove-Item -LiteralPath $_.FullName -Recurse -Force
            }

        Get-ChildItem -Path $mediaRoot -Recurse -File -Filter "$Scene.mp4" |
            ForEach-Object {
                Remove-Item -LiteralPath $_.FullName -Force
            }
    }

    $args += "--disable_caching"
}

$args += @($File, $Scene)

Write-Host "Rendering $Scene from $File at $Quality quality..."
if ($Fresh) {
    Write-Host "Fresh render requested: caching disabled for this run."
}

& $manimPath @args
