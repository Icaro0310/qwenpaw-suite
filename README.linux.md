# qwenpaw-suite, Linux guide

This guide covers Linux setup only. See [README.md](README.md) for features, shared commands, limitations, and the safety model.

Linux uses the extended runtime: local execution plus optional Devin VM/QwenPaw delegation when this artifact supports it.

## Prerequisites

- Follow the requirements listed in [README.md](README.md).

## Install

This related project is not installed by the DevKit. See its main README for current setup instructions.

## Devin paths

Session data normally lives under `${XDG_DATA_HOME:-$HOME/.local/share}/devin/cli/`; UI state and ACP stores under `${XDG_CONFIG_HOME:-$HOME/.config}/Devin/User/`.
Use `--data-dir`/`--config-dir` where the tool documents them for non-default locations.

## Environment notes

- Delegated runtime is optional; this guide installs local tooling only.
- Linux can use additional compute or Linux-compatible delegated tooling when available.
- macOS is planned but not claimed as tested.

## Linux specifics

- **Installer choice:** `uv tool install` is the recommended path (isolated environment, managed Python). `pipx install` works identically for PyPI packages; `pip install --user` is the last-resort fallback, no isolation, watch dependency conflicts.
- **PATH:** executables land in `~/.local/bin`. If a command is not found, add `export PATH="$HOME/.local/bin:$PATH"` to `~/.bashrc`/`~/.zshrc` and open a new shell.
- **Distros:** tested on Ubuntu; Debian, Fedora and Arch follow the same steps, only `uv`/Python acquisition differs (distro package or the uv installer script).
- **Headless and minimal environments:** no display is needed, every CLI is text-only. In containers or WSL, install `uv` and Git and follow the same steps; `XDG_*` paths resolve normally.
- **Permissions:** tools read Devin data under `$XDG_DATA_HOME/devin` and write only their own config/state, no root or sudo is required.
- **Scheduling:** optional recurring work belongs to `systemd --user` timers or cron; installation never creates jobs.

## Starting the bridge

`bridge/start-all.sh` is the POSIX equivalent of `start-all.bat` — the same
steps in the same order: it cds to `bridge/`, defaults `BRIDGE_HOST` to
`127.0.0.1`, creates `bridge/.venv` when missing, installs
`bridge/requirements.txt` into it, and execs `bridge.py` in the foreground:

```bash
./bridge/start-all.sh
```

### Optional systemd --user service

`bridge/qwenpaw-bridge.service` runs the bridge as a user service (no root).
It calls `start-all.sh`, so the venv bootstrap stays the single entry point;
secrets such as `BRIDGE_API_KEY` live outside the repo in
`~/.config/qwenpaw-suite/bridge.env` (`KEY=value` lines, optional file):

```bash
mkdir -p ~/.config/systemd/user
sed "s|@BRIDGE_DIR@|$PWD/bridge|" bridge/qwenpaw-bridge.service \
    > ~/.config/systemd/user/qwenpaw-bridge.service
systemctl --user daemon-reload
systemctl --user enable --now qwenpaw-bridge.service
```

Run the `sed` line from the repository root so `@BRIDGE_DIR@` becomes the
absolute path of `bridge/`. Logs: `journalctl --user -u qwenpaw-bridge -f`.
Nothing is scheduled or enabled automatically — the unit is opt-in.

## Troubleshooting

- Follow the platform-specific troubleshooting notes in the main README.
