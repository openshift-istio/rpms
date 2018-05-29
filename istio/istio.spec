# Generate devel rpm
%global with_devel 0
# Build with debug info rpm
%global with_debug 0
# Run unit tests
%global with_tests 0
# Build test binaries
%global with_test_binaries 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global git_commit d91d44ead27d9b4018ab5997ef7ec0f0a4621d9d
%global git_shortcommit  %(c=%{git_commit}; echo ${c:0:7})

%global provider        github
%global provider_tld    com
%global project         openshift-istio
%global repo            istio
# https://github.com/openshift-istio/istio
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     istio.io/istio

# Use /usr/local as base dir, once upstream heavily depends on that
%global _prefix /usr/local

Name:           istio
Version:        0.8.0
Release:        0.12.0.git.0.%{git_shortcommit}%{?dist}
Summary:        An open platform to connect, manage, and secure microservices
License:        ASL 2.0
URL:            https://%{provider_prefix}

Source0:        https://%{provider_prefix}/archive/%{git_commit}/%{repo}-%{git_commit}.tar.gz
Source1:        istiorc
Source2:        buildinfo

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  golang >= 1.9

%description
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

########### pilot-discovery ###############
%package pilot-discovery
Summary:  The istio pilot discovery
Requires: istio = %{version}-%{release}

%description pilot-discovery
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the pilot-discovery program.

pilot-discovery is the main pilot component and belongs to Control Plane.

########### pilot-agent ###############
%package pilot-agent
Summary:  The istio pilot agent
Requires: istio = %{version}-%{release}

%description pilot-agent
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the pilot-agent program.

pilot-agent is agent that talks to Istio pilot. It belongs to Data Plane.
Along with Envoy, makes up the proxy that goes in the sidecar along with applications.

########### istioctl ###############
%package istioctl
Summary:  The istio command line tool
Requires: istio = %{version}-%{release}

%description istioctl
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the istioctl program.

istioctl is the configuration command line utility.

########### sidecar-injector ###############
%package sidecar-injector
Summary:  The istio sidecar injector
Requires: istio = %{version}-%{release}

%description sidecar-injector
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the sidecar-injector program.

sidecar-injector is the Kubernetes injector for Istio sidecar.
It belongs to Control Plane.

########### mixs ###############
%package mixs
Summary:  The istio mixs
Requires: istio = %{version}-%{release}

%description mixs
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the mixs program.

mixs is the main mixer (server) component. Belongs to Control Plane.

########### mixc ###############
%package mixc
Summary:  The istio mixc
Requires: istio = %{version}-%{release}

%description mixc
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the mixc program.

mixc is a debug/development CLI tool to interact with Mixer API.

########### citadel ###############
%package citadel
Summary:  Istio Security Component
Requires: istio = %{version}-%{release}

%description citadel
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the istio_ca program.

This is the Istio Certificate Authority (CA) + security components.

%if 0%{?with_test_binaries}

########### tests ###############
%package pilot-tests
Summary:  Istio Pilot Test Binaries
Requires: istio = %{version}-%{release}

%description pilot-tests
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains the binaries needed for pilot tests.

%endif

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

Provides:      golang(%{import_path}/broker/cmd/brkcol/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/cmd/brks/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/cmd/shared) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/controller) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/model/config) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/model/osb) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/platform/kube/crd) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/server) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/testing/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/testing/mock/proto) = %{version}-%{release}
Provides:      golang(%{import_path}/broker/pkg/testing/util) = %{version}-%{release}
Provides:      golang(%{import_path}/galley/pkg) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/circonus) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/circonus/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/denier) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/denier/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/fluentd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/fluentd/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/kubernetesenv) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/kubernetesenv/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/kubernetesenv/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/list) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/list/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/memquota) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/memquota/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/noop) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/opa) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/opa/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/prometheus) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/prometheus/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/servicecontrol) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/servicecontrol/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/servicecontrol/template/servicecontrolreport) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stackdriver) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stackdriver/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stackdriver/helper) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stackdriver/log) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stackdriver/metric) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/statsd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/statsd/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stdio) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/adapter/stdio/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/cmd/mixc/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/cmd/mixcol/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/cmd/mixs/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/cmd/shared) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/example/servicegraph) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/example/servicegraph/dot) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/example/servicegraph/promgen) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/adapter) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/adapter/test) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/api) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/attribute) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/config/crd) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/config/proto) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/config/store) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/expr) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/compiled) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/compiler) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/evaluator) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/interpreter) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/runtime) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/testing) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/il/text) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/mockapi) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/perf) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/pool) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/runtime) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/runtime2/config) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/runtime2/handler) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/runtime2/testing/data) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/runtime2/testing/util) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/server) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/status) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/pkg/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/apikey) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/authorization) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/checknothing) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/listentry) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/logentry) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/metric) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/quota) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/reportnothing) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/sample) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/sample/apa) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/sample/check) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/sample/quota) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/sample/report) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/template/tracespan) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/test/client/env) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/test/spyAdapter) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/test/spyAdapter/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/test/spyAdapter/template/apa) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/test/spyAdapter/template/report) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/adapterlinter/testdata/bad) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/adapterlinter/testdata/good) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/bootstrapgen) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/bootstrapgen/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/interfacegen) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/interfacegen/template) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/inventory) = %{version}-%{release}
Provides:      golang(%{import_path}/mixer/tools/codegen/pkg/modelgen) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/cmd/istioctl/gendeployment) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/bootstrap) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/config/aggregate) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/config/kube/crd) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/config/kube/crd/file) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/config/kube/ingress) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/config/memory) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/dataplane) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/kube/admit) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/kube/admit/testcerts) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/kube/inject) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/model) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/model/test) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/proxy) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/proxy/envoy) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/proxy/envoy/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry/aggregate) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry/cloudfoundry) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry/consul) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry/eureka) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/pkg/serviceregistry/kube) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/test/grpcecho) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/test/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/pilot/test/util) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/cache) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/log) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/tracing) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides:      golang(%{import_path}/security/cmd/node_agent/na) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/caclient/grpc) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/caclient/grpc/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/credential) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/pki) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/pki/ca) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/pki/ca/controller) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/pki/testutil) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/platform) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/platform/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/registry) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/registry/kube) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/server/grpc) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/util) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/util/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/security/pkg/workload) = %{version}-%{release}
Provides:      golang(%{import_path}/security/proto) = %{version}-%{release}
Provides:      golang(%{import_path}/security/tests/integration) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/e2e/framework) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/component/fortio_server) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/component/mixer) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/component/proxy) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/example/environment/appOnlyEnv) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/example/environment/mixerEnvoyEnv) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/integration/framework) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/k8s) = %{version}-%{release}
Provides:      golang(%{import_path}/tests/util) = %{version}-%{release}

%description devel
Istio is an open platform that provides a uniform way to connect, manage
and secure microservices. Istio supports managing traffic flows between
microservices, enforcing access policies, and aggregating telemetry data,
all without requiring changes to the microservice code.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%prep

rm -rf ISTIO
mkdir -p ISTIO/src/istio.io/istio
tar zxf %{SOURCE0} -C ISTIO/src/istio.io/istio --strip=1

cp %{SOURCE1} ISTIO/src/istio.io/istio/.istiorc.mk
cp %{SOURCE2} ISTIO/src/istio.io/istio/buildinfo

%build
cd ISTIO
export GOPATH=$(pwd):%{gopath}

pushd src/istio.io/istio
make pilot-discovery pilot-agent istioctl sidecar-injector mixc mixs citadel

%if 0%{?with_test_binaries}
make test-bins
%endif

popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}

cp -pav ISTIO/out/linux_amd64/release/{pilot-discovery,pilot-agent,istioctl,sidecar-injector,mixs,mixc,istio_ca} $RPM_BUILD_ROOT%{_bindir}/

%if 0%{?with_test_binaries}
cp -pav ISTIO/out/linux_amd64/release/{pilot-test-server,pilot-test-client,pilot-test-eurekamirror} $RPM_BUILD_ROOT%{_bindir}/
%endif

%if 0%{?with_tests}

%check
cd ISTIO
export GOPATH=$(pwd):%{gopath}
pushd src/istio.io/istio
make localTestEnv test
make localTestEnvCleanup
popd

%endif

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license ISTIO/src/istio.io/istio/LICENSE
%doc     ISTIO/src/istio.io/istio/README.md

%files pilot-discovery
%{_bindir}/pilot-discovery

%files pilot-agent
%{_bindir}/pilot-agent

%files istioctl
%{_bindir}/istioctl

%files sidecar-injector
%{_bindir}/sidecar-injector

%files mixs
%{_bindir}/mixs

%files mixc
%{_bindir}/mixc

%files citadel
%{_bindir}/istio_ca

%if 0%{?with_test_binaries}
%files pilot-tests
%{_bindir}/pilot-test-server
%{_bindir}/pilot-test-client
%{_bindir}/pilot-test-eurekamirror
%endif

%if 0%{?with_devel}
%files devel -f devel.file-list
%license ISTIO/src/istio.io/istio/LICENSE
%doc ISTIO/src/istio.io/istio/README.md ISTIO/src/istio.io/istio/DEV-*.md ISTIO/src/istio.io/istio/CONTRIBUTING.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%changelog
* Wed Apr 18 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.8.0-0
- Vendor is not a submodule anymore

* Tue Apr 17 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.8.0-0rc1
- Update to 0.8rc1

* Thu Apr 5 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.7.1-2
- Optionally run unit tests

* Sat Mar 31 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.7.1-1
- New version

* Tue Mar 13 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.6.0-4
- Fix the docker hub and version (tag)

* Mon Mar 12 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.6.0-3
- Use /usr/local as base dir, once upstream heavily depends on that

* Tue Mar 6 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.6.0-2
- Update buildinfo file. Now it will be updated by update.sh

* Tue Feb 27 2018 Jonh Wendell <jonh.wendell@redhat.com> - 0.6.0-1
- First package
