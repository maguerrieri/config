if ($args.count > 0) {
	$cloud = $args[0]
} else {
	$cloud = "dropbox"
}

Start-Process powershell -verb runAs {
	if (!(Get-Command choco -errorAction SilentlyContinue)) {
		Invoke-Expression ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'));
	}
	Start-Process powershell {
		./scripts/install.ps1 $args;
		./scripts/symlinks.ps1 $cloud $args;
	}
	Update-Help;
	explorer ./reg/hide_onedrive.reg;
}