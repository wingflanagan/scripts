#!/usr/bin/env bash
set -euo pipefail

VMRUN=${VMRUN:-vmrun}
VMX=${VMX:-"/home/jflana/uwmc-dev_vm/uwmc-dev.vmx"}

"$VMRUN" -T ws start "$VMX" nogui

ip=$("$VMRUN" -T ws getGuestIPAddress "$VMX" -wait | tr -d '\r')

if [[ -z "${ip}" ]]; then
  echo "Failed to retrieve guest IP address." >&2
  exit 1
fi

echo "Guest IP: ${ip}"
