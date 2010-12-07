# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro ; only that wy a new akmod package will 
# get build (and only then one is is actually needed)
%define buildforkernels newest

%define         svn 1

# name should have a -kmod suffix
Name:           omnibook-kmod

Version:        2.20090714
Release:        0.5.svn288%{?dist}.6
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
# fix compilation with kernel-2.6.34: http://sourceforge.net/tracker/?func=detail&aid=2978676&group_id=174260&atid=868544
Patch2:         %{name}-backlight-2.6.34.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
%patch2 -p1 -b .bl
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
* Tue Dec 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.6
- rebuild for updated kernel

* Thu Oct 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.5
- rebuild for new kernel

* Sun Sep 19 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.4
- rebuild for new kernel

* Sat Sep 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.3
- rebuild with akmod package and add proper hint to spec file

* Sat Sep 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.2
- rebuild for new kernel

* Fri Sep 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.5.svn288.1
- rebuild for new kernel

* Sun Sep 05 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.5.svn288
- fix build with kernel 2.6.34

* Sat Aug 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.14
- rebuild for new kernel

* Fri Aug 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.13
- rebuild for new kernel

* Wed Aug 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.12
- rebuild for new kernel

* Sun Aug 08 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.11
- rebuild for new kernel

* Tue Jul 27 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.10
- rebuild for new kernel

* Wed Jul 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.9
- rebuild for new kernel

* Fri Jun 18 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.8
- rebuild for new kernel

* Fri May 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.7
- rebuild for new kernel

* Thu May 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.6
- rebuild for new kernel

* Mon May 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.5
- rebuild for new kernel

* Fri May 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.4
- rebuild for new kernel

* Tue May 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.3
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.2
- rebuild for new kernel

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.20090714-0.4.svn288.1
- rebuild for new kernel

* Sat Jan 09 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.4.svn288
- build only akmods in rawhide

* Fri Jan 08 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.3.svn288
- fix build on rawhide

* Thu Jan 07 2010 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.2.svn288
- drop unnecessary ExclusiveArch
- drop double BR: kmodtool

* Wed Sep 16 2009 Dominik Mierzejewski <rpm@greysector.net> 2.20090714-0.1.svn288
- initial build for RPM Fusion
