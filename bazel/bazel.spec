# they warn against doing this ... :-\
%define _disable_source_fetch 0
# make sure that internet access is enabled during the build

Name:           bazel
Version:        0.15.2
Release:        1%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/bazel/releases/download/%{version}/bazel-%{version}-dist.zip

ExclusiveArch:  x86_64

BuildRequires:  unzip 
BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  python
BuildRequires:  gcc-c++
Requires:       java-1.8.0-openjdk-devel

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%define debug_package %{nil}
%define __os_install_post %{nil}

%description
Correct, reproducible, and fast builds for everyone.

%prep
%setup -q -c -n %{name}-%{version}-dist

%build

which g++
g++ --version

CC=gcc
CXX=g++
./compile.sh
./output/bazel build --experimental_distdir=./derived/distdir //scripts:bazel-complete.bash
./output/bazel shutdown

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{bashcompdir}
cp output/bazel %{buildroot}/%{_bindir}
cp ./bazel-bin/scripts/bazel-complete.bash %{buildroot}/%{bashcompdir}/bazel

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{bashcompdir}/bazel


%changelog
* Wed Aug 1  2018 Dmitri Dolguikh <ddolguik@redhat.com> 0.15.2-1
- Release 0.15.2-1
* Wed Mar 14 2018 William DeCoste <wdecoste@redhat.com> 0.11.1-1
- Initial from vbatts copr

