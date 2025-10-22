#!/usr/bin/env bash
set -euo pipefail

VMRUN=${VMRUN:-vmrun}
VMX=${VMX:-"/home/john/uwmc-dev_vm/uwmc-dev.vmx"}

"$VMRUN" -T ws stop "$VMX" soft
