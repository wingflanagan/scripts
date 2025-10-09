FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    EDITOR=nvim

# Base packages and build deps (for node-gyp, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git gnupg unzip jq \
    ripgrep fzf fd-find tig tmux \
    python3 python3-pip python3-venv pipx \
    make g++ build-essential \
    openjdk-17-jre-headless lsb-release locales tzdata \
    && ln -s /usr/bin/fdfind /usr/local/bin/fd \
    && sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

# Neovim (stable) from neovim-releases tarball, arch-aware, no FUSE needed
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
    # move into /usr/local (bin+share) so it wins on PATH
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

# Non-root user
ARG USER=dev UID=1000 GID=1000
RUN groupadd -g ${GID} ${USER} && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER}
USER ${USER}
WORKDIR /home/${USER}
RUN printf '\nalias ll="ls -lhAF --color=auto"\n' >> ~/.bashrc

# LazyVim starter
RUN git clone https://github.com/LazyVim/starter ~/.config/nvim && rm -rf ~/.config/nvim/.git

# NVM + Node 22
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

# tmux config
RUN printf '%s\n' \
    'set -g mouse on' \
    'set -g history-limit 50000' \
    'setw -g mode-keys vi' \
    'bind | split-window -h' \
    'bind - split-window -v' \
    'bind r source-file ~/.tmux.conf \; display "tmux reloaded"' \
    > /home/${USER}/.tmux.conf

# SPFx + Yeoman
RUN . "$NVM_DIR/nvm.sh" \
    && npm -g install yo gulp-cli @microsoft/generator-sharepoint @pnp/cli-microsoft365

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
