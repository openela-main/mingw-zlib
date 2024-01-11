%?mingw_package_header

Name:           mingw-zlib
Version:        1.2.8
Release:        10%{?dist}
Summary:        MinGW Windows zlib compression library

License:        zlib
Group:          Development/Libraries
URL:            http://www.zlib.net/
Source0:        http://www.zlib.net/zlib-%{version}.tar.gz
# Replace the zlib build system with an autotools based one
Patch3:         mingw32-zlib-1.2.7-autotools.patch
# The .def file contains an empty LIBRARY line which isn't valid
Patch5:         zlib-1.2.7-use-correct-def-file.patch
# Libtool tries to make a libz-1.dll while we expect zlib1.dll
# Force this by hacking the ltmain.sh
Patch6:         mingw32-zlib-create-zlib1-dll.patch

# Backported from zlib-1.2.11-CVE-2018-25032.patch
# https://github.com/madler/zlib/commit/5c44459c3b28a9bd3283aaceab7c615f8020c531
Patch7:         zlib-1.2.8-CVE-2018-25032.patch

BuildArch:      noarch
ExclusiveArch: %{ix86} x86_64

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

BuildRequires:  perl-interpreter
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
MinGW Windows zlib compression library.


# Win32
%package -n mingw32-zlib
Summary:        MinGW Windows zlib compression library for the win32 target

%description -n mingw32-zlib
MinGW Windows zlib compression library for the win32 target.


%package -n mingw32-zlib-static
Summary:        Static libraries for mingw32-zlib development.
Group:          Development/Libraries
Requires:       mingw32-zlib = %{version}-%{release}

%description -n mingw32-zlib-static
The mingw32-zlib-static package contains static library for mingw32-zlib development.


%package -n mingw32-minizip
Summary:        Minizip manipulates files from a .zip archive
Group:          Development/Libraries
Requires:       mingw32-zlib = %{version}-%{release}

%description -n  mingw32-minizip
MinGW Minizip manipulates files from a .zip archive.

# Win64
%package -n mingw64-zlib
Summary:        MinGW Windows zlib compression library for the win64 target

%description -n mingw64-zlib
MinGW Windows zlib compression library for the win64 target.

%package -n mingw64-zlib-static
Summary:        Static libraries for mingw64-zlib development
Requires:       mingw64-zlib = %{version}-%{release}

%description -n mingw64-zlib-static
The mingw64-zlib-static package contains static library for mingw64-zlib development.

%package -n mingw64-minizip
Summary:        Minizip manipulates files from a .zip archive
Requires:       mingw64-zlib = %{version}-%{release}

%description -n mingw64-minizip
MinGW Minizip manipulates files from a .zip archive.


%?mingw_debug_package


%prep
%setup -q -n zlib-%{version}
%patch3 -p1 -b .atools
%patch5 -p1 -b .def
# patch cannot create an empty dir
mkdir m4
iconv -f windows-1252 -t utf-8 <ChangeLog >ChangeLog.tmp

autoreconf --install --force

%patch6 -p0 -b .libtool
%patch7 -p1 -b .CVE-2018-25032


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
# Libtool tries to install a file called libz-1.dll
# but this isn't created anymore due to patch #6
# Fool libtool until a proper fix has been found
touch build_win32/.libs/libz-1.dll build_win64/.libs/libz-1.dll
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

# Manually install the correct zlib.dll
install -m 0644 build_win32/.libs/zlib1.dll $RPM_BUILD_ROOT%{mingw32_bindir}/
install -m 0644 build_win64/.libs/zlib1.dll $RPM_BUILD_ROOT%{mingw64_bindir}/

# Install the pkgconfig file
install -m 0644 build_win32/zlib.pc $RPM_BUILD_ROOT%{mingw32_libdir}/pkgconfig/
install -m 0644 build_win64/zlib.pc $RPM_BUILD_ROOT%{mingw64_libdir}/pkgconfig/

# Drop the fake libz-1.dll
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/libz-1.dll
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/libz-1.dll

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete

# Drop the man pages
rm -rf $RPM_BUILD_ROOT%{mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw64_mandir}


# Win32
%files -n mingw32-zlib
%{mingw32_includedir}/zconf.h
%{mingw32_includedir}/zlib.h
%{mingw32_libdir}/libz.dll.a
%{mingw32_bindir}/zlib1.dll
%{mingw32_libdir}/pkgconfig/zlib.pc

%files -n mingw32-zlib-static
%{mingw32_libdir}/libz.a

%files -n mingw32-minizip
%{mingw32_libdir}/libminizip.dll.a
%{mingw32_bindir}/libminizip-1.dll
%dir %{mingw32_includedir}/minizip
%{mingw32_includedir}/minizip/*.h
%{mingw32_libdir}/pkgconfig/minizip.pc

# Win64
%files -n mingw64-zlib
%{mingw64_includedir}/zconf.h
%{mingw64_includedir}/zlib.h
%{mingw64_libdir}/libz.dll.a
%{mingw64_bindir}/zlib1.dll
%{mingw64_libdir}/pkgconfig/zlib.pc

%files -n mingw64-zlib-static
%{mingw64_libdir}/libz.a

%files -n mingw64-minizip
%{mingw64_libdir}/libminizip.dll.a
%{mingw64_bindir}/libminizip-1.dll
%dir %{mingw64_includedir}/minizip
%{mingw64_includedir}/minizip/*.h
%{mingw64_libdir}/pkgconfig/minizip.pc


%changelog
* Mon May 09 2022 Uri Lublin <uril@redhat.com> - 1.2.8-10
- Fix CVE-2018-25032
  Resolves: rhbz#2068370

* Tue Aug 14 2018 Victor Toso <victortoso@redhat.com> - 1.2.8-9
- ExclusiveArch: i686, x86_64
- Related: rhbz#1615874

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-10
- Added win64 support
- Simplified the build process by using autotools and a hacked version of libtool
- Made the package compliant with the new MinGW packaging guidelines

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.2.5-9
- Renamed the source package to mingw-zlib (#800415)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Kalev Lember <kalevlember@gmail.com> - 1.2.5-8
- Remove the .la files
- Spec clean up

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-7
- Rebuild against the mingw-w64 toolchain
- Use the correct RPM macros
- Fix FTBFS against the latest binutils caused by the use of an invalid .def file

* Fri Feb 17 2012 David Tardon <dtardon@redhat.com> - 1.2.5-6
- fix dlname in libz.la

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.5-4
- Use the built .pc file instead of manually generating it

* Tue Apr 26 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.5-3
- Install zlib pkgconfig file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5
- Use %%global instead of %%define
- Automatically generate debuginfo subpackage
- Use correct %%defattr tag
- Merged the changes from the native Fedora package

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-18
- Cannot copy current directory into itself, so fix the copy command
  which creates 'x' subdirectory.

* Fri May  1 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 1.2.3-17
- BR autoconf, automake, libtool

* Thu Apr 30 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 1.2.3-16
- use autotools build system from native package

* Tue Mar  3 2009 W. Pilorz <wpilorz at gmail.com> - 1.2.3-15
- Add static subpackage.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-13
- Rebuild for mingw32-gcc 4.4

* Mon Jan 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-12
- Force rebuild to test maintenance account.

* Thu Dec 18 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-11
- Pass correct CFLAGS to build.

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-10
- Consider native patches.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-9
- Rename mingw -> mingw32.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-8
- Remove manpage.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-7
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Fix misnamed file: zlibdll.a -> zlib.dll.a
- Explicitly provide mingw(zlib1.dll).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Initial RPM release, largely based on earlier work from several sources.
