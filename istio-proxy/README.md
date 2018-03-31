# SPEC file and Utilities for creation of Istio Proxy RPM

### Generating proxy-full.tar.xz 
The source file specified in istio-proxy.spec is currently too large to be stored in github (~200M). To generate proxy-full.tar.xz execute the tar-proxy-source.sh script. This will:

* Clone the Istio Proxy source
* Clone the dependency source and custom recipes
* Fetch the dependencies required by Bazel to complete an offline build
* Prune the fetched cache
* Create a compressed tarball at /tmp/proxy-full/tar.xz


