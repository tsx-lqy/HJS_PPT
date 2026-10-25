param(
    [Parameter(Mandatory=$true)][string]$InputFile,
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [ValidateRange(640,3840)][int]$Width = 1600
)
# Windows desktop PowerPoint required. Export only; never save the source deck.
$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $InputFile).Path
if ([IO.Path]::GetExtension($inputPath) -ne '.pptx') { throw 'Input must be a .pptx file.' }
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Choose a new output directory.' }
$outputPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($OutputDirectory)
$beforeHash = (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash
$app = $null
$deck = $null
$count = 0
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($inputPath, -1, 0, 0)
    New-Item -ItemType Directory -Path $outputPath | Out-Null
    $height = [int][Math]::Round($Width * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
    $count = $deck.Slides.Count
    for ($page = 1; $page -le $count; $page++) {
        $file = Join-Path $outputPath ('slide-{0:D3}.png' -f $page)
        $deck.Slides.Item($page).Export($file, 'PNG', $Width, $height)
        if (!(Test-Path -LiteralPath $file) -or (Get-Item -LiteralPath $file).Length -eq 0) {
            throw "Slide $page did not produce a PNG."
        }
    }
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($null -ne $app -and $app.Presentations.Count -eq 0) { $app.Quit() }
}
$afterHash = (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash
if ($beforeHash -ne $afterHash) { throw 'Source file changed during rendering; investigate before delivery.' }
Write-Output "Rendered $count slides to $outputPath. Source SHA-256 unchanged. Visual review still required."
