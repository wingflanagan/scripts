#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") <guest-ip>"
  exit 1
fi

GUEST_IP=$1
SSH_CMD=${SSH_CMD:-ssh}
USER=${USER_OVERRIDE:-jflana}

declare -a TUNNELS=(
  "-L1455:localhost:1455"
  "-L27017:localhost:27017"
  "-L3000:localhost:3000"
  "-L8000:localhost:8000"
  "-L4321:localhost:4321"
  "-L35729:localhost:35729"
)

echo "Connecting to ${USER}@${GUEST_IP} with port forwards..."

"${SSH_CMD}" \
  -o StrictHostKeyChecking=accept-new \
  -o ExitOnForwardFailure=yes \
  "${TUNNELS[@]}" \
  "${USER}@${GUEST_IP}"
