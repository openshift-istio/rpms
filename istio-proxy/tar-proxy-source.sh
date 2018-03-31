set -x

mkdir /tmp/istio-proxy
pushd /tmp/istio-proxy

#clone proxy
if [ ! -d "proxy" ]; then
  PROXY_VERSION=0.6.0
  git clone https://github.com/istio/proxy -b ${PROXY_VERSION}
fi

#clone dependency source and custom recipes
if [ ! -d "recipes" ]; then
  git clone https://github.com/bdecoste/proxy-rpm
  mv proxy-rpm/proxy/* .
  rm -rf proxy-rpm
fi

#bazel fetch
if [ ! -d "bazelorig" ]; then 
  if [[ ${PATH} != *"devtoolset"* ]]; then
    source /opt/rh/devtoolset-4/enable
  fi

  if [[ ${PATH} != *"llvm-toolset"* ]]; then
    source /opt/rh/llvm-toolset-7/enable
  fi

  pushd /tmp/istio-proxy/proxy
  bazel --output_base=/tmp/istio-proxy/bazel/base --output_user_root=/tmp/istio-proxy/bazel/root --batch fetch //...
#  bazel --output_base=/tmp/proxy/bazel/base --output_user_root=/tmp/proxy/bazel/root --batch fetch "//src/envoy -//external:android/crosstool -//external:android/sdk -//external:android/dx_jar_import -//external:android_sdk_for_testing -//external:android_ndk_for_testing -//external:has_androidsdk -//external:java_toolchain -//external:databinding_annotation_processor -//external:local_jdk -//external:jre-default -//external:jre -//external:jni_md_header-linux -//external:jni_md_header-freebsd -//external:jni_md_header-darwin -//external:jni_header -//external:jinja2 -//external:jdk-default -//external:jdk -//external:javac -//external:java_toolchain -//external:java -//external:jar -//external:go_sdk -//tools/deb:all -//:deb_version -//:darwin -//src/envoy:envoy_tar"
#bazel --output_base=/tmp/istio-proxy/bazel/base --output_user_root=/tmp/istio-proxy/bazel/root --batch fetch --experimental_external_repositories --experimental_repository_cache=/tmp/istio-proxy/bazel/X //...
  popd
  cp -rfp bazel bazelorig
fi

INSTALL_HASH=$(ls bazel/root/install)

# replace links with copies (links are fully qualified paths so don't travel)
#cp -rfL /tmp/bazel proxy
rm -rf bazel
cp -rfp bazelorig bazel

pushd /tmp/istio-proxy/bazel
find . -lname '/*' -exec ksh -c '
  for link; do
    target=$(readlink "$link")
    link=${link#./}
    root=${link//+([!\/])/..}; root=${root#/}; root=${root%..}
    rm "$link"
    target="$root${target#/}"
    target=$(echo $target | sed "s|../../../tmp/istio-proxy/bazel/base|../../../base|")
    target=$(echo $target | sed "s|../../tmp/istio-proxy/bazel/base|../../base|")
    target=$(echo $target | sed "s|../../../tmp/istio-proxy/bazel/root|../../../root|")
    target=$(echo $target | sed "s|../tmp/istio-proxy/bazel/root|../root|")
    target=$(echo $target | sed "s|../../../usr/lib/jvm|/usr/lib/jvm|")
    ln -s "$target" "$link"
  done
' _ {} +
popd

#prune native 
#rm bazel/root/install/${INSTALL_HASH}/_embedded_binaries/embedded_tools/src/main/native/BUILD

#prune git
find . -name ".git*" | xargs rm -rf

#prune logs
find . -name "*.log" | xargs rm -rf

#prune gzip
#find . -name "*.gz" | xargs rm -rf

#clean
rm -rf proxy/bazel-*

#prune go sdk
#GO_HOME=/usr/lib/golang
#rm -rf bazel/base/external/go_sdk/{api,bin,lib,pkg,wrc,test,misc,doc,blog}
#ln -s ${GO_HOME}/api bazel/base/external/go_sdk/api
#ln -s ${GO_HOME}/bin bazel/base/external/go_sdk/bin
#ln -s ${GO_HOME}/lib bazel/base/external/go_sdk/lib
#ln -s ${GO_HOME}/pkg bazel/base/external/go_sdk/pkg
#ln -s ${GO_HOME}/src bazel/base/external/go_sdk/src
#ln -s ${GO_HOME}/test bazel/base/external/go_sdk/test

#prune boringssl tests
#rm -rf boringssl/crypto/cipher_extra/test

#prune grpc tests
rm -rf bazel/base/external/com_github_grpc_grpc/test

#prune build_tools
#cp -rf BUILD.bazel bazel/base/external/io_bazel_rules_go/go/toolchain/BUILD.bazel

#prune unecessary files
pushd /tmp/istio-proxy/bazel
##find . -name "*.html" | xargs rm -rf
##find . -name "*.zip" | xargs rm -rf
#find . -name "example" | xargs rm -rf
#find . -name "examples" | xargs rm -rf
#find . -name "sample" | xargs rm -rf
#find . -name "samples" | xargs rm -rf
##find . -name "android" | xargs rm -rf
##find . -name "osx" | xargs rm -rf
#find . -name "*.a" | xargs rm -rf
##find . -name "*.so" | xargs rm -rf
#rm -rf bazel/base/external/go_sdk/src/archive/
popd

# remove fetch-build
#ENVOY_HASH=fbe7fd77b8354b9a6f47b8e24c1a5f25
rm -rf bazel/base/external/envoy_deps_cache_*

# use custom dependency recipes
cp -rf recipes/*.sh bazel/base/external/envoy/ci/build_container/build_recipes

popd

# create tarball
pushd /tmp
rm -rf proxy-full.tar.xz
tar cf proxy-full.tar istio-proxy --exclude=istio-proxy/bazelorig --exclude=istio-proxy/bazel/X --atime-preserve
xz proxy-full.tar
popd




