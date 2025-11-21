#!/bin/bash

IMG="audio"

podman build . -t $IMG
podman run -it -v "$(realpath .):/app/src" $IMG "$@"