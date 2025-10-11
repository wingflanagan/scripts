#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[!] Error on line $LINENO: $BASH_COMMAND" >&2' ERR

# -------- Settings you may tweak ----------
TZONE=${TZONE:-Etc/UTC}
MONGO_MAJOR=${MONGO_MAJOR:-7.0}
AWS_REGION=${AWS_REGION:-us-west-2}
# -----------------------------------------

export DEBIAN_FRONTEND=noninteractive

echo "[*] Updating base system and installing core packages..."
apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates curl git gnupg unzip jq \
  ripgrep fzf fd-find tig \
  python3 python3-pip python3-venv pipx \
  make g++ build-essential \
  default-jre-headless lsb-release locales tzdata \
  libnss3-tools openssl sudo net-tools ncurses-term zoxide \
  vim htop \
  openssh-server ufw \
  open-vm-tools qemu-guest-agent

ln -sf /usr/bin/fdfind /usr/local/bin/fd || true

# ----- Neovim 0.11.x (official tarball) -----
echo "[*] Installing Neovim (>=0.11.x) ..."
NV_ARCH=$(uname -m)
case "$NV_ARCH" in
  x86_64)  NV_TARBALL="nvim-linux-x86_64.tar.gz" ;;
  aarch64|arm64) NV_TARBALL="nvim-linux-arm64.tar.gz" ;;
  *) echo "Unsupported arch for Neovim: $NV_ARCH" >&2; exit 1 ;;
esac

# Allow override via NEOVIM_TAG env (e.g., v0.11.4); default to latest stable
NEOVIM_TAG=${NEOVIM_TAG:-stable}
TMPD="$(mktemp -d)"
curl -fsSL -o "$TMPD/$NV_TARBALL" "https://github.com/neovim/neovim/releases/download/${NEOVIM_TAG}/${NV_TARBALL}"

# Extract directly into /usr/local so runtime files live at /usr/local/share/nvim
# This avoids missing runtime (syntax.vim) and Lua modules (vim.uri) errors
tar -xzf "$TMPD/$NV_TARBALL" -C /usr/local --strip-components=1
rm -rf "$TMPD"
echo "[*] Neovim installed: $(/usr/local/bin/nvim --version | head -1)"

# Ensure jflana exists and is passwordless sudo
if ! id "jflana" &>/dev/null; then
  useradd -m -s /bin/bash jflana
fi
usermod -aG sudo jflana
echo "jflana ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/90-jflana
chmod 440 /etc/sudoers.d/90-jflana

echo "[*] Timezone -> ${TZONE}"
timedatectl set-timezone "$TZONE" || true

echo "[*] Locales..."
sed -i 's/^[# ]*en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
locale-gen
update-locale LANG=en_US.UTF-8

# Basic defaults in login shells
echo 'export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8' >/etc/profile.d/00-locale.sh
echo 'export EDITOR=nvim' >/etc/profile.d/editor.sh
chmod 644 /etc/profile.d/{00-locale.sh,editor.sh}

echo '[*] Aliases...'
printf '\nalias ll="ls -lhAF --color=auto"\n' >> /etc/profile.d/aliases.sh
chmod 644 /etc/profile.d/aliases.sh

echo "[*] SSH hardening..."
sshd_cfg=/etc/ssh/sshd_config
grep -q '^PasswordAuthentication' "$sshd_cfg" && \
  sed -ri 's/^#?\s*PasswordAuthentication\s+.*/PasswordAuthentication no/' "$sshd_cfg" || \
  echo 'PasswordAuthentication no' >> "$sshd_cfg"
grep -q '^PermitRootLogin' "$sshd_cfg" && \
  sed -ri 's/^#?\s*PermitRootLogin\s+.*/PermitRootLogin no/' "$sshd_cfg" || \
  echo 'PermitRootLogin no' >> "$sshd_cfg"
systemctl enable --now ssh

##############################
# SSH authorized_keys install
##############################
# Paste your RSA public key between the single quotes below.
# Example: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... your-email'
SSH_PUBKEY='ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCdMgnHPqZXUGtGbQBwYKX0PRVfTyYSpog4f/SWg3mO/wPWe9undSIAX4Prm2vtuh7I35k0fUr9QLq7B9OB5pEM6f92UYyNOLofPWT0mHTf0cYa4Mb0a+eoUL8d22MCQWcNBExf1joyIWljyAXLkFFt2pmyp7JlFRwHwezLKi9VI5svrkxjn36xbnCdfJ9pzzBTuGKErnWtpQimeHbrL4iajThAPUv5ykJXcg8D/HXLaEJuqRv6OvPrKML8TTldXN9xrLx+9vyBti6LDQu7QAQKZii7mcM7qqLr5bN5ewFP+gvxnwPcF8FNfH5VLfGrWMArHeqOpCS3LXk2m1qN9hTjY/vyCErjwgu19uu+hRXC+OCxPspnpPobhnKlVNPQoIUBpDgYAIFMZYUvWr/fMq8+VK2X+js8PyRFGISqVdcNPq3ZO53q68Iy9PpO/bHuKiQb32LZlZHa13TRseEnglJ5cInwOrdx+kJB2GGtPKC2lYJGICjyg8pi+oDGRVQl/sE= jflana@UW-MEDICINE'

add_key() {
  local user="$1"
  local home_dir
  home_dir="$(getent passwd "$user" | cut -d: -f6)"
  [ -n "$home_dir" ] || { echo "[!] No home dir for $user"; return 1; }
  local ssh_dir="${home_dir}/.ssh"
  local auth_keys="${ssh_dir}/authorized_keys"

  install -d -m 700 -o "$user" -g "$user" "$ssh_dir"
  touch "$auth_keys"
  chown "$user":"$user" "$auth_keys"
  chmod 600 "$auth_keys"

  if ! grep -qxF "$SSH_PUBKEY" "$auth_keys"; then
    echo "$SSH_PUBKEY" >> "$auth_keys"
    chown "$user":"$user" "$auth_keys"
    echo "[*] Installed SSH key for $user"
  else
    echo "[*] SSH key already present for $user"
  fi
}

if [[ "$SSH_PUBKEY" == *"<put key here>"* || -z "$SSH_PUBKEY" ]]; then
  echo "[!] SSH_PUBKEY not set; skipping key installation."
else
  add_key root
  add_key jflana
fi
##############################

# ----- AWS CLI v2 (system-wide) -----
echo "[*] Installing AWS CLI v2..."
tmp=$(mktemp -d)
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m | sed 's/aarch64/aarch64/;s/x86_64/x86_64/').zip" -o "$tmp/awscliv2.zip"
unzip -q "$tmp/awscliv2.zip" -d "$tmp"
"$tmp/aws/install" --update
rm -rf "$tmp"

# ----- lazygit (latest) -----
echo "[*] Installing lazygit..."
LG_ARCH=$(uname -m)
if [ "$LG_ARCH" = "x86_64" ]; then LG_SUFFIX="Linux_x86_64.tar.gz"; elif [ "$LG_ARCH" = "aarch64" ]; then LG_SUFFIX="Linux_arm64.tar.gz"; else echo "Unsupported arch for lazygit: $LG_ARCH"; exit 1; fi
LG_VER=$(curl -s https://api.github.com/repos/jesseduffield/lazygit/releases/latest | grep -Po '"tag_name":\s*"\K[^"]+')
curl -fsSL -o /tmp/lazygit.tgz "https://github.com/jesseduffield/lazygit/releases/download/${LG_VER}/lazygit_${LG_VER#v}_${LG_SUFFIX}"
tar -xzf /tmp/lazygit.tgz -C /tmp lazygit
install /tmp/lazygit /usr/local/bin/lazygit
rm -f /tmp/lazygit /tmp/lazygit.tgz

# ----- zellij (apt or fallback to static binary) -----
echo "[*] Installing zellij..."
if apt-get install -y --no-install-recommends zellij 2>/dev/null; then
  echo "[*] zellij installed from Debian repo."
else
  echo "[!] zellij not in Debian repo for this release; installing prebuilt binary."
  Z_ARCH="$(uname -m)"
  if [ "$Z_ARCH" = "x86_64" ]; then Z_FILE="zellij-x86_64-unknown-linux-musl.tar.gz"; elif [ "$Z_ARCH" = "aarch64" ]; then Z_FILE="zellij-aarch64-unknown-linux-musl.tar.gz"; else echo "Unsupported arch for zellij: $Z_ARCH"; exit 1; fi
  TMPD="$(mktemp -d)"
  curl -fsSL "https://github.com/zellij-org/zellij/releases/latest/download/${Z_FILE}" -o "$TMPD/zellij.tgz"
  tar -xzf "$TMPD/zellij.tgz" -C "$TMPD"
  install -m 0755 "$TMPD/zellij" /usr/local/bin/zellij
  rm -rf "$TMPD"
  echo "[*] zellij $(/usr/local/bin/zellij --version) installed to /usr/local/bin"
fi

# ----- MongoDB server (handles Debian 13 -> bookworm mapping) -----
echo "[*] Installing MongoDB ${MONGO_MAJOR} server..."
install -d -m 0755 /etc/apt/keyrings
curl -fsSL "https://pgp.mongodb.com/server-${MONGO_MAJOR}.asc" \
  | gpg --dearmor -o "/etc/apt/keyrings/mongodb-server-${MONGO_MAJOR}.gpg"

sys_codename=$(. /etc/os-release && echo "$VERSION_CODENAME")
mongo_codename="${sys_codename}"
if [ "$mongo_codename" = "trixie" ]; then
  echo "[*] Debian 13 detected; using bookworm repo for Mongo."
  mongo_codename="bookworm"
fi

cat > /etc/apt/sources.list.d/mongodb-org-${MONGO_MAJOR}.list <<EOF
deb [ signed-by=/etc/apt/keyrings/mongodb-server-${MONGO_MAJOR}.gpg ] https://repo.mongodb.org/apt/debian ${mongo_codename}/mongodb-org/${MONGO_MAJOR} main
EOF

apt-get update
apt-get install -y --no-install-recommends mongodb-org
systemctl enable --now mongod

# Bind local only by default; we'll tunnel from host
if grep -q '^\s*bindIp:' /etc/mongod.conf; then
  sed -ri 's/^\s*bindIp:\s*.*/  bindIp: 127.0.0.1/' /etc/mongod.conf
else
  if grep -q '^\s*net:\s*$' /etc/mongod.conf; then
    sed -i '/^\s*net:\s*$/a\  bindIp: 127.0.0.1' /etc/mongod.conf
  else
    printf '\nnet:\n  bindIp: 127.0.0.1\n' >> /etc/mongod.conf
  fi
fi
systemctl restart mongod

# ----- DynamoDB Local as a systemd service (runs as jflana) -----
echo "[*] Installing DynamoDB Local..."
install -d -o jflana -g jflana /opt/dynamodb/bin
install -d -o jflana -g jflana /opt/dynamodb/data
curl -fsSL https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o /opt/dynamodb/dynamodb_local_latest.tar.gz
tar -xzf /opt/dynamodb/dynamodb_local_latest.tar.gz -C /opt/dynamodb/bin
rm -f /opt/dynamodb/dynamodb_local_latest.tar.gz
cat >/etc/systemd/system/dynamodb-local.service <<'EOF'
[Unit]
Description=AWS DynamoDB Local
After=network.target

[Service]
Type=simple
User=jflana
Group=jflana
WorkingDirectory=/opt/dynamodb/bin
ExecStart=/usr/bin/java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar \
  -sharedDb -dbPath /opt/dynamodb/data -port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now dynamodb-local

# ----- pipx path for all shells -----
echo 'export PATH="$HOME/.local/bin:$PATH"' >/etc/profile.d/pipx.sh
chmod 644 /etc/profile.d/pipx.sh

# ----- Per-user shell QoL (root and jflana) -----
add_qol() {
  local user="$1"
  sudo -u "$user" -H bash -lc '
cat >> ~/.bashrc << "EOS"
alias ll="ls -lhAF --color=auto"

# fzf keybindings (Debian paths differ; try both)
if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then
  . /usr/share/doc/fzf/examples/key-bindings.bash
elif [ -f /usr/share/fzf/key-bindings.bash ]; then
  . /usr/share/fzf/key-bindings.bash
fi

# FZF defaults & huge persistent history
export FZF_DEFAULT_OPTS="--height 40% --reverse --border"
export HISTSIZE=200000
export HISTFILESIZE=200000
export HISTCONTROL=ignoredups:erasedups
shopt -s histappend

# zoxide
eval "$(zoxide init bash)"

# Truecolor & terminal niceties
export COLORTERM=truecolor
export TERM=xterm-256color

# pipx shims + user-local bin
export PATH="$HOME/.local/bin:$PATH"

# NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# Auto-attach zellij for interactive SSH sessions (will not break scp)
if [[ $- == *i* ]] && [ -n "$SSH_TTY" ] && [ -z "$ZELLIJ" ] && command -v zellij >/dev/null; then
  zellij attach -c
fi
EOS
'
}
add_qol root
add_qol jflana

# ----- SAM CLI and NVM/Node per-user (root and jflana) -----
setup_user_tooling() {
  local user="$1"

  # pipx + SAM
  sudo -u "$user" -H pipx ensurepath || true
  sudo -u "$user" -H pipx install aws-sam-cli || true

  # NVM + Node 22 + global npm goodies (per-user)
  sudo -u "$user" -H bash -lc '
    set -e
    export NVM_DIR="$HOME/.nvm"
    if [ ! -d "$NVM_DIR" ]; then
      curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    fi
    . "$NVM_DIR/nvm.sh"
    nvm install 22
    nvm alias default 22
    npm -g install npm@latest yarn pnpm yo gulp-cli @microsoft/generator-sharepoint @pnp/cli-microsoft365 aws-cdk @openai/codex
  '
}
setup_user_tooling root
setup_user_tooling jflana

# ----- LazyVim starter for jflana (fixed: no nested single quotes) -----
echo "[*] Installing LazyVim starter for jflana..."
sudo -u jflana -H bash -lc 'git clone https://github.com/LazyVim/starter ~/.config/nvim && rm -rf ~/.config/nvim/.git'
sudo -u jflana -H bash -lc 'mkdir -p ~/.config/nvim/lua/config ~/.config/nvim/lua/plugins'

# keymaps.lua
sudo -u jflana -H tee /home/jflana/.config/nvim/lua/config/keymaps.lua >/dev/null <<'EOF'
local map = vim.keymap.set
local opts = { silent = true }
map("n", "<Esc>", "<cmd>nohlsearch<CR>", opts)
map("v", "J", ":m ' >+1<CR>gv=gv", opts)
map("v", "K", ":m ' <-2<CR>gv=gv", opts)
map({ "n", "i", "v" }, "<C-s>", "<cmd>w<CR>", opts)
map("n", "<C-h>", "<C-w>h", opts)
map("n", "<C-j>", "<C-w>j", opts)
map("n", "<C-k>", "<C-w>k", opts)
map("n", "<C-l>", "<C-w>l", opts)
map("n", "j", "gj", { silent = true })
map("n", "k", "gk", { silent = true })
EOF
# NOTE: The two lines above intentionally use single quotes inside the string.
# If you prefer the exact original, replace the two lines with: 
# map("v", "J", ":m '>+1<CR>gv=gv", opts)
# map("v", "K", ":m '<-2<CR>gv=gv", opts)

# options.lua
sudo -u jflana -H tee /home/jflana/.config/nvim/lua/config/options.lua >/dev/null <<'EOF'
local opt = vim.opt
local g = vim.g
opt.number = true
opt.relativenumber = true
opt.cursorline = true
opt.signcolumn = "yes"
opt.scrolloff = 8
opt.sidescrolloff = 8
opt.termguicolors = true
opt.wrap = true
opt.linebreak = true
opt.breakindent = true
opt.colorcolumn = "100"
opt.splitright = true
opt.splitbelow = true
opt.expandtab = true
opt.tabstop = 2
opt.shiftwidth = 2
opt.softtabstop = 2
opt.smartindent = true
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true
opt.hlsearch = true
opt.updatetime = 200
opt.timeoutlen = 400
opt.undofile = true
opt.swapfile = false
opt.clipboard = "unnamedplus"
opt.conceallevel = 2
g.autoformat = true
g.mapleader = " "
g.maplocalleader = "\\"
EOF

# telescope.lua
sudo -u jflana -H tee /home/jflana/.config/nvim/lua/plugins/telescope.lua >/dev/null <<'EOF'
return {
  "nvim-telescope/telescope.nvim",
  config = function(_, opts)
    local telescope = require("telescope")
    local builtin = require("telescope.builtin")
    telescope.setup(opts)
    vim.keymap.set("n", "<leader>fo", function()
      builtin.find_files({ prompt_title = "Find Anything", cwd = vim.fn.expand("~"), hidden = true })
    end, { desc = "Find files anywhere (from ~)" })
    vim.keymap.set("n", "<leader>fc", function()
      builtin.find_files({ prompt_title = "Neovim Config", cwd = vim.fn.stdpath("config"), hidden = true })
    end, { desc = "Find Neovim config files" })
  end,
}
EOF

# windsurf.vim (Codeium) plugin
sudo -u jflana -H tee /home/jflana/.config/nvim/lua/plugins/windsurf.lua >/dev/null <<'EOF'
return {
  "Exafunction/windsurf.vim",
  event = "InsertEnter",
  init = function()
    vim.g.codeium_no_map_tab = 1
  end,
}
EOF

# codex.nvim plugin
sudo -u jflana -H tee /home/jflana/.config/nvim/lua/plugins/codex.lua >/dev/null <<'EOF'
return {
  "johnseth97/codex.nvim",
  lazy = true,
  cmd = { "Codex", "CodexToggle" },
  keys = {
    { "<leader>cc", function() require("codex").toggle() end, desc = "Toggle Codex popup" },
  },
  opts = {
    keymaps = {
      toggle = nil,  -- keep plugin from auto-mapping; we use <leader>cc above
      quit = "<C-q>",
    },
    border = "rounded",
    width = 0.8,
    height = 0.8,
    model = nil,
    autoinstall = true,
  },
}
EOF

# ----- UFW: block everything by default; open SSH -----
echo "[*] Configuring UFW firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw --force enable

# ----- Make AWS envs visible to all shells -----
echo "AWS_PAGER=" >> /etc/environment
echo "AWS_REGION=${AWS_REGION}" >> /etc/environment

# ----- Done -----
cat <<'EON'

Provisioning complete.

Sanity checks (as jflana):
  nvim --version | head -1
  bash -lc 'node -v && npm -v && yarn -v && pnpm -v'
  aws --version
  bash -lc 'sam --version'
  bash -lc 'cdk --version'
  bash -lc 'codex --version'
  mongosh --nodb --eval 'quit()'
  systemctl status mongod --no-pager
  systemctl status dynamodb-local --no-pager
  zellij --version

Notes:
- Root SSH login remains disabled (PermitRootLogin no). Keys are installed for both users anyway.
- Node via NVM is installed per-user for root and jflana with Node 22 set as default; switch with: nvm ls; nvm use <version>

EON
