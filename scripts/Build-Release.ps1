[CmdletBinding()]
param(
    [string]$Python = ".\.venv\Scripts\python.exe",
    [string]$Version = "1.0.0-rc2"
)

$ErrorActionPreference = 'Stop'
$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pythonPath = [System.IO.Path]::GetFullPath((Join-Path $projectRoot $Python))
if (-not $pythonPath.StartsWith($projectRoot, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Interprete Python esterno al progetto.' }
if (-not (Test-Path -LiteralPath $pythonPath)) { throw "Interprete non trovato: $pythonPath" }
$artifactsRoot = Join-Path $projectRoot 'artifacts\release'
$packageName = "IgnitionPropertiesConverter-$Version-win-x64-unsigned"
$packageRoot = Join-Path $artifactsRoot $packageName
if (-not $packageRoot.StartsWith($projectRoot, [System.StringComparison]::OrdinalIgnoreCase)) { throw 'Percorso artifact non sicuro.' }
if (Test-Path -LiteralPath $packageRoot) { Remove-Item -LiteralPath $packageRoot -Recurse -Force }
New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null

Push-Location $projectRoot
try {
    & $pythonPath -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Test non superati.' }
    & $pythonPath -m PyInstaller --clean --noconfirm main.spec
    if ($LASTEXITCODE -ne 0) { throw 'Build PyInstaller non riuscita.' }

    $builtExecutable = Join-Path $projectRoot 'dist\IgnitionPropertiesConverter.exe'
    if (-not (Test-Path -LiteralPath $builtExecutable)) { throw 'Eseguibile atteso non prodotto.' }
    $executable = Join-Path $packageRoot 'IgnitionPropertiesConverter.exe'
    Copy-Item -LiteralPath $builtExecutable -Destination $executable

    $signature = Get-AuthenticodeSignature -LiteralPath $executable
    if ($signature.Status -ne 'NotSigned') { throw "Stato firma inatteso per il candidato unsigned: $($signature.Status)." }

    $docsRoot = Join-Path $packageRoot 'docs'
    $licensesRoot = Join-Path $packageRoot 'licenses'
    $examplesRoot = Join-Path $packageRoot 'examples'
    New-Item -ItemType Directory -Path $docsRoot,$licensesRoot,$examplesRoot -Force | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $projectRoot 'docs\public') -File | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $docsRoot }
    Copy-Item -LiteralPath (Join-Path $projectRoot 'README.md') -Destination (Join-Path $docsRoot 'README.md')
    Copy-Item -LiteralPath (Join-Path $projectRoot 'LICENSE') -Destination (Join-Path $licensesRoot 'PROJECT-MIT-LICENSE.txt')
    Copy-Item -LiteralPath (Join-Path $projectRoot 'THIRD_PARTY_NOTICES.md') -Destination $licensesRoot
    Get-ChildItem -LiteralPath (Join-Path $projectRoot 'examples') -File | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $examplesRoot }
    $screenshotsSource = Join-Path $projectRoot 'artifacts\screenshots'
    if (Test-Path -LiteralPath $screenshotsSource) {
        Copy-Item -LiteralPath $screenshotsSource -Destination (Join-Path $packageRoot 'screenshots') -Recurse
    }

    & $pythonPath (Join-Path $projectRoot 'scripts\Collect-Licenses.py') (Join-Path $licensesRoot 'third-party')
    if ($LASTEXITCODE -ne 0) { throw 'Raccolta licenze non riuscita.' }
    & $pythonPath -c "from converter import export_to_excel; export_to_excel(['examples/Language_it.properties','examples/Language_en.properties'], r'$examplesRoot\Translations-example.xlsx')"
    if ($LASTEXITCODE -ne 0) { throw 'Generazione workbook di esempio non riuscita.' }

    Set-Content -LiteralPath (Join-Path $packageRoot 'VERSION.txt') -Value $Version -Encoding ascii
    Set-Content -LiteralPath (Join-Path $packageRoot 'SIGNING_STATUS.txt') -Value @(
        'NOT SIGNED - PUBLIC PRE-RELEASE'
        "Authenticode status: $($signature.Status)"
        'This pre-release is intentionally distributed without Authenticode signing.'
        'Windows may display a security warning. Verify the published SHA-256 checksum before running it.'
        'Pre-release software: no individual support is provided and use is at the user''s own risk.'
    ) -Encoding utf8

    $forbiddenExtensions = @('.py', '.pyc', '.pfx', '.p12', '.pem', '.key', '.db', '.sqlite', '.sqlite3')
    $forbidden = Get-ChildItem -LiteralPath $packageRoot -Recurse -File | Where-Object {
        ($forbiddenExtensions -contains $_.Extension.ToLowerInvariant()) -or
        ($_.BaseName -match '(?i)(credential|secret|token)')
    }
    if ($forbidden) { throw "File vietati nel pacchetto: $($forbidden.FullName -join ', ')" }

    $contents = Get-ChildItem -LiteralPath $packageRoot -Recurse -File |
        Where-Object { $_.Name -ne 'PACKAGE_CONTENTS_SHA256.txt' } |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($packageRoot.Length + 1).Replace('\', '/')
            $fileHash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            "$fileHash  $relative"
        }
    Set-Content -LiteralPath (Join-Path $packageRoot 'PACKAGE_CONTENTS_SHA256.txt') -Value $contents -Encoding ascii

    $zip = Join-Path $artifactsRoot "$packageName.zip"
    if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }
    Compress-Archive -LiteralPath $packageRoot -DestinationPath $zip -CompressionLevel Optimal
    $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
    Set-Content -LiteralPath "$zip.sha256" -Value "$hash  $(Split-Path -Leaf $zip)" -Encoding ascii
    Write-Output "PACKAGE=$packageRoot"
    Write-Output "ZIP=$zip"
    Write-Output "SHA256=$hash"
    Write-Output 'STATUS=UNSIGNED_PUBLIC_PRERELEASE'
}
finally {
    Pop-Location
}
