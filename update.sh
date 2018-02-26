#!/bin/bash

NEW_SOURCES=""
PKG_COMMAND=${PKG:-rhpkg}

function usage() {
    echo "$0 <SHA of istio> <SHA of vendor>"
    echo
    exit 0
}

function update_commit() {
    local prefix="$1"
    local prefix_spec=${prefix/-/_}
    local sha="$2"

    local tarball="https://github.com/openshift-istio/${prefix}istio/archive/${sha}/${prefix}istio-${sha}.tar.gz"
    local filename="${prefix}istio-${sha}.tar.gz"

    echo -n "Checking ${prefix}istio...   "
    if [ ! -f "${filename}" ]; then
        echo "Downloading ${tarball}"
        curl -Lfs ${tarball} -o "${filename}"
        if [ $? -ne 0 ]; then
            echo "Error downloading tarball, exiting."
            exit 1
        fi
    else
        echo "Already on disk, download not necessary"
    fi

    sed -i "s/%global ${prefix_spec}git_commit .*/%global ${prefix_spec}git_commit ${sha}/" istio.spec
    NEW_SOURCES="${NEW_SOURCES} ${filename}"
}

function new_sources() {
    echo
    echo "Executing ${PKG_COMMAND} new-sources ${NEW_SOURCES}"
    ${PKG_COMMAND} new-sources ${NEW_SOURCES}

    if [ $? -eq 0 ]; then
        git add istio.spec
    fi
}

function update_snapshot_info() {
    local date="$(date +'%Y%m%d')"
    sed -i "s/%global build_date .*/%global build_date ${date}/" istio.spec
}

[ $# -eq 2 ] || usage

update_commit "" "$1"
update_commit "vendor-" "$2"
update_snapshot_info
new_sources
