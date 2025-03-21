# Navigate to the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $scriptDir

# Define paths
$frontendDir = "$scriptDir\client"
$frontendBuild = "$scriptDir\public"
$distPath = "$frontendDir\dist"

# Ensure 'public' exists
if (-Not (Test-Path $frontendBuild)) {
    New-Item -ItemType Directory -Path $frontendBuild | Out-Null
}

# Check if Vite build already exists
if (Test-Path "$distPath\index.html") {
    Write-Host "✅ Vite UI is already built."
} else {
    Write-Host "⚡ Building Vite UI..."

    # Run npm install and build
    Set-Location -Path $frontendDir
    npm install
    npm run build
    Set-Location -Path $scriptDir
}

# Copy 'dist' to 'public'
if (Test-Path $distPath) {
    Remove-Item -Recurse -Force $frontendBuild
    Copy-Item -Path $distPath -Destination $frontendBuild -Recurse
    Write-Host "✅ Vite UI built successfully!"
} else {
    Write-Host "❌ Vite build failed: 'dist/' folder not found!"
}

# Start Flask
Write-Host "🚀 Starting Flask server..."
python app.py
