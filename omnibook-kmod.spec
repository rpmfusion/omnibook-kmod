# (un)define the next line to either build for the newest or all current kernels
%define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmods

%define         svn 1

# name should have a -kmod suffix
Name:           omnibook-kmod

Version:        2.20090714
Release:        0.3.svn288%{?dist}.16
Summary:        Kernel module for HP Omnibook/Pavillon, Toshiba Satellite and Compal laptops

Group:          System Environment/Kernel

License:        GPLv2
URL:            http://sourceforge.net/projects/omnibook/
%if %{svn}
# svn export -r288 https://omnibook.svn.sourceforge.net/svnroot/omnibook/omnibook/trunk omnibook-2.20090714
Source0:        omnibook-%{version}.tar.xz
%else
Source0:        http://downloads.sourceforge.net/project/omnibook/omnibook%20kernel%20module/%{version}/omnibook-%{version}.tar.gz
%endif
# silence some warnings: http://sourceforge.net/tracker/?func=detail&aid=2703528&group_id=174260&atid=868544
Patch0:         %{name}-warnings.patch
# add support for Toshiba Satellite A300D: http://sourceforge.net/tracker/?func=detail&aid=2841062&group_id=174260&atid=868544
Patch1:         %{name}-a300d.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

ExclusiveArch:  i686 x86_64

# get the proper build-sysbuild package from the repo, which
# tracks in all the kernel-devel packages
BuildRequires:  %{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
Linux kernel module for many HP Omnibook/Pavillon, Toshiba Satellite
(with Phoenix BIOS) and Compal laptops. It is based on the module found
in the 'omke' project.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

# apply patches and do other stuff here
pushd omnibook-%{version}
%patch0 -p1 -b .warn
%patch1 -p1 -b .a300d
popd

for kernel_version in %{?kernel_versions} ; do
    cp -a omnibook-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*} modules
done


%install
for kernel_version in %{?kernel_versions}; do
# doesn't work
#    make install -C "${kernel_version##*___}" DESTDIR=${RPM_BUILD_ROOT} KMODPATH=%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install -D -m 755 _kmod_build_${kernel_version%%___*}/omnibook.ko  ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/omnibook.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat May 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.16
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.15
- rebuild for new kernel

* Thu Apr 22 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.14
- rebuild for new kernel

* Mon Apr 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.13
- rebuild for new kernel

* Sat Apr 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.12
- rebuild for new kernel

* Sat Apr 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.11
- rebuild for new kernel

* Mon Mar 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.10
- rebuild for new kernel

* Fri Mar 05 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.9
- rebuild for new kernel

* Mon Mar 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.8
- rebuild for new kernel

* Sun Feb 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.7
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.6
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.5
- rebuild for new kernel

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.4
- rebuild for new kernel

* Wed Feb 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.3
- rebuild for new kernel

* Sat Jan 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.2
- rebuild for new kernel

* Wed Jan 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.3.svn288.1
- rebuild for new kernel

* Sat Jan 09 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.3.svn288
- ExclusiveArch is still necessary on F-12

* Thu Jan 07 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.2.svn288
- drop unnecessary ExclusiveArch
- drop double BR: kmodtool

* Wed Sep 16 2009 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.1.svn288
- initial build for RPM Fusion
