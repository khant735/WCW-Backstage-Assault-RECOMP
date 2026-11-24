param([string]$ToolchainZip = '', [string]$Framework = "$PSScriptRoot/psxrecomp")
$ErrorActionPreference = 'Stop'
$Framework = [IO.Path]::GetFullPath($Framework)
$cli = Join-Path $Framework 'psxrecomp_cli.py'
if (!(Test-Path $cli)) { throw 'Extract the supplied PSXRecomp source into psxrecomp or pass -Framework.' }
$args2 = @($cli,'ensure-toolchain','--project-root',$PSScriptRoot,'--json-progress')
if ($ToolchainZip) { $args2 += @('--toolchain-zip',$ToolchainZip) }
$progress = & python @args2
if ($LASTEXITCODE -ne 0) { throw 'Toolchain setup failed.' }
$result = $progress | Where-Object { $_ -like '{*' } | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.event -eq 'result' } | Select-Object -Last 1
if (!$result.toolchain_bin) { throw 'No toolchain bin returned.' }
$env:Path = "$($result.toolchain_bin);$env:Path"
$build = Join-Path $PSScriptRoot 'build-release'
& cmake -S $PSScriptRoot -B $build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ "-DPSXRECOMP_ROOT=$Framework" -DPSXRECOMP_BIOS_STEMS=OpenBIOS -DPSX_REWIND=OFF -DPSX_SETUP_WIZARD=OFF -DPSX_DEBUG_TOOLS=ON
if ($LASTEXITCODE -ne 0) { throw 'Configure failed.' }
& cmake --build $build --target psx-runtime
if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
Copy-Item (Join-Path $PSScriptRoot 'game.toml') $build -Force
