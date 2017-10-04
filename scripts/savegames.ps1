if ($args.Contains("gnomoria")) {
	New-Symlink "$home\Documents\My Games\Gnomoria" "$home\Dropbox\games\video\saves\Gnomoria";
}
if ($args.Contains("locomotion")) {
	New-Symlink "${env:ProgramFiles(x86)}\GOG Games\Chris Sawyer's Locomotion\Single Player Saved Games" "$home\Dropbox\games\video\saves\Locomotion";
}
if ($args.Contains("toothandtail")) {
	New-Symlink "$env:APPDATA\ToothAndTail\" "$home\dropbox\games\video\saves\ToothAndTail";
}
