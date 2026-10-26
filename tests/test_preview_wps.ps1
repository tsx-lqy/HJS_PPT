$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot '..\skills\hjs_ppt\scripts\preview_wps.ps1'
$parseErrors = $null
$tokens = $null
[System.Management.Automation.Language.Parser]::ParseFile($script, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count) { throw 'PowerShell parse errors' }
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('hjs-wps-test-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $testRoot | Out-Null
try {
    $source = Join-Path $testRoot 'source deck.pptx'
    $fakeWps = Join-Path $testRoot 'wpp.exe'
    [IO.File]::WriteAllBytes($source, [byte[]](80,75,3,4,5,6))
    [IO.File]::WriteAllBytes($fakeWps, [byte[]](0))
    $before = (Get-FileHash -LiteralPath $source).Hash
    # Stub the process boundary. No executable is launched in this test.
    $global:hjsPreviewLaunches = @()
    function Start-Process {
        param($FilePath, $ArgumentList)
        $global:hjsPreviewLaunches += @{ file=$FilePath; args=$ArgumentList }
    }
    $probe = & $script -InputFile $source -WpsPath $fakeWps -CheckOnly | ConvertFrom-Json
    if ($probe.status -ne 'available' -or $global:hjsPreviewLaunches.Count -ne 0) { throw 'Probe should not launch.' }
    $a = & $script -InputFile $source -WpsPath $fakeWps | ConvertFrom-Json
    $b = & $script -InputFile $source -WpsPath $fakeWps | ConvertFrom-Json
    if ($a.preview -eq $b.preview -or $global:hjsPreviewLaunches.Count -ne 2) { throw 'Checkpoints must be distinct.' }
    if (!(Get-Item -LiteralPath $a.preview).IsReadOnly) { throw 'Preview must be read-only.' }
    if ((Get-FileHash -LiteralPath $a.preview).Hash -ne $before -or (Get-FileHash -LiteralPath $source).Hash -ne $before) { throw 'Bytes changed.' }
    if ($global:hjsPreviewLaunches[0].args -ne ('"'+$a.preview+'"')) { throw 'Snapshot path must be quoted.' }
    Write-Output 'PASS: probe, two distinct read-only snapshots, source hash and quoted launch arguments. WPS itself was not run.'
} finally {
    # This exact directory was freshly created above under the system temp dir.
    if ([IO.Path]::GetFullPath($testRoot).StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()), [StringComparison]::OrdinalIgnoreCase) -and (Split-Path $testRoot -Leaf).StartsWith('hjs-wps-test-')) {
        Remove-Item -LiteralPath $testRoot -Recurse -Force
    }
    Remove-Variable hjsPreviewLaunches -Scope Global -ErrorAction SilentlyContinue
}
