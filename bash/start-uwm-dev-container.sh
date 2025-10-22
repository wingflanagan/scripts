#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-uwm-dev}"
NAME="${2:-uwm-dev}"
HOST_NET="${HOST_NET:-0}"
if [[ "${3:-}" == "--host-net" ]]; then HOST_NET=1; fi

HOST_HOME="${HOME}"
HOST_CODEX="${HOME}/.codex"
mkdir -p "${HOST_CODEX}"

VOL_HOME="${HOST_HOME}:/mnt/home:rw"
VOL_CODEX="${HOST_CODEX}:/home/jflana/.codex:rw"

if podman ps -a --format '{{.Names}}' | grep -qx "${NAME}"; then
  echo "Starting existing container '${NAME}' ..."
  exec podman start -ai "${NAME}"
fi

echo "Creating and starting container '${NAME}' from image '${IMAGE}' ..."
if [[ "${HOST_NET}" == "1" ]]; then
  exec podman run -it \
    --name "${NAME}" \
    --network host \
    -v "${VOL_HOME}" \
    -v "${VOL_CODEX}" \
    "${IMAGE}" bash
else
  exec podman run -it \
    --name "${NAME}" \
    -p 1455:1455 \
    -v "${VOL_HOME}" \
    -v "${VOL_CODEX}" \
    "${IMAGE}" bash
fi
