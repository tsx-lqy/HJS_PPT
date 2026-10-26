param(
    [Parameter(Mandatory=$true)][string]$InputFile,
    [string]$PreviewDirectory,
    [string]$WpsPath,
    [switch]$CheckOnly
)
# A finite checkpoint operation. Never starts a background watcher, closes WPS,
# saves a user's open document, or modifies the source PPTX.
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $InputFile).Path
if ([IO.Path]::GetExtension($sourcePath) -ne '.pptx') { throw 'Input must be a .pptx file.' }

if ($WpsPath) {
    $executable = (Resolve-Path -LiteralPath $WpsPath).Path
    if ([IO.Path]::GetFileName($executable) -ine 'wpp.exe') { throw 'WpsPath must point to wpp.exe.' }
} else {
    $candidates = @()
    $command = Get-Command wpp.exe -ErrorAction SilentlyContinue
    if ($command) { $candidates += $command.Source }
    foreach ($key in @(
        'Registry::HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\App Paths\wpp.exe',
        'Registry::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\App Paths\wpp.exe',
        'Registry::HKEY_LOCAL_MACHINE\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\wpp.exe')) {
        if (Test-Path -LiteralPath $key) { $candidates += (Get-Item -LiteralPath $key).GetValue('') }
    }
    foreach ($base in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:LOCALAPPDATA)) {
        if (!$base) { continue }
        $office = Join-Path $base 'Kingsoft\WPS Office'
        if (Test-Path -LiteralPath $office) {
            $candidates += Get-ChildItem -LiteralPath $office -Filter wpp.exe -File -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
        }
    }
    $executable = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } | Select-Object -First 1
}
if (!$executable) {
    if ($CheckOnly) {
        [pscustomobject]@{ status='not_installed'; input=$sourcePath; hint='Install WPS separately or provide -WpsPath.' } | ConvertTo-Json -Compress
        exit 0
    }
    throw 'WPS Presentation was not found. Provide -WpsPath; no software was installed.'
}
if ($CheckOnly) {
    [pscustomobject]@{ status='available'; executable=$executable; input=$sourcePath } | ConvertTo-Json -Compress
    exit 0
}
if (!$PreviewDirectory) { $PreviewDirectory = Join-Path ([IO.Path]::GetDirectoryName($sourcePath)) 'wps-preview' }
$previewRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($PreviewDirectory)
New-Item -ItemType Directory -Path $previewRoot -Force | Out-Null
$name = [IO.Path]::GetFileNameWithoutExtension($sourcePath) + '-preview-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8) + '.pptx'
$snapshot = Join-Path $previewRoot $name
$sourceHash = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
Copy-Item -LiteralPath $sourcePath -Destination $snapshot
if ((Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash -ne $sourceHash -or (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash -ne $sourceHash) {
    throw 'PPTX changed while copying; save the deck fully and retry this checkpoint.'
}
(Get-Item -LiteralPath $snapshot).IsReadOnly = $true
# This visible window is intentional: the user requested a WPS preview.
Start-Process -FilePath $executable -ArgumentList ('"' + $snapshot + '"') | Out-Null
[pscustomobject]@{ status='launch_requested'; preview=$snapshot; sourceSha256=$sourceHash; readOnly=$true; visualVerification='pending' } | ConvertTo-Json -Compress
