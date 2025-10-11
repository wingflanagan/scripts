FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    EDITOR=nvim

# Base packages and build deps (for node-gyp, cert trust, tmux truecolor, shell QoL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git gnupg unzip jq \
    ripgrep fzf fd-find tig tmux \
    python3 python3-pip python3-venv pipx \
    make g++ build-essential \
    openjdk-17-jre-headless lsb-release locales tzdata \
    libnss3-tools openssl sudo net-tools ncurses-term zoxide \
    && ln -s /usr/bin/fdfind /usr/local/bin/fd \
    && sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

# Neovim (stable) from neovim-releases tarball, arch-aware, no FUSE needed  [leave intact]
RUN set -eux; \
    arch="$(uname -m)"; \
    case "$arch" in \
    x86_64)  TAR="nvim-linux-x86_64.tar.gz" ;; \
    aarch64) TAR="nvim-linux-arm64.tar.gz" ;; \
    *) echo "Unsupported arch: $arch"; exit 1 ;; \
    esac; \
    url="https://github.com/neovim/neovim-releases/releases/latest/download/${TAR}"; \
    curl -fL "$url" -o /tmp/nvim.tar.gz; \
    tar -xzf /tmp/nvim.tar.gz -C /tmp; \
    nvimdir="$(tar -tf /tmp/nvim.tar.gz | head -1 | cut -d/ -f1)"; \
    install -Dm755 "/tmp/${nvimdir}/bin/nvim" /usr/local/bin/nvim; \
    mkdir -p /usr/local/share; \
    cp -r "/tmp/${nvimdir}/share/nvim" /usr/local/share/nvim; \
    rm -rf /tmp/nvim.tar.gz "/tmp/${nvimdir}"; \
    nvim --version | head -1

# MongoDB CLIs: mongosh + database-tools (client-only, no server)
RUN install -d -m 0755 /etc/apt/keyrings \
    && curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg --dearmor -o /etc/apt/keyrings/mongodb-server-7.0.gpg \
    && echo "deb [ signed-by=/etc/apt/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" \
    > /etc/apt/sources.list.d/mongodb-org-7.0.list \
    && apt-get update && apt-get install -y --no-install-recommends \
    mongodb-mongosh mongodb-database-tools \
    && rm -rf /var/lib/apt/lists/*

# AWS CLI v2
RUN curl -Ls "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip

USER root
RUN printf '\nalias ll="ls -lhAF --color=auto"\n' >> /etc/profile.d/aliases.sh

# Non-root user with passwordless sudo (you will need it sooner than you think)
ARG USER=dev UID=1000 GID=1000
RUN groupadd -g ${GID} ${USER} && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} \
    && usermod -aG sudo ${USER} \
    && echo "${USER} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/90-${USER}

USER ${USER}
WORKDIR /home/${USER}
RUN printf '\nalias ll="ls -lhAF --color=auto"\n' >> ~/.bashrc

# LazyVim starter (unchanged)
RUN git clone https://github.com/LazyVim/starter ~/.config/nvim && rm -rf ~/.config/nvim/.git

# ---- Your LazyVim config files (exact content) ----
RUN mkdir -p ~/.config/nvim/lua/config ~/.config/nvim/lua/plugins

# keymaps.lua
RUN cat > ~/.config/nvim/lua/config/keymaps.lua <<'EOF'
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

-- Better window nav if you’re not using the built-ins
map("n", "<C-h>", "<C-w>h", opts)
map("n", "<C-j>", "<C-w>j", opts)
map("n", "<C-k>", "<C-w>k", opts)
map("n", "<C-l>", "<C-w>l", opts)

map("n", "j", "gj", { silent = true })
map("n", "k", "gk", { silent = true })
EOF

# options.lua
RUN cat > ~/.config/nvim/lua/config/options.lua <<'EOF'
--- ~/.config/nvim/lua/config/options.lua
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

# telescope.lua
RUN cat > ~/.config/nvim/lua/plugins/telescope.lua <<'EOF'
-- ~/.config/nvim/lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  config = function(_, opts)
    local telescope = require("telescope")
    local builtin = require("telescope.builtin")

    telescope.setup(opts) -- keep LazyVim defaults

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

# Optional AI plugins (only load if keys present)
RUN cat > ~/.config/nvim/lua/plugins/windsurf.lua <<'EOF'
return {
  "Exafunction/windsurf.nvim",
  cond = function()
    return vim.env.WINDSURF_API_KEY ~= nil or vim.env.CODEIUM_API_KEY ~= nil
  end,
  config = function() end,
}
EOF

RUN cat > ~/.config/nvim/lua/plugins/codex.lua <<'EOF'
return {
  "johnseth97/codex.nvim",
  cond = function()
    return vim.env.OPENAI_API_KEY ~= nil
  end,
  config = function()
    require("codex").setup({})
  end,
}
EOF

# NVM + Node 22 (SPFx 1.21 is happy), plus yarn/pnpm
ENV NVM_DIR=/home/${USER}/.nvm
RUN curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install 22 \
    && nvm alias default 22 \
    && npm -g install npm@latest yarn pnpm

# Auto-load NVM in interactive shells
RUN printf '\nexport NVM_DIR="$HOME/.nvm"\n[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"\n' >> ~/.bashrc

# AWS CDK (npm) + AWS SAM (pipx)
RUN . "$NVM_DIR/nvm.sh" \
    && npm -g install aws-cdk \
    && pipx install aws-sam-cli

# lazygit (x86_64) + ensure user-local bin on PATH
RUN mkdir -p /home/${USER}/.local/bin \
    && LZ_VER=$(curl -s https://api.github.com/repos/jesseduffield/lazygit/releases/latest | grep -Po '"tag_name":\s*"\K[^"]+') \
    && curl -fsSL -o /tmp/lazygit.tar.gz \
    "https://github.com/jesseduffield/lazygit/releases/download/${LZ_VER}/lazygit_${LZ_VER#v}_Linux_x86_64.tar.gz" \
    && tar -xzf /tmp/lazygit.tar.gz -C /tmp lazygit \
    && install /tmp/lazygit /home/${USER}/.local/bin/lazygit \
    && rm -rf /tmp/lazygit* \
    && printf '\n# PATH for user-local bin\nexport PATH="$HOME/.local/bin:$PATH"\n' >> ~/.bashrc

# tmux config (add truecolor + sane defaults; keep your binds)
RUN printf '%s\n' \
    'set -g mouse on' \
    'set -g history-limit 50000' \
    'setw -g mode-keys vi' \
    'bind | split-window -h' \
    'bind - split-window -v' \
    'bind r source-file ~/.tmux.conf \; display "tmux reloaded"' \
    '' \
    '# 24-bit color path end-to-end' \
    'set -g default-terminal "tmux-256color"' \
    'set -as terminal-overrides ",*:Tc"' \
    'set -g focus-events on' \
    > /home/${USER}/.tmux.conf

# SPFx + Yeoman
RUN . "$NVM_DIR/nvm.sh" \
    && npm -g install yo gulp-cli @microsoft/generator-sharepoint @pnp/cli-microsoft365

# Shell QoL: fzf keybindings, giant fuzzy-searchable history, zoxide, truecolor env
RUN printf '%s\n' \
  '' \
  '# --- fzf key bindings (Debian paths differ; try both) ---' \
  'if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then' \
  '  . /usr/share/doc/fzf/examples/key-bindings.bash' \
  'elif [ -f /usr/share/fzf/key-bindings.bash ]; then' \
  '  . /usr/share/fzf/key-bindings.bash' \
  'fi' \
  '' \
  '# FZF defaults and huge persistent history' \
  'export FZF_DEFAULT_OPTS="--height 40% --reverse --border"' \
  'export HISTSIZE=200000' \
  'export HISTFILESIZE=200000' \
  'export HISTCONTROL=ignoredups:erasedups' \
  'shopt -s histappend' \
  '' \
  '# zoxide: smarter cd (use `z foo`, or `zi` for interactive)' \
  'eval "$(zoxide init bash)"' \
  '' \
  '# advertise truecolor; outside tmux we want xterm-256color' \
  'export COLORTERM=truecolor' \
  'export TERM=xterm-256color' \
  >> ~/.bashrc

# Git: make Neovim the default difftool/mergetool
RUN git config --global diff.tool nvimdiff \
    && git config --global difftool.prompt false \
    && git config --global difftool.nvimdiff.cmd 'nvim -d "$LOCAL" "$REMOTE"' \
    && git config --global difftool.nvimdiff.trustExitCode true \
    && git config --global merge.tool nvimdiff3 \
    && git config --global mergetool.prompt false \
    && git config --global mergetool.keepBackup false \
    && git config --global mergetool.nvimdiff3.cmd 'nvim -d "$LOCAL" "$BASE" "$REMOTE" "$MERGED" -c "wincmd J"' \
    && git config --global mergetool.nvimdiff3.trustExitCode false

# Make pipx shims available in all shells, interactive or not
ENV PATH="/home/dev/.local/bin:${PATH}" \
    AWS_PAGER="" \
    AWS_REGION=us-west-2

CMD ["/bin/bash"]
