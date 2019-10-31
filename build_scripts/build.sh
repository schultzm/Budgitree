#!/bin/bash
sync.sh
sudo singularity build --force -T ecoh_typing.simg Singularity && singularity test ecoh_typing.simg
