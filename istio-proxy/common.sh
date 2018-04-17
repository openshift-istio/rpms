set -x 
set -e

if [ -z "${BAZEL_VERSION}" ]; then
  BAZEL_VERSION=0.12.0
fi

function check_dependencies() {
  RESULT=$(bazel version)
  rm -rf ~/.cache/bazel

  if [[ $RESULT != *"${BAZEL_VERSION}"* ]]; then
    echo "Error: Istio Proxy requires Bazel ${BAZEL_VERSION}"
    exit -1
  fi
}

function set_path() {
  RHEL=$(grep -Fc "Red Hat Enterprise Linux Server" /etc/redhat-release || true)
  if [ "$RHEL" == "1" ]; then
    if [[ ${PATH} != *"llvm"* ]]; then
      source /opt/rh/llvm-toolset-7/enable
    fi
  else
    if [ ! -f "cmake" ]; then
      ln -s /usr/bin/cmake3 cmake
    fi

    if [[ ${PATH} != *"$(pwd)"* ]]; then
      export PATH=$(pwd):$PATH
    fi
  fi

  if [[ ${PATH} != *"devtoolset"* ]]; then
    source /opt/rh/devtoolset-4/enable
  fi
}

