#!/usr/bin/env bash
###############################################################################
#
# This is a simple grep search.
# - con: we need to know the indicators ahead of time
# - pro: typically one or two indicators are all we need
#
# Output can be cleaned up a bit.
#
###############################################################################

DRUPAL_PATH=$1

echo "[*] Searching ${DRUPAL_PATH}"

find ${DRUPAL_PATH} -type f -exec grep -H 'items\[' {} \; | awk '{print $2 }'

