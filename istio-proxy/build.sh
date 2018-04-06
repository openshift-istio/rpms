set -x 

function set_default_envs() {
  if [ -z "${PROXY_GIT_BRANCH}" ]; then
    PROXY_GIT_BRANCH=0.7.1
  fi

  if [ -z "${FETCH_DIR}" ]; then
    FETCH_DIR=${RPM_BUILD_DIR}/istio-proxy
  fi

  if [ -z "${BUILD_CONFIG}" ]; then
    BUILD_CONFIG=release
  fi

  if [ -z "${TARBALL_SUFFIX}" ]; then
    TARBALL_SUFFIX=alpha
  fi
}

function set_path() {

  grep -Fxq "Red Hat Enterprise Linux Server" /etc/redhat-release
  RHEL="$?"
  if [ $RHEL ]; then
    source /opt/rh/llvm-toolset-7/enable
  else
    ln -s /usr/bin/cmake3 cmake
    export PATH=$(pwd):$PATH
  fi

  if [[ ${PATH} != *"devtoolset"* ]]; then
    source /opt/rh/devtoolset-4/enable
  fi
}

function copy_fetch() {

  if [ "$FETCH_DIR" == "${RPM_BUILD_DIR}/istio-proxy" ]; then
    pushd ${FETCH_DIR}/proxy
      SHA="$(git rev-parse --verify HEAD)"
    popd

    #bazel build expects istio-proxy-${PROXY_GIT_BRANCH} dir
    mkdir -p istio-proxy-${PROXY_GIT_BRANCH}
    mv ${FETCH_DIR} istio-proxy-${PROXY_GIT_BRANCH}

    #rpmbuild expects istio-proxy dir
    mkdir -p ${RPM_BUILD_DIR}/istio-proxy
  else
    pushd ${FETCH_DIR}/istio-proxy/proxy
      SHA="$(git rev-parse --verify HEAD)"
    popd

    rm -rf istio-proxy-${PROXY_GIT_BRANCH}
    cp -rfp ${FETCH_DIR} istio-proxy-${PROXY_GIT_BRANCH}
  fi
}

function run_build() {
  pushd istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy

    #replace fully qualified tool path from fetch
    sed -i "s|BUILD_PATH_MARKER/bazel|${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel|" ../bazel/base/external/local_config_cc/cc_wrapper.sh
    sed -i "s|BUILD_PATH_MARKER/bazel|${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel|" ../bazel/base/external/local_config_cc/CROSSTOOL

    RECIPES_DIR=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy bazel --output_base=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/root --batch build --config=${BUILD_CONFIG} "//..."

  popd
}

function create_artifacts() {
  if [ "${CREATE_ARTIFACTS}" == "true" ]; then
    pushd istio-proxy-${PROXY_GIT_BRANCH}
      mkdir -p usr/local/bin  
      cp istio-proxy/proxy/bazel-bin/src/envoy/envoy usr/local/bin/envoy
      cp istio-proxy/proxy/bazel-bin/src/envoy/envoy envoy
      tar -cvf envoy-${TARBALL_SUFFIX}-${SHA}.tar usr
      gzip envoy-${TARBALL_SUFFIX}-${SHA}.tar
      scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $HOME/.ssh/id_rsa envoy-${TARBALL_SUFFIX}-${SHA}.tar.gz geriatrix.boston.devel.redhat.com:/usr/share/nginx/html/istio-build/proxy/
    popd
  fi
}

function copy_binary() {
  if [ "${FETCH_DIR}" == "${RPM_BUILD_DIR}/istio-proxy" ]; then
    cp istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy/bazel-bin/src/envoy/envoy ${RPM_BUILD_DIR}
  fi
}

set_default_envs
set_path
copy_fetch
run_build
create_artifacts
copy_binary


