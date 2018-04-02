# Generate devel rpm
%global with_devel 0
# Build with debug info rpm
%global with_debug 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# https://github.com/istio/proxy
%global provider        github
%global provider_tld    com
%global project         istio
%global repo            proxy
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}

Name:           istio-proxy
Version:        0.7.1
Release:        3%{?dist}
Summary:        The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.
License:        ASL 2.0
URL:            https://%{provider_prefix}

#Common
BuildRequires:  bazel
BuildRequires:  devtoolset-4-gcc
BuildRequires:  devtoolset-4-gcc-c++
BuildRequires:  devtoolset-4-libatomic-devel
BuildRequires:  devtoolset-4-libstdc++-devel
BuildRequires:  devtoolset-4-runtime
BuildRequires:  libtool
BuildRequires:  golang
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  m4
BuildRequires:  perl

%if 0%{?centos} >= 7
BuildRequires:  cmake3
%else
BuildRequires:  llvm-toolset-7-cmake
BuildRequires:  llvm-toolset-7-runtime
BuildRequires:  llvm-toolset-7-cmake-data
%endif

Source0:        proxy-full.tar.xz
Source1:        build.sh

%description
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

########### istio-proxy ###############
%package istio-proxy
Summary:  The istio envoy proxy

%description istio-proxy
The Istio Proxy is a microservice proxy that can be used on the client and server side, and forms a microservice mesh. The Proxy supports a large number of features.

This package contains the envoy program.

istio-proxy is the proxy required by the Istio Pilot Agent that talks to Istio pilot

%prep
%setup -q -n %{name}

%build

%if 0%{?centos} >= 7
  export CENTOS=true
%endif

cd ..
%{SOURCE1}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}/usr/local/bin

cp -pav ${RPM_BUILD_DIR}/envoy ${RPM_BUILD_ROOT}/usr/local/bin

%files
/usr/local/bin/envoy

%changelog
* Mon Mar 5 2018 Bill DeCoste <wdecoste@redhat.com>
- First package 
