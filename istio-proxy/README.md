# SPEC file and Utilities for creation of Istio Proxy RPM

### Online Fetch
First fetch all of the source and dependencies via the fetch script. For example, FETCH_DIR=/tmp CREATE_TARBALL=true ./fetch.sh. This will:

* Clone the Istio Proxy source
* Clone the dependency source and custom recipes
* Fetch the dependencies required by Bazel to complete an offline build
* Prune the fetched cache
* Create a compressed tarball at /tmp/proxy-full/tar.xz

### Offline Build
First extract the tarball from the fetch stage to a build directory (e.g. /home/root/workspaces/istio-proxy-build) and then execute the build script. For example, RPM_BUILD_DIR=/home/root/workspaces/isto-proxy-build RPM_SOURCE_DIR=/home/root/workspaces/rpms/isto-proxy ./build.sh

### Offline Test
Execute the test script. For example, RPM_BUILD_DIR=/home/root/workspaces/isto-proxy-build RPM_SOURCE_DIR=/home/root/workspaces/rpms/isto-proxy ./test.sh 


