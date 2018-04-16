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

set_default_envs
set_path
run_tests


