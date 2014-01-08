%global VERSION_SUFFIX -SNAPSHOT
%global JAVA_VERSION 1.7

%global PYTHON_THRIFT_STRUCTS JobConfiguration Lock ScheduledTask Quota


Name:           aurora
Version:        0.4.0
Release:        1%{?dist}
Summary:        A framework for scheduling long-running services against Apache Mesos

License:        ASL 2.0
URL:            http://%{name}.incubator.apache.org/
Source0:        https://github.com/apache/incubator-%{name}/archive/%{version}/incubator-%{name}-%{version}.tar.gz
Source1:        %{name}-scheduler-%{version}%{VERSION_SUFFIX}.pom

# Java-wise build dependencies:
BuildRequires:  java-devel 
BuildRequires:  jpackage-utils
# gradle is dead.beef
#BuildRequires:  gradle

# Python-wise build dependencies
BuildRequires:  python-devel

# Thrift-wise build dependencies:
BuildRequires:  thrift >= 0.9.1


%description
Apache Aurora is a service scheduler that runs on top of Mesos, enabling you to schedule
long-running services that take advantage of Mesos' scalability, fault-tolerance, and
resource isolation.

###################################
%package client
Summary:  A client for scheduling services against Apache Aurora

Requires: python-mock >= 1.0.1
Requires: python-argparse >= 1.2.1
Requires: python-mox >= 0.5.3
Requires: python-psutil >= 1.1.2
Requires: python-pystachio >= 0.7.2
Requires: PyYAML >= 3.10
Requires: thrift >= 0.9.1

%description client
TODO Needs more love
###########################

%package -n thermos
Summary: A simple Pythonic process management framework for Mesos chroots

Requires: python-psutil >= 1.2.1
Requires: python-pystachio >= 0.7.2
Requires: python-mako >= 0.4.0
Requires: python-mock >= 1.0.1
Requires: python-cherrypy >= 3.2.2
Requires: python-bottle >= 0.11.6
Requires: thrift >= 0.9.1

%description -n thermos
Thermos a simple process management framework used for orchestrating
dependent processes within a single Mesos chroot.  

%prep
%setup -q -n incubator-%{name}-%{version}
cp %{SOURCE1} ./pom.xml

# Generates Java-specific Thrift bindings.
# TODO - BARFS HERE!
for thrift_file in src/main/thrift/**/*.thrift; do
  thrift --gen java:hashcode -o generated-src ${thrift_file}
done

# Generates Python-specific Thrift bindings.
for thrift_struct in %{PYTHON_THRIFT_STRUCTS}; do
  %{_python} src/main/python/apache/aurora/tools/java/thrift_wrapper_codegen.py \
  src/main/thrift/org/apache/aurora/gen/api.thrift generated-src/gen-java \
  ${thrift_struct}
done


%pom_add_plugin org.apache.maven.plugins:maven-compiler-plugin . "
  <configuration>
    <source>%{JAVA_VERSION}</source>
    <target>%{JAVA_VERSION}</target>
  </configuration>"

%build
# Builds Aurora server Java JARs.
%mvn_build

%install
%mvn_install

%files
%doc LICENSE README.md

%files -n thermos
%doc LICENSE src/main/python/apache/thermos/README.md



%changelog
* Tue Jan  7 2014 Steve Salevan <ssalevan@twitter.com>
- Initial specfile writeup.
