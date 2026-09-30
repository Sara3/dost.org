#!/bin/zsh
cd -- "${0:A:h}" || exit 1
export PATH="$HOME/.pyenv/shims:/opt/homebrew/bin:/usr/local/bin:$PATH"
python3 scripts/prepare_media.py --watch
