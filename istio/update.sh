#!/bin/bash

NEW_SOURCES=""

function usage() {
    echo "Usage: $0 [-i <SHA of istio>]"
    echo
    exit 0
}

while getopts ":i:v:" opt; do
  case ${opt} in
    i) ISTIO_SHA="${OPTARG}";;
    *) usage;;
  esac
done

[[ -z "${ISTIO_SHA}" ]] && ISTIO_SHA="$(grep '%global git_commit ' istio.spec | cut -d' ' -f3)"

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
    echo "Updating sources file with ${NEW_SOURCES}"
    md5sum ${NEW_SOURCES} > sources
}

function update_buildinfo() {
    local sha="$1"
    sed -i "s|istio.io/istio/pkg/version.buildGitRevision=.*|istio.io/istio/pkg/version.buildGitRevision=${sha}|" buildinfo
}

update_commit "" "${ISTIO_SHA}"
update_buildinfo "${ISTIO_SHA}"
new_sources
