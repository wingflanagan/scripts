FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    EDITOR=nvim \
    container=podman

# Base packages and build deps (aligning with setup.sh; no GUI, no systemd services)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git gnupg unzip jq \
    ripgrep fzf fd-find tig \
    python3 python3-pip python3-venv pipx \
    make g++ build-essential \
    openjdk-21-jdk-headless lsb-release locales tzdata \
    libnss3-tools openssl sudo net-tools ncurses-term zoxide \
    vim btop mc less \
    systemd systemd-sysv dbus procps \
    openssh-client \
  && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
  && sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
  && locale-gen \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone \
  && rm -rf /var/lib/apt/lists/*

# Proper stop signal for systemd in containers
STOPSIGNAL SIGRTMIN+3

# Basic defaults in login shells
RUN echo 'export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8' >/etc/profile.d/00-locale.sh \
 && echo 'export EDITOR=nvim' >/etc/profile.d/editor.sh \
 && printf '\nalias ll="ls -lhAF --color=auto"\n' >> /etc/profile.d/aliases.sh \
 && chmod 644 /etc/profile.d/00-locale.sh /etc/profile.d/editor.sh /etc/profile.d/aliases.sh

# Neovim (>=0.11 recommended). You can override with --build-arg NEOVIM_TAG=v0.11.x
ARG NEOVIM_TAG=stable
RUN set -eux; \
    arch="$(uname -m)"; \
    case "$arch" in \
      x86_64)  TAR="nvim-linux-x86_64.tar.gz" ;; \
      aarch64|arm64) TAR="nvim-linux-arm64.tar.gz" ;; \
      *) echo "Unsupported arch: $arch"; exit 1 ;; \
    esac; \
    url="https://github.com/neovim/neovim/releases/download/${NEOVIM_TAG}/${TAR}"; \
    tmpd="$(mktemp -d)"; \
    curl -fL "$url" -o "$tmpd/nvim.tar.gz"; \
    tar -xzf "$tmpd/nvim.tar.gz" -C /usr/local --strip-components=1; \
    rm -rf "$tmpd"; \
    /usr/local/bin/nvim --version | head -1

# Create user 'jflana' with passwordless sudo (matches setup.sh)
ARG USER=jflana UID=1000 GID=1000
RUN groupadd -g ${GID} ${USER} \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} \
 && usermod -aG sudo ${USER} \
 && echo "${USER} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/90-${USER} \
 && chmod 440 /etc/sudoers.d/90-${USER}

USER ${USER}
WORKDIR /home/${USER}

# System-scoped Neovim config to avoid being overridden by host-mounted $HOME
USER root
RUN install -d -m 0755 /opt/nvim /opt/nvim-data /opt/nvim/uwm \
 && install -d -m 0755 /opt/nvim/uwm/lua/config /opt/nvim/uwm/lua/plugins \
 && chown -R $(id -u jflana):$(id -g jflana) /opt/nvim /opt/nvim-data
ENV XDG_CONFIG_HOME=/opt/nvim XDG_DATA_HOME=/opt/nvim-data NVIM_APPNAME=uwm
USER ${USER}

# Shell QoL: fzf bindings, history, zoxide, truecolor, pipx shims
RUN printf '%s\n' \
  '' \
  'alias ll="ls -lhAF --color=auto"' \
  '' \
  '# fzf keybindings (Debian paths differ; try both)' \
  'if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then' \
  '  . /usr/share/doc/fzf/examples/key-bindings.bash' \
  'elif [ -f /usr/share/fzf/key-bindings.bash ]; then' \
  '  . /usr/share/fzf/key-bindings.bash' \
  'fi' \
  '' \
  '# FZF defaults & huge persistent history' \
  'export FZF_DEFAULT_OPTS="--height 40% --reverse --border"' \
  'export HISTSIZE=200000' \
  'export HISTFILESIZE=200000' \
  'export HISTCONTROL=ignoredups:erasedups' \
  'shopt -s histappend' \
  '' \
  '# zoxide' \
  'eval "$(zoxide init bash)"' \
  '' \
  '# Truecolor & terminal niceties' \
  'export COLORTERM=truecolor' \
  'export TERM=xterm-256color' \
  '' \
  '# pipx shims + user-local bin' \
  'export PATH="$HOME/.local/bin:$PATH"' \
  >> ~/.bashrc

# Readline: prefix search with up/down arrows and friendlier completion
RUN cat > ~/.inputrc <<'EOF'

# Makes up/down arrows search for commands starting with what you've typed
"\e[A": history-search-backward
"\e[B": history-search-forward

# This ensures your typed prefix stays visible as you scroll
set show-all-if-ambiguous on
set completion-ignore-case on
EOF

# LazyVim starter (installed to /opt/nvim/uwm)
USER root
RUN rm -rf /opt/nvim/uwm \
 && git clone https://github.com/LazyVim/starter /opt/nvim/uwm \
 && rm -rf /opt/nvim/uwm/.git \
 && mkdir -p /opt/nvim/uwm/lua/config /opt/nvim/uwm/lua/plugins \
 && chown -R $(id -u jflana):$(id -g jflana) /opt/nvim/uwm
USER ${USER}

# keymaps.lua
RUN cat > /opt/nvim/uwm/lua/config/keymaps.lua <<'EOF'
-- ~/.config/nvim/lua/config/keymaps.lua
local map = vim.keymap.set
local opts = { silent = true }

-- Clear search highlight
map("n", "<Esc>", "<cmd>nohlsearch<CR>", opts)

-- Move lines up/down (visual mode)
map("v", "J", ":m '>+1<CR>gv=gv", opts)
map("v", "K", ":m '<-2<CR>gv=gv", opts)

-- Save fast
map({ "n", "i", "v" }, "<C-s>", "<cmd>w<CR>", opts)

-- Better window nav if you're not using the built-ins
map("n", "<C-h>", "<C-w>h", opts)
map("n", "<C-j>", "<C-w>j", opts)
map("n", "<C-k>", "<C-w>k", opts)
map("n", "<C-l>", "<C-w>l", opts)

map("n", "j", "gj", { silent = true })
map("n", "k", "gk", { silent = true })

-- Resize window using <ctrl> arrow keys
map("n", "<C-Up>", "<cmd>resize +2<cr>", { desc = "Increase Window Height", silent = true })
map("n", "<C-Down>", "<cmd>resize -2<cr>", { desc = "Decrease Window Height", silent = true })
map("n", "<C-Left>", "<cmd>vertical resize -2<cr>", { desc = "Decrease Window Width", silent = true })
map("n", "<C-Right>", "<cmd>vertical resize +2<cr>", { desc = "Increase Window Width", silent = true })
EOF

# options.lua
RUN cat > /opt/nvim/uwm/lua/config/options.lua <<'EOF'
-- ~/.config/nvim/lua/config/options.lua
local opt = vim.opt
local g = vim.g

-- UI
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
opt.equalalways = false
opt.winminwidth = 1

-- Editing
opt.expandtab = true
opt.tabstop = 2
opt.shiftwidth = 2
opt.softtabstop = 2
opt.smartindent = true

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true
opt.hlsearch = true

-- Behavior
opt.updatetime = 200
opt.timeoutlen = 400
opt.undofile = true
opt.swapfile = false

-- Encoding/clipboard
opt.clipboard = "unnamedplus"

-- Conceal
opt.conceallevel = 2

-- LazyVim knobs
g.autoformat = true
g.mapleader = " "
g.maplocalleader = "\\"
EOF

# trouble.lua - open on the right, ~40% width, friendly symbols mapping
RUN cat > /opt/nvim/uwm/lua/plugins/trouble.lua <<'EOF'
-- ~/.config/nvim/lua/plugins/trouble.lua
return {
  {
    "folke/trouble.nvim",
    opts = function(_, opts)
      local size = math.floor(vim.o.columns * 0.4)
      opts = opts or {}
      opts.position = "right"
      -- Support both pre-v3 (width) and v3+ (size) styles
      opts.width = size
      opts.size = size
      return opts
    end,
    keys = {
      {
        "<leader>cs",
        function()
          local size = math.floor(vim.o.columns * 0.4)
          require("trouble").open({
            mode = "symbols",
            position = "right",
            size = size,
            width = size,
          })
        end,
        desc = "Symbols (Trouble 40% right)",
      },
    },
  },
}
EOF

# Resize all Trouble windows on open (right side ~40%)
RUN cat >> /opt/nvim/uwm/lua/config/autocmds.lua <<'EOF'

-- Ensure Trouble pane opens on the right with ~40% width
vim.api.nvim_create_autocmd("FileType", {
  pattern = { "trouble", "Trouble" },
  callback = function()
    -- Move to far right; wrap to appease LuaLS type-check
    pcall(function() vim.cmd("wincmd L") end)
    vim.opt_local.winfixwidth = false
    vim.cmd(("vertical resize %d"):format(math.floor(vim.o.columns * 0.4)))
  end,
})
EOF

# telescope.lua
RUN cat > /opt/nvim/uwm/lua/plugins/telescope.lua <<'EOF'
-- ~/.config/nvim/lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  config = function(_, opts)
    local telescope = require("telescope")
    local builtin = require("telescope.builtin")

    telescope.setup(opts)

    -- Find anything from home dir
    vim.keymap.set("n", "<leader>fo", function()
      builtin.find_files({
        prompt_title = "Find Anything",
        cwd = vim.fn.expand("~"),
        hidden = true,
      })
    end, { desc = "Find files anywhere (from ~)" })

    -- Find Neovim config files
    vim.keymap.set("n", "<leader>fc", function()
      builtin.find_files({
        prompt_title = "Neovim Config",
        cwd = vim.fn.stdpath("config"),
        hidden = true,
      })
    end, { desc = "Find Neovim config files" })
  end,
}
EOF

# Optional AI plugin stubs (load only if keys present)
RUN cat > /opt/nvim/uwm/lua/plugins/windsurf.lua <<'EOF'
return {
  "Exafunction/windsurf.nvim",
  cond = function()
    return vim.env.WINDSURF_API_KEY ~= nil or vim.env.CODEIUM_API_KEY ~= nil
  end,
  config = function() end,
}
EOF

RUN cat > /opt/nvim/uwm/lua/plugins/codex.lua <<'EOF'
return {
  "johnseth97/codex.nvim",
  -- Load on toggle command or keymap
  cmd = { "Codex", "CodexToggle" },
  keys = {
    {
      "<leader>cx",
      function() require("codex").toggle() end,
      desc = "Toggle Codex",
    },
  },
  opts = {
    autoinstall = false, -- CLI installed in Docker image
    keymaps = {
      toggle = nil, -- keep external mapping above
      quit = "<C-q>",
    },
    border = "rounded",
    width = 0.85,
    height = 0.85,
  },
}
EOF

# treesitter.lua - ensure common parsers and enable highlight/indent
RUN cat > /opt/nvim/uwm/lua/plugins/treesitter.lua <<'EOF'
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  opts = {
    ensure_installed = {
      "lua", "vim", "vimdoc", "bash", "regex",
      "json", "yaml", "toml", "dockerfile",
      "html", "css", "javascript", "typescript", "tsx",
      "markdown", "markdown_inline", "gitcommit", "gitignore",
      "query", "cmake"
    },
    highlight = { enable = true, additional_vim_regex_highlighting = false },
    indent = { enable = true },
    auto_install = true,
  },
}
EOF

# Harden Treesitter install location and compilers to avoid missing parsers
RUN cat > /opt/nvim/uwm/lua/plugins/treesitter-extra.lua <<'EOF'
return {
  {
    "nvim-treesitter/nvim-treesitter",
    init = function()
      -- Ensure Neovim can find parsers installed outside the default tree
      vim.g.parser_install_dir = "/opt/nvim-data/parsers"
      vim.opt.runtimepath:append(vim.g.parser_install_dir)
    end,
    opts = function(_, opts)
      opts = opts or {}
      -- Make sure key JS/TS parsers are present
      local ensure = opts.ensure_installed or {}
      local function ensure_lang(lang)
        if type(ensure) == "table" then
          for _, l in ipairs(ensure) do if l == lang then return end end
          table.insert(ensure, lang)
        end
      end
      ensure_lang("javascript")
      ensure_lang("typescript")
      ensure_lang("tsx")
      opts.ensure_installed = ensure

      -- Use gcc and prefer tarballs over git to be CI-friendly
      local install = require("nvim-treesitter.install")
      install.compilers = { "gcc", "cc", "g++" }
      install.prefer_git = false
      return opts
    end,
  },
}
EOF

# lsp.lua - opt-in servers and Lua defaults. Mason will install these.
RUN cat > /opt/nvim/uwm/lua/plugins/lsp.lua <<'EOF'
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      lua_ls = {
        settings = {
          Lua = {
            workspace = { checkThirdParty = false },
            telemetry = { enable = false },
          },
        },
      },
      bashls = {},
      tsserver = {},
      jsonls = {},
      yamlls = {},
      dockerls = {},
      html = {},
      cssls = {},
      marksman = {},
    },
  },
}
EOF

# mason.lua - ensure Mason is loadable by command (MasonInstall et al.)
RUN cat > /opt/nvim/uwm/lua/plugins/mason.lua <<'EOF'
return {
  "williamboman/mason.nvim",
  cmd = {
    "Mason", "MasonUpdate", "MasonInstall", "MasonUninstall",
    "MasonUninstallAll", "MasonLog"
  },
  opts = {},
}
EOF

# Preinstall Lazy plugins, Treesitter parsers (Node not required yet)
RUN nvim --headless "+Lazy! sync" +qa || true
RUN nvim --headless "+TSUpdateSync all" +qa || true
# Ensure critical parsers explicitly (fixes occasional misses in CI builds)
RUN nvim --headless "+TSInstallSync lua vim vimdoc bash regex json yaml toml dockerfile html css javascript typescript tsx markdown markdown_inline gitcommit gitignore query cmake" +qa || true

# Git configuration (align with setup.sh):
# - credential.helper store so first login persists plaintext creds locally
# - safe.directory '*', user name/email, and nvim difftool/mergetool
RUN git config --global credential.helper store \
 && git config --global --add safe.directory '*' \
 && git config --global user.name "John Flanagan" \
 && git config --global user.email jflana@uw.edu \
 && git config --global diff.tool nvimdiff \
 && git config --global difftool.prompt false \
 && git config --global difftool.nvimdiff.cmd 'nvim -d "$LOCAL" "$REMOTE"' \
 && git config --global difftool.nvimdiff.trustExitCode true \
 && git config --global merge.tool nvimdiff3 \
 && git config --global mergetool.prompt false \
 && git config --global mergetool.keepBackup false \
 && git config --global mergetool.nvimdiff3.cmd 'nvim -d "$LOCAL" "$BASE" "$REMOTE" "$MERGED" -c "wincmd J"' \
 && git config --global mergetool.nvimdiff3.trustExitCode false

# AWS CLI v2 (system-wide)
USER root
RUN set -eux; \
    ARCH=$(uname -m); \
    case "$ARCH" in \
      x86_64) AWS_PKG=awscli-exe-linux-x86_64.zip ;; \
      aarch64|arm64) AWS_PKG=awscli-exe-linux-aarch64.zip ;; \
      *) echo "Unsupported arch: $ARCH"; exit 1 ;; \
    esac; \
    curl -fsSL "https://awscli.amazonaws.com/${AWS_PKG}" -o /tmp/awscliv2.zip; \
    unzip -q /tmp/awscliv2.zip -d /tmp; \
    /tmp/aws/install --update; \
    rm -rf /tmp/aws /tmp/awscliv2.zip

# lazygit (latest)
RUN set -eux; \
    ARCH=$(uname -m); \
    case "$ARCH" in \
      x86_64) SUFFIX=Linux_x86_64.tar.gz ;; \
      aarch64|arm64) SUFFIX=Linux_arm64.tar.gz ;; \
      *) echo "Unsupported arch for lazygit: $ARCH"; exit 1 ;; \
    esac; \
    LZ_VER=$(curl -s https://api.github.com/repos/jesseduffield/lazygit/releases/latest | grep -Po '"tag_name":\s*"\K[^" ]+'); \
    curl -fsSL -o /tmp/lazygit.tgz "https://github.com/jesseduffield/lazygit/releases/download/${LZ_VER}/lazygit_${LZ_VER#v}_${SUFFIX}"; \
    tar -xzf /tmp/lazygit.tgz -C /tmp lazygit; \
    install /tmp/lazygit /usr/local/bin/lazygit; \
    rm -f /tmp/lazygit /tmp/lazygit.tgz

# zellij (prefer apt; fallback to static release if unavailable on trixie)
RUN if apt-get update && apt-get install -y --no-install-recommends zellij 2>/dev/null; then \
      echo "zellij installed from Debian repo"; \
    else \
      set -eux; \
      ARCH=$(uname -m); \
      case "$ARCH" in \
        x86_64) Z_FILE="zellij-x86_64-unknown-linux-musl.tar.gz" ;; \
        aarch64|arm64) Z_FILE="zellij-aarch64-unknown-linux-musl.tar.gz" ;; \
        *) echo "Unsupported arch for zellij: $ARCH"; exit 1 ;; \
      esac; \
      TMPD=$(mktemp -d); \
      curl -fsSL "https://github.com/zellij-org/zellij/releases/latest/download/${Z_FILE}" -o "$TMPD/zellij.tgz"; \
      tar -xzf "$TMPD/zellij.tgz" -C "$TMPD"; \
      install -m 0755 "$TMPD/zellij" /usr/local/bin/zellij; \
      rm -rf "$TMPD"; \
    fi

# MongoDB server 7.0 from official repo: map trixie->bookworm (no systemd)
ARG MONGO_MAJOR=7.0
RUN install -d -m 0755 /etc/apt/keyrings \
 && curl -fsSL "https://pgp.mongodb.com/server-${MONGO_MAJOR}.asc" | gpg --dearmor -o "/etc/apt/keyrings/mongodb-server-${MONGO_MAJOR}.gpg" \
 && . /etc/os-release \
 && MONGO_CODENAME="${VERSION_CODENAME}" \
 && if [ "$MONGO_CODENAME" = "trixie" ]; then MONGO_CODENAME="bookworm"; fi \
 && echo "deb [ signed-by=/etc/apt/keyrings/mongodb-server-${MONGO_MAJOR}.gpg ] https://repo.mongodb.org/apt/debian ${MONGO_CODENAME}/mongodb-org/${MONGO_MAJOR} main" \
    > /etc/apt/sources.list.d/mongodb-org-${MONGO_MAJOR}.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends mongodb-org \
 && rm -rf /var/lib/apt/lists/* \
 && ( \
      if grep -q '^\s*bindIp:' /etc/mongod.conf; then \
        sed -ri 's/^\s*bindIp:\s*.*/  bindIp: 127.0.0.1/' /etc/mongod.conf; \
      else \
        if grep -q '^\s*net:\s*$' /etc/mongod.conf; then \
          sed -i '/^\s*net:\s*$/a\  bindIp: 127.0.0.1' /etc/mongod.conf; \
        else \
          printf '\nnet:\n  bindIp: 127.0.0.1\n' >> /etc/mongod.conf; \
        fi; \
      fi \
    )

# DynamoDB Local (no systemd). Provide wrapper to launch it easily.
RUN install -d -o root -g root /opt/dynamodb/bin \
 && install -d -o root -g root /opt/dynamodb/data \
 && curl -fsSL https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz -o /opt/dynamodb/dynamodb_local_latest.tar.gz \
 && tar -xzf /opt/dynamodb/dynamodb_local_latest.tar.gz -C /opt/dynamodb/bin \
 && rm -f /opt/dynamodb/dynamodb_local_latest.tar.gz \
 && printf '%s\n' \
    '#!/usr/bin/env bash' \
    'set -euo pipefail' \
    'cd /opt/dynamodb/bin' \
    'exec /usr/bin/java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -dbPath /opt/dynamodb/data -port "${DDB_PORT:-8000}"' \
    > /usr/local/bin/dynamodb-local \
 && chmod +x /usr/local/bin/dynamodb-local

# Allow the non-root user to run DynamoDB Local with write access
RUN chown -R ${USER}:${USER} /opt/dynamodb

# systemd unit for DynamoDB Local (disabled by default; start with `systemctl start dynamodb-local`)
RUN printf '%s\n' \
  '[Unit]' \
  'Description=AWS DynamoDB Local' \
  'After=network.target' \
  '' \
  '[Service]' \
  'Type=simple' \
  'User=jflana' \
  'Group=jflana' \
  'WorkingDirectory=/opt/dynamodb/bin' \
  'ExecStart=/usr/bin/java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -dbPath /opt/dynamodb/data -port 8000' \
  'Restart=on-failure' \
  '' \
  '[Install]' \
  'WantedBy=multi-user.target' \
  > /etc/systemd/system/dynamodb-local.service

# TUI clients
# - vi-mongo (Go; Apache-2.0) https://github.com/kopecmaciej/vi-mongo
# - ddv (Rust; MIT) DynamoDB viewer https://github.com/lusingander/ddv
RUN set -eux; \
    ARCH=$(uname -m); \
    # vi-mongo prebuilt
    case "$ARCH" in \
      x86_64) VIMONGO_ASSET=vi-mongo_Linux_x86_64.tar.gz ;; \
      aarch64|arm64) VIMONGO_ASSET=vi-mongo_Linux_arm64.tar.gz ;; \
      *) echo "Unsupported arch for vi-mongo: $ARCH"; exit 1 ;; \
    esac; \
    VIMONGO_VER=$(curl -s https://api.github.com/repos/kopecmaciej/vi-mongo/releases/latest | grep -Po '"tag_name":\s*"\K[^" ]+'); \
    curl -fsSL -o /tmp/vi-mongo.tgz "https://github.com/kopecmaciej/vi-mongo/releases/download/${VIMONGO_VER}/${VIMONGO_ASSET}"; \
    tar -xzf /tmp/vi-mongo.tgz -C /tmp; \
    VIM_BIN=$(find /tmp -maxdepth 2 -type f -name 'vi-mongo' | head -n1); \
    install "$VIM_BIN" /usr/local/bin/vi-mongo; \
    rm -rf /tmp/vi-mongo*; \
    # ddv prebuilt
    case "$ARCH" in \
      x86_64) DDV_ASSET=ddv-0.2.0-x86_64-unknown-linux-gnu.tar.gz ;; \
      aarch64|arm64) DDV_ASSET=ddv-0.2.0-aarch64-unknown-linux-gnu.tar.gz ;; \
      *) echo "Unsupported arch for ddv: $ARCH"; exit 1 ;; \
    esac; \
    curl -fsSL -o /tmp/ddv.tgz "https://github.com/lusingander/ddv/releases/download/v0.2.0/${DDV_ASSET}"; \
    tar -xzf /tmp/ddv.tgz -C /tmp; \
    DDV_BIN=$(find /tmp -maxdepth 2 -type f -name 'ddv' | head -n1); \
    install "$DDV_BIN" /usr/local/bin/ddv; \
    rm -rf /tmp/ddv*

USER root
# Global fnm shell init for Bash (robust and POSIX-safe)
RUN cat > /etc/profile.d/fnm.sh <<'EOF'
# fnm (system-wide init)
if [ -d /opt/fnm ]; then
  PATH="/opt/fnm:$PATH"
fi
if command -v fnm >/dev/null 2>&1; then
  # Initialize fnm; --use-on-cd selects per-project versions when entering dirs
  eval "$(fnm env --use-on-cd)"
fi
EOF
RUN chmod 644 /etc/profile.d/fnm.sh \
 && grep -q "/etc/profile.d/fnm.sh" /etc/bash.bashrc || printf '\n# Source fnm init for interactive shells\n[ -f /etc/profile.d/fnm.sh ] && . /etc/profile.d/fnm.sh\n' >> /etc/bash.bashrc

# Convenience wrapper to start a user-owned mongod (no systemd)
RUN printf '%s\n' \
    '#!/usr/bin/env bash' \
    'set -euo pipefail' \
    'DBDIR="$HOME/.local/share/mongodb"' \
    'mkdir -p "$DBDIR"' \
    'exec mongod --dbpath "$DBDIR" --bind_ip 127.0.0.1 --port "${MONGO_PORT:-27017}"' \
    | tee /usr/local/bin/mongod-local >/dev/null \
 && chmod +x /usr/local/bin/mongod-local
USER ${USER}

# FNM installed system-wide under /opt/fnm + Node 22 for ${USER} (plus yarn/pnpm) and AWS CDK; SAM via pipx for the user
USER root
RUN curl -fsSL https://fnm.vercel.app/install | bash -s -- --install-dir /opt/fnm --skip-shell \
 && chown -R ${USER}:${USER} /opt/fnm

USER ${USER}
RUN bash -lc 'export PATH="/opt/fnm:$PATH" \
    && eval "$(fnm env)" \
    && fnm install 22 \
    && fnm default 22 \
    && corepack enable \
    && corepack prepare yarn@stable --activate \
    && corepack prepare pnpm@latest --activate \
    && npm -g install npm@latest aws-cdk yo gulp-cli @microsoft/generator-sharepoint @pnp/cli-microsoft365 \
    && nvim --headless "+Lazy! sync" "+MasonUpdate" "+MasonInstall lua-language-server bash-language-server typescript-language-server json-lsp yaml-language-server dockerfile-language-server html-lsp css-lsp marksman" +qa || true'

# Ensure pipx shims available; fnm init will be handled globally via /etc/profile.d
RUN python3 -m pipx ensurepath || true

# AWS SAM CLI via pipx for the user
RUN pipx install aws-sam-cli || true

# Make pipx shims available in all shells
ENV PATH="/opt/fnm:/home/${USER}/.local/bin:${PATH}" \
    AWS_PAGER="" \
    AWS_REGION=us-west-2

# Install Codex CLI from GitHub releases (avoid npm wrapper + node warnings)
USER root
RUN set -eux; \
    ARCH=$(uname -m); \
    case "$ARCH" in \
      x86_64)  COD_ARCH=x86_64-unknown-linux-musl ;; \
      aarch64|arm64) COD_ARCH=aarch64-unknown-linux-musl ;; \
      *) echo "Unsupported arch for Codex: $ARCH"; exit 1 ;; \
    esac; \
    VER=$(curl -fsSL https://api.github.com/repos/openai/codex/releases/latest | grep -Po '"tag_name"\s*:\s*"\K[^"]+'); \
    URL="https://github.com/openai/codex/releases/download/${VER}/codex-${COD_ARCH}.tar.gz"; \
    TMPD=$(mktemp -d); \
    curl -fsSL "$URL" -o "$TMPD/codex.tgz"; \
    tar -xzf "$TMPD/codex.tgz" -C "$TMPD"; \
    BIN=$(find "$TMPD" -maxdepth 1 -type f -name "codex-*" | head -n1); \
    install "$BIN" /usr/local/bin/codex; \
    rm -rf "$TMPD"; \
    codex --version || true
USER ${USER}

# Ensure the Rust Codex binary is preferred over any Node shims
USER root
RUN cat > /etc/profile.d/70-codex.sh <<'EOF'
# Prefer the official Rust Codex binary and neutralize Node wrapper shims
if [ -x /usr/local/bin/codex ]; then
  alias codex=/usr/local/bin/codex
  # Clear any cached command lookup
  hash -r 2>/dev/null || true
  # Remove any per-user NVM codex shims inside the container
  if [ -d "$HOME/.nvm/versions/node" ]; then
    find "$HOME/.nvm/versions/node" -type f -path '*/bin/codex' -exec rm -f {} + 2>/dev/null || true
  fi
fi
EOF
RUN chmod 644 /etc/profile.d/70-codex.sh
USER ${USER}

# Finalize Neovim plugin sync and Treesitter parsers (belt-and-suspenders)
RUN nvim --headless "+Lazy! sync" +qa || true
RUN nvim --headless "+TSUpdateSync all" +qa || true
RUN nvim --headless "+TSInstallSync javascript typescript tsx" +qa || true

# Expose a mount point for host home directory
VOLUME ["/mnt/home"]

# Notes for host bind-mounts (examples):
# - Windows:  podman run -it --name uwmc_dev -v "C:\\Users\\John Flanagan:/mnt/home:rw" <image> bash
# - macOS:    podman run -it --name uwmc_dev -v "$HOME:/mnt/home:rw" <image> bash
# - Linux:    podman run -it --name uwmc_dev -v "$HOME:/mnt/home:rw" <image> bash

CMD ["/sbin/init"]

CMD ["/bin/bash"]
