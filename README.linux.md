# qwenpaw-suite — Linux guide

This guide covers Linux setup only. See [README.md](README.md) for features, shared commands, limitations, and the safety model.

Linux uses the extended runtime: local execution plus optional Devin VM/QwenPaw delegation when this artifact supports it.

## Prerequisites

- Follow the requirements listed in [README.md](README.md).

## Install

This related project is not installed by the DevKit. See its main README for current setup instructions.

## Devin paths

Session data normally lives under `${XDG_DATA_HOME:-$HOME/.local/share}/devin/cli/`; UI state and ACP stores under `${XDG_CONFIG_HOME:-$HOME/.config}/Devin/User/`.
Use the tool's documented `--data-dir` or `--config-dir` flags for non-default locations.

## Environment notes

- Delegated runtime is optional; this guide installs local tooling only.
- Linux can use additional compute or Linux-compatible delegated tooling when available.
- macOS is planned but not claimed as tested.

## Troubleshooting

- Follow the platform-specific troubleshooting notes in the main README.
