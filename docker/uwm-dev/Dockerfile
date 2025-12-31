FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/Los_Angeles \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    EDITOR=fresh \
    container=podman

# Base packages and build deps (aligning with setup.sh; no GUI, no systemd services)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git gnupg unzip jq \
    ripgrep fzf fd-find tig \
    python3 python3-pip python3-venv pipx \
    make g++ build-essential \
    openjdk-21-jdk-headless lsb-release locales tzdata \
    libnss3-tools openssl sudo net-tools ncurses-term zoxide \
    btop mc less \
    systemd systemd-sysv dbus procps \
    openssh-client \
  && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
  && sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
  && locale-gen \
  && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
  && echo $TZ > /etc/timezone \
  && rm -rf /var/lib/apt/lists/*

# Twin (local .deb)
COPY ntwin_0.9.1-neo.2-7_amd64.deb /tmp/ntwin_0.9.1-neo.2-7_amd64.deb
RUN set -eux; \
    dpkg -i /tmp/ntwin_0.9.1-neo.2-7_amd64.deb || true; \
    apt-get update; \
    apt-get install -y --no-install-recommends -f; \
    rm -rf /var/lib/apt/lists/*; \
    rm -f /tmp/ntwin_0.9.1-neo.2-7_amd64.deb

# Proper stop signal for systemd in containers
STOPSIGNAL SIGRTMIN+3

# Basic defaults in login shells
RUN echo 'export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8' >/etc/profile.d/00-locale.sh \
 && echo 'export EDITOR=fresh' >/etc/profile.d/editor.sh \
 && printf '\nalias ll="ls -lhAF --color=auto"\n' >> /etc/profile.d/aliases.sh \
 && chmod 644 /etc/profile.d/00-locale.sh /etc/profile.d/editor.sh /etc/profile.d/aliases.sh

# Create user 'jflana' with passwordless sudo (matches setup.sh)
ARG USER=jflana UID=1000 GID=1000
RUN groupadd -g ${GID} ${USER} \
 && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER} \
 && usermod -aG sudo ${USER} \
 && echo "${USER} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/90-${USER} \
 && chmod 440 /etc/sudoers.d/90-${USER}

USER ${USER}
WORKDIR /home/${USER}

# Shell QoL: fzf bindings, history, zoxide, truecolor, pipx shims
RUN printf '%s\n' \
  '' \
  'alias ll="ls -lhAF --color=auto"' \
  'alias desktop="twin -hw=tty"' \
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

# Git configuration (align with setup.sh):
# - credential.helper store so first login persists plaintext creds locally
# - safe.directory '*', user name/email
RUN git config --global credential.helper store \
 && git config --global --add safe.directory '*' \
 && git config --global user.name "John Flanagan" \
 && git config --global user.email jflana@uw.edu

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

# FNM installed system-wide under /opt/fnm + Node 22 for ${USER} (plus yarn/pnpm) and global npm CLIs; SAM via pipx for the user
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
    && npm -g install npm@latest aws-cdk yo gulp-cli @microsoft/generator-sharepoint @pnp/cli-microsoft365 @fresh-editor/fresh-editor @openai/codex'

# Ensure pipx shims available; fnm init will be handled globally via /etc/profile.d
RUN python3 -m pipx ensurepath || true

# AWS SAM CLI via pipx for the user
RUN pipx install aws-sam-cli || true

# Make pipx shims available in all shells
ENV PATH="/opt/fnm:/home/${USER}/.local/bin:${PATH}" \
    AWS_PAGER="" \
    AWS_REGION=us-west-2


# Expose a mount point for host home directory
VOLUME ["/mnt/home"]

# Notes for host bind-mounts (examples):
# - Windows:  podman run -it --name uwmc_dev -v "C:\\Users\\John Flanagan:/mnt/home:rw" <image> bash
# - macOS:    podman run -it --name uwmc_dev -v "$HOME:/mnt/home:rw" <image> bash
# - Linux:    podman run -it --name uwmc_dev -v "$HOME:/mnt/home:rw" <image> bash

CMD ["/sbin/init"]

CMD ["/bin/bash"]

