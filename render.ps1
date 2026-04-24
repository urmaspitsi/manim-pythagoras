param(
    [ValidateSet("low", "medium", "high")]
    [string]$Quality = "medium",
    [string]$Scene = "PythagoreanShortsPrototype",
    [string]$File = "shorts_pythagoras.py",
    [switch]$KeepCache
)

$ErrorActionPreference = "Stop"

$manimPath = Join-Path $PSScriptRoot ".venv\Scripts\manim.exe"
$mediaBase = [System.IO.Path]::GetFileNameWithoutExtension($File)
$mediaRoot = Join-Path $PSScriptRoot "media\videos\$mediaBase"
$mediaTextRoot = Join-Path $PSScriptRoot "media\texts"

if (-not (Test-Path $manimPath)) {
    throw "Manim executable not found at $manimPath"
}

$qualityFlag = switch ($Quality) {
    "low" { "-ql" }
    "medium" { "-qm" }
    "high" { "-qh" }
}

$args = @($qualityFlag)

if (-not $KeepCache) {
    Write-Host "Cleaning old Manim outputs for $mediaBase..."

    if (Test-Path $mediaRoot) {
        $resolvedMediaRoot = (Resolve-Path -LiteralPath $mediaRoot).Path
        $expectedRoot = (Join-Path $PSScriptRoot "media\videos")

        if (-not $resolvedMediaRoot.StartsWith($expectedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to delete unexpected media path: $resolvedMediaRoot"
        }

        Remove-Item -LiteralPath $resolvedMediaRoot -Recurse -Force
    }

    if (Test-Path $mediaTextRoot) {
        Remove-Item -LiteralPath $mediaTextRoot -Recurse -Force
    }

    $args += "--disable_caching"
}

$args += @($File, $Scene)

Write-Host "Rendering $Scene from $File at $Quality quality..."
if (-not $KeepCache) {
    Write-Host "Fresh render enforced: old outputs removed and Manim caching disabled."
}

& $manimPath @args
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not $KeepCache) {
    Get-ChildItem -Path $mediaRoot -Recurse -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -eq "partial_movie_files" } |
        ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Recurse -Force
        }

    if (Test-Path $mediaTextRoot) {
        Remove-Item -LiteralPath $mediaTextRoot -Recurse -Force
    }
}

$outputFile = Get-ChildItem -Path $mediaRoot -Recurse -File -Filter "$Scene.mp4" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $outputFile) {
    throw "Render finished, but no final output file named $Scene.mp4 was found under $mediaRoot"
}

Write-Host "Final output:"
Write-Host $outputFile.FullName
