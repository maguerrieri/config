$env:VAGRANT_DEFAULT_PROVIDER = "hyperv"
$cloud = "dropbox"

Set-Alias which Get-Command
Set-Alias top taskmgr

# Import-VisualStudioVars 140

function open {
	foreach ($path in $args) {
		foreach ($rpath in Resolve-Path $path) {
			explorer $rpath
		}
	}
}

function web ($arg) {
	if (!$arg.StartsWith("http://") -and !$arg.StartsWith("https://")) { 
		$arg = "http://" + $arg
	}
	explorer $arg
}

# winget completion
Register-ArgumentCompleter -Native -CommandName winget -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)
        [Console]::InputEncoding = [Console]::OutputEncoding = $OutputEncoding = [System.Text.Utf8Encoding]::new()
        $Local:word = $wordToComplete.Replace('"', '""')
        $Local:ast = $commandAst.ToString().Replace('"', '""')
        winget complete --word="$Local:word" --commandline "$Local:ast" --position $cursorPosition | ForEach-Object {
            [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
        }
}

# set up SSH agent
# run 
# 	> Unblock-File ssh-agent-utils.ps1
# to avoid security prompt at profile load
# . (Resolve-Path "~/$cloud/tech/config/profile/ssh-agent-utils.ps1")

# Chocolatey profile
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
	Import-Module "$ChocolateyProfile"
}
