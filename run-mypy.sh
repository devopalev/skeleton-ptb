#!/usr/bin/env bash
#
# Copyright (c) 2024, «Domclick» LLC.
# All Rights Reserved. (domclick.ru)
#

set -o errexit

# Change directory to the project root directory.
cd "$(dirname "$0")"

mypy ./apps
