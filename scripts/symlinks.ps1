$cloud = $args[0];
$args = $args[1..($args.length)];

$links = 
	@("$env:APPDATA\Code\User\settings.json","code.json"),
	@($profile,"powershell.ps1")

function link($link) {
	$source = $link[0]
	$dest = $link[1]
	echo (Split-Path $source)
	echo (Split-Path $dest -leaf)
	echo ("$home\$cloud\tech\config\profile\" + (Split-Path $dest -leaf))
	if (!(Test-Path (Split-Path $source))) {
		New-Item (Split-Path $source) -itemtype directory;
	}
	if (Test-Path $source) {
		Remove-Item $source;
	}
	New-Symlink $source ("$home\$cloud\tech\config\profile\" + (Split-Path $dest -leaf));
}

$links | ForEach-Object { link($_) }
