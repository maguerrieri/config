$profiles_dir = $args[0];
$args = $args[1..($args.length)];

if ($profiles_dir) {
	$links = 
		@("$env:APPDATA\Code\User\settings.json", "code.json"),
		@($profile, "powershell.ps1")
	
	function link($link) {
		$source = $link[0]
		$dest = $link[1]
		Write-Output (Split-Path $source)
		Write-Output (Split-Path $dest -leaf)
		Write-Output ("$profiles_dir\" + (Split-Path $dest -leaf))
		if (!(Test-Path (Split-Path $source))) {
			New-Item (Split-Path $source) -itemtype directory;
		}
		if (Test-Path $source) {
			Remove-Item $source;
		}
		New-Symlink $source ("$profiles_dir\" + (Split-Path $dest -leaf));
	}
	
	$links | ForEach-Object { link($_) }
} else {
	Write-Output "Missing profiles directory"
}
