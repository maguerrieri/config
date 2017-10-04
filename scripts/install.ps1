$android = $args.Contains("android");

choco install -y pscx; # Powershell Community Extensions

choco install -y visualstudiocode visualstudio2017community ./pkg/git.install.2.10.0.nupkg python3 sqlite.shell; # developer tools
choco pin add -n="git.install" # pin git to our modified package (the public one doesn't support /NoShellExt)
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine) + ";$env:ProgramFiles\Git\usr\bin", [EnvironmentVariableTarget]::Machine); # add Unix tools included with git to PATH
if ($android) { # install Android Studio (+ SDK, etc) if argument was passed
	choco install -y androidstudio -version 2.0.0.20;
}

choco install -y winrar paint.net windirstat spotify steam battle.net slack dropbox geforce-experience; # other
