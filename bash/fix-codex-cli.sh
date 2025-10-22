#!/usr/bin/env bash
# Purpose: Replace npm @openai/codex wrapper with the official Codex CLI binary.
# Usage (inside container):
#   bash ./bash/fix-codex-cli.sh
# Or from host (container name uwm-dev):
#   podman cp bash/fix-codex-cli.sh uwm-dev:/tmp/
#   podman exec -it uwm-dev bash /tmp/fix-codex-cli.sh

set -euo pipefail

log() { printf "[fix-codex] %s\n" "$*"; }
die() { printf "[fix-codex] ERROR: %s\n" "$*" >&2; exit 1; }

need() { command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"; }

need curl
need tar

maybe_load_fnm() {
  if command -v fnm >/dev/null 2>&1; then
    # shellcheck disable=SC1090
    eval "$(fnm env)" || true
  fi
}

uninstall_npm_wrapper() {
  maybe_load_fnm
  if command -v npm >/dev/null 2>&1; then
    # Try to uninstall via npm (non-fatal if missing)
    npm -g rm @openai/codex >/dev/null 2>&1 || true
    # Also remove any leftover codex shim in npm's global bin dir
    local nb
    nb=$(npm bin -g 2>/dev/null || true)
    if [ -n "${nb:-}" ] && [ -e "$nb/codex" ]; then
      log "Removing stale npm shim: $nb/codex"
      rm -f "$nb/codex" "$nb/codex.cmd" 2>/dev/null || true
    fi
  fi
  # Do NOT invoke pnpm/yarn to avoid Corepack prompts; purge is handled via PATH scan.
}

detect_arch() {
  local arch
  arch=$(uname -m)
  case "$arch" in
    x86_64)  echo "x86_64-unknown-linux-musl" ;;
    aarch64|arm64) echo "aarch64-unknown-linux-musl" ;;
    *) die "Unsupported architecture: $arch" ;;
  esac
}

get_latest_version() {
  # Prefer a fast, low-rate HEAD redirect to get the tag name
  local eff
  eff=$(curl -fsSIL -o /dev/null -w '%{url_effective}' https://github.com/openai/codex/releases/latest)
  printf '%s\n' "${eff##*/}"
}

install_binary() {
  local arch tag url tmp bin
  arch=$(detect_arch)
  tag=${CODEX_VERSION:-$(get_latest_version)}
  [ -n "$tag" ] || die "Could not determine latest Codex release tag"
  url="https://github.com/openai/codex/releases/download/${tag}/codex-${arch}.tar.gz"

  log "Downloading Codex ${tag} for ${arch} ..."
  tmp=$(mktemp -d)
  curl -fsSL "$url" -o "$tmp/codex.tgz"
  tar -xzf "$tmp/codex.tgz" -C "$tmp"
  bin=$(find "$tmp" -maxdepth 1 -type f -name 'codex-*' | head -n1)
  [ -n "$bin" ] || die "Failed to locate extracted codex binary"

  # Try installing to /usr/local/bin first (preferred)
  if [ -w /usr/local/bin ]; then
    install "$bin" /usr/local/bin/codex
  else
    if command -v sudo >/dev/null 2>&1; then
      sudo install "$bin" /usr/local/bin/codex
    else
      # Fallback to user bin
      mkdir -p "$HOME/.local/bin"
      install "$bin" "$HOME/.local/bin/codex"
      case ":$PATH:" in
        *":$HOME/.local/bin:"*) : ;;
        *) log "Adding \"$HOME/.local/bin\" to PATH for current session"; export PATH="$HOME/.local/bin:$PATH" ;;
      esac
      log "Installed to $HOME/.local/bin/codex (no sudo available)"
    fi
  fi

  rm -rf "$tmp"
}

is_node_wrapper() {
  # Heuristic: text file with a node shebang or "node" string near top
  local f="$1"
  [ -f "$f" ] || return 1
  # If it's an ELF binary, it's not the Node wrapper
  if head -c 4 "$f" 2>/dev/null | grep -q $'\x7fELF'; then
    return 1
  fi
  if head -n 1 "$f" 2>/dev/null | grep -qiE 'node|env node'; then
    return 0
  fi
  head -n 5 "$f" 2>/dev/null | grep -qi 'node' && return 0 || return 1
}

purge_path_wrappers() {
  # Remove/rename any earlier PATH entries named 'codex' that are Node wrappers
  local installed
  if [ -x /usr/local/bin/codex ]; then
    installed=/usr/local/bin/codex
  elif [ -x "$HOME/.local/bin/codex" ]; then
    installed="$HOME/.local/bin/codex"
  else
    installed=""
  fi
  # Also nuke any NVM-installed codex shims
  local nvm_dir
  nvm_dir=${NVM_DIR:-"$HOME/.nvm"}
  if [ -d "$nvm_dir/versions/node" ]; then
    find "$nvm_dir/versions/node" -type f -path '*/bin/codex' -print -exec rm -f {} + 2>/dev/null || true
  fi
  # If preferred is not a binary yet, still scan PATH
  IFS=: read -r -a parts <<<"${PATH:-}"
  for d in "${parts[@]}"; do
    [ -n "$d" ] || continue
    [ -x "$d/codex" ] || continue
    # Skip our newly installed binary to avoid self-nuking
    if [ -n "${installed:-}" ] && [ "$d/codex" = "$installed" ]; then
      continue
    fi
    if is_node_wrapper "$d/codex"; then
      log "Disabling Node wrapper at $d/codex"
      mv -f "$d/codex" "$d/codex.node-wrapper.bak" 2>/dev/null || rm -f "$d/codex" || true
    fi
  done
}

verify() {
  if ! command -v codex >/dev/null 2>&1; then
    die "codex binary not found in PATH after install"
  fi
  # Clear shell command cache and ensure resolution points to our binary
  hash -r 2>/dev/null || true
  log "codex binary: $(command -v codex)"
  codex --version || true
}

main() {
  uninstall_npm_wrapper
  install_binary
  purge_path_wrappers
  verify
  cat <<'EON'

Next steps:
- Run `codex` and choose "Sign in with ChatGPT".
- Open the printed http://localhost:1455/... URL in your host browser.
- If running in a container, ensure port 1455 is forwarded (your start script maps -p 1455:1455).

Tip: You can persist auth by mounting your host ~/.codex to /home/jflana/.codex.
EON
}

main "$@"
