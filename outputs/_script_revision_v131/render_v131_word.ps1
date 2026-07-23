$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$inputPath = Join-Path $root '文本\奔月_正式分镜稿_V1.3.1.docx'
$outputDir = Join-Path $PSScriptRoot 'render_word'
$pdfPath = Join-Path $outputDir '奔月_正式分镜稿_V1.3.1.pdf'

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($inputPath, $false, $true)
    try {
        $doc.ExportAsFixedFormat($pdfPath, 17)
    }
    finally {
        $doc.Close($false)
    }
}
finally {
    $word.Quit()
}

& pdftoppm -png -r 150 $pdfPath (Join-Path $outputDir 'page')
