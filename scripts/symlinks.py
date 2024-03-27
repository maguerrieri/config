#!/usr/bin/env python3

import argparse
import os
import platform
import sys
from pathlib import Path, PureWindowsPath
from typing import List

parser = argparse.ArgumentParser("Set up your symlinks")
parser.add_argument("--cloud")
parser.add_argument("--shortcloud")

args = parser.parse_args()
cloud = args.cloud or "icloud"
shortcloud = args.shortcloud or cloud

class UnsupportedPlatformException(Exception):
    pass

is_wsl = len(os.popen("which cmd.exe").readline().strip()) > 0

def make_home_path() -> Path:
    return Path("~").expanduser()
home_path = make_home_path()
print(f"Home directory: {home_path}")

def make_real_home_path() -> Path:
    if not is_wsl:
        return home_path

    wsl_path = Path(os.popen("wslpath $(cmd.exe /C \"echo %USERPROFILE%\")").readline().strip()).resolve()
    if wsl_path.exists():
        return wsl_path
    
    raise UnsupportedPlatformException()
real_home_path = make_real_home_path()
print(f"Platform home directory: {real_home_path}")

def make_cloud_path() -> Path:
    macos_path = Path("~").expanduser() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
    if macos_path.exists():
        return macos_path

    wsl_path = real_home_path / cloud
    if os.path.exists(wsl_path):
        return wsl_path
    
    raise FileNotFoundError(f"Can't find cloud directory named {cloud}")
cloud_path = make_cloud_path()
print(f"Cloud path: {cloud_path}")

wsl_root_path = PureWindowsPath(Path("/mnt/c").resolve())

def make_symlink(target: Path, source: Path, use_mklink=False):
    if use_mklink:
        cmd_path = os.popen("which cmd.exe").readline().strip()
        if len(cmd_path) > 0:
            win_source = "C:" / PureWindowsPath(source.relative_to(wsl_root_path))
            win_target = "C:" / PureWindowsPath(target.relative_to(wsl_root_path))

            os.system(f"cmd.exe /C \"mklink {win_source} {win_target}\"")
            return
    
    os.symlink(target, source)

class Link:
    def __init__(self,
                 target: Path,
                 name: Path,
                 platforms: List[str] | None=None,
                 archs: List[str] | None=None,
                 mklink_if_wsl: bool=False) -> None:
        self.target = target
        self.name = name
        self.platforms = platforms
        self.archs = archs
        self.mklink_if_wsl = mklink_if_wsl

    def __iter__(self):
        yield from [
            self.target,
            self.name,
            self.platforms,
            self.archs,
            self.mklink_if_wsl,
        ]

    def match(self, platform, arch):
        return ((self.platforms is None or platform in self.platforms)
                and (self.archs is None or arch in self.archs))

links = [
    Link(cloud_path, real_home_path / shortcloud),
    Link(cloud_path / "tech", real_home_path / "tech"),
    Link(cloud_path / "tech" / "config" / "profile" / "zshrc", real_home_path / ".zshrc"),
    Link(cloud_path / "tech" / "config" / "profile" / "zprofile", real_home_path / ".zprofile"),
    Link(cloud_path / "tech" / "config" / "profile" / "git", real_home_path / ".gitconfig"),
    Link(cloud_path / "tech" / "config" / "profile" / "gitignore", real_home_path / ".gitignore_global"),
    Link(
        cloud_path / "tech" / "config" / "profile" / "windows-terminal.json",
        real_home_path / "AppData" / "Local" / "Packages" / "Microsoft.WindowsTerminal_8wekyb3d8bbwe" / "LocalState"
            / "settings.json",
        ['wsl'],
        mklink_if_wsl=True
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "ibrew",
        home_path / ".local" / "bin" / "ibrew",
        platforms=['darwin'],
        archs=['arm'],
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "git-clear-hard",
        home_path / ".local" / "bin" / "git-cl",
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "git-clear",
        home_path / ".local" / "bin" / "git-clear",
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "git-submodule-update",
        home_path / ".local" / "bin" / "git-smu",
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "git-iamme",
        home_path / ".local" / "bin" / "git-iamme",
    ),
    Link(
        cloud_path / "tech" / "config" / "bin" / "git-iampg",
        home_path / ".local" / "bin" / "git-iampg",
    ),
    Link(
        home_path / "Developer" / "androidsigning" / "keystores" / "debug_pg.keystore",
        home_path / ".android" / "debug.keystore",
    ),
]

for link in links:
    if not link.match("wsl" if is_wsl else sys.platform, platform.processor()):
        continue

    if link.name.is_symlink():
        print(f"Deleting existing symlink `{link.name}`.")
        link.name.unlink()
    elif link.name.exists():
        backup = link.name.parent / f"_{link.name.name}"
        print(f"Moving existing `{link.name}` to `{backup}`.")
        if not backup.exists():
            link.name.rename(backup)
        else:
            print(f"`{backup}` also exists; aborting.")
            sys.exit()
    
    print(f"Linking `{link.name}` -> `{link.target}`.")
    make_symlink(link.target, link.name, link.mklink_if_wsl)
