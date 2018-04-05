set -x 
set -e

function set_default_envs() {
  if [ -z "${PROXY_GIT_BRANCH}" ]; then
    PROXY_GIT_BRANCH=0.7.1
  fi

  if [ -z "${FETCH_DIR}" ]; then
    FETCH_DIR=${RPM_BUILD_DIR}/istio-proxy
  fi
}

function set_path() {

  if [ "${CENTOS}" == "true" ]; then 
    ln -s /usr/bin/cmake3 cmake
    export PATH=$(pwd):$PATH
  elif [[ ${PATH} != *"llvm-toolset"* ]]; then
    source /opt/rh/llvm-toolset-7/enable
  fi

  if [[ ${PATH} != *"devtoolset"* ]]; then
    source /opt/rh/devtoolset-4/enable
  fi
}

function copy_fetch() {
  if [ "$FETCH_DIR" == "${RPM_BUILD_DIR}/istio-proxy" ]; then
    #bazel build expects istio-proxy-${PROXY_GIT_BRANCH} dir
    mkdir -p istio-proxy-${PROXY_GIT_BRANCH}
    mv ${FETCH_DIR} istio-proxy-${PROXY_GIT_BRANCH}

    #rpmbuild expects istio-proxy dir
    mkdir -p ${RPM_BUILD_DIR}/istio-proxy
  else
    rm -rf istio-proxy-${PROXY_GIT_BRANCH}
    cp -rfp ${FETCH_DIR} istio-proxy-${PROXY_GIT_BRANCH}
  fi
}

function run_build() {
  pushd istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy

    #replace fully qualified tool path from fetch
    sed -i "s|BUILD_PATH_MARKER/bazel|${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel|" ../bazel/base/external/local_config_cc/cc_wrapper.sh
    sed -i "s|BUILD_PATH_MARKER/bazel|${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel|" ../bazel/base/external/local_config_cc/CROSSTOOL

    RECIPES_DIR=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy bazel --output_base=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/root --batch build --config=release "//..."

  popd
}

function create_artifacts() {
  if [ "${CREATE_ARTIFACTS}" == "true" ]; then
    mkdir -p istio-proxy-${PROXY_GIT_BRANCH}/usr/local/bin  
    cp istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy/bazel-bin/src/envoy/envoy istio-proxy-${PROXY_GIT_BRANCH}/usr/local/bin
    cp istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy/bazel-bin/src/envoy/envoy istio-proxy-${PROXY_GIT_BRANCH}
    pushd istio-proxy-${PROXY_GIT_BRANCH}
      tar -cv --xform 's|usr|/usr|' -f proxy.tar usr
      xz proxy.tar
    popd
  fi
}

function run_tests() {
  if [ "${RUN_TESTS}" == "true" ]; then
    pushd istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/proxy
      if [ "${RUN_TESTS}" == "true" ]; then
        if [ "${FORCE_TEST_FAILURE}" == "true" ]; then
          sed -i 's|ASSERT_TRUE|ASSERT_FALSE|g' src/istio/mixerclient/check_cache_test.cc
          sed -i 's|EXPECT_TRUE|EXPECT_FALSE|g' src/istio/mixerclient/check_cache_test.cc
          sed -i 's|EXPECT_OK|EXPECT_FALSE|g' src/istio/mixerclient/check_cache_test.cc
          sed -i 's|TEST_F|TEST|g' src/istio/mixerclient/check_cache_test.cc
        fi

        bazel --output_base=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/base --output_user_root=${RPM_BUILD_DIR}/istio-proxy-${PROXY_GIT_BRANCH}/istio-proxy/bazel/root --batch test "//..."
      fi
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
run_tests
copy_binary


