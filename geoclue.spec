# Tarfile created using git
# git clone git://anongit.freedesktop.org/geoclue
# git archive --format=tar --prefix=geoclue-0.11.1.1/ %{git_version} | gzip > ~/geoclue-%{version}-%{gitdate}.tar.gz

%define gitdate 20091026
%define git_version 73b6729
%define tarfile %{name}-%{version}-%{gitdate}.tar.gz
%define snapshot %{gitdate}git%{git_version}

Name:           geoclue
Version:        0.11.1.1
Release:        0.13.%{snapshot}%{?dist}
Summary:        A modular geoinformation service

Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://geoclue.freedesktop.org/
#Source0:        http://folks.o-hand.com/jku/geoclue-releases/%{name}-%{version}.tar.gz
Source0:        %{tarfile}
Patch0:         geoclue-nm08.patch
Patch1:         0001-Add-error-type-registration.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=528897#c15•
Patch2:         0002-Don-t-lose-special-D-Bus-error-sauce-when-copying.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: libsoup-devel
BuildRequires: GConf2-devel
BuildRequires: gtk2-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
%ifnarch s390 s390x
BuildRequires: gypsy-devel
%endif
BuildRequires: gtk-doc

# Require these until we move back to a formal release
BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf

Requires: dbus

%description
Geoclue is a modular geoinformation service built on top of the D-Bus 
messaging system. The goal of the Geoclue project is to make creating 
location-aware applications as simple as possible. 

%package devel
Summary: Development package for geoclue
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus-devel
Requires: libxml2-devel
Requires: pkgconfig

%description devel
Files for development with geoclue.

%package doc
Summary: Developer documentation for geoclue
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk-doc
BuildArch: noarch

%description doc
Developer documentation for geoclue

%package gui
Summary: Testing gui for geoclue
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description gui
Testing gui for geoclue

%ifnarch s390 s390x
%package gypsy
Summary: gypsy provider for geoclue
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description gypsy
A gypsy provider for geoclue
%endif

%prep
%setup -q
%patch0 -p1 -b .nm08
%patch1 -p1 -b .reg-errors
%patch2 -p1 -b .error-sauce

%build
./autogen.sh
%ifarch s390 s390x
%configure --disable-static --enable-gtk-doc --enable-networkmanager=yes --enable-skyhook=yes
%else
%configure --disable-static --enable-gtk-doc --enable-networkmanager=yes --enable-gypsy=yes --enable-skyhook=yes
%endif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgeoclue.la
# Install the test gui as it seems the test isn't installed any more
mkdir $RPM_BUILD_ROOT%{_bindir}
cp test/.libs/geoclue-test-gui $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%dir %{_datadir}/geoclue-providers
%{_libdir}/libgeoclue.so.0
%{_libdir}/libgeoclue.so.0.0.0
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Master.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Example.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Geonames.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Hostip.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Localnet.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Manual.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Plazes.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Skyhook.service
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Yahoo.service
%{_datadir}/geoclue-providers/geoclue-example.provider
%{_datadir}/geoclue-providers/geoclue-geonames.provider
%{_datadir}/geoclue-providers/geoclue-hostip.provider
%{_datadir}/geoclue-providers/geoclue-localnet.provider
%{_datadir}/geoclue-providers/geoclue-manual.provider
%{_datadir}/geoclue-providers/geoclue-plazes.provider
%{_datadir}/geoclue-providers/geoclue-skyhook.provider
%{_datadir}/geoclue-providers/geoclue-yahoo.provider
%{_libexecdir}/geoclue-example
%{_libexecdir}/geoclue-geonames
%{_libexecdir}/geoclue-hostip
%{_libexecdir}/geoclue-localnet
%{_libexecdir}/geoclue-manual
%{_libexecdir}/geoclue-master
%{_libexecdir}/geoclue-plazes
%{_libexecdir}/geoclue-skyhook
%{_libexecdir}/geoclue-yahoo

%files devel
%defattr(-,root,root,-)
%{_includedir}/geoclue
%{_libdir}/pkgconfig/geoclue.pc
%{_libdir}/libgeoclue.so

%files doc
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/geoclue/

%files gui
%defattr(-,root,root,-)
%{_bindir}/geoclue-test-gui

%ifnarch s390 s390x
%files gypsy
%defattr(-,root,root,-)
%{_libexecdir}/geoclue-gypsy
%{_datadir}/geoclue-providers/geoclue-gypsy.provider
%{_datadir}/dbus-1/services/org.freedesktop.Geoclue.Providers.Gypsy.service
%endif

%changelog
* Thu Jun 24 2010 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.13
- Disable gypsy sub-package on s390
Related: rhbz#606853

* Fri Jan 29 2010 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.12
- Fix crashers in geoclue-master provider
Related: rhbz#543948

* Thu Dec 17 2009 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.11
- Remove gammu and gpsd BuildRequires (#547787)
Related: rhbz#543948

* Tue Dec  1 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.11.1.1-0.10.1
- Do not build against gammu on s390/s390x

* Mon Oct 24 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1.1-0.10
- Rebuild for new NetworkManager

* Mon Oct 24 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1.1-0.9
- New git snapshit, enable NetworkManager support for WiFi location, gsmloc and new Skyhook plugin

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1.1-0.8.20090310git3a31d26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1.1-0.7
- Move develop documentation to its own noarch package to fix RHBZ 513488

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.6
- Add developer documentation

* Fri Jun 19 2009 Bastien Nocera <bnocera@redhat.com> 0.11.1.1-0.4
- Fix geoclue-test-gui (#506921)

* Thu Apr 09 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1.1-0.3
- Fix install of test gui

* Sun Mar 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.11.1.1-0.2
- Rebuild for new gpsd

* Tue Mar 10 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1.1-0.1
- Move to a git snapshot until we finally get a new stable release

* Wed Mar 4 2009 Peter Robinson <pbrobinson@gmail.com> 0.11.1-15
- Move docs to noarch, a few spec file cleanups

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-13
- Fix summary

* Thu Jul 31 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-12
- Once more for fun

* Thu Jul 31 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-11
- Increment build number to allow for clean F-8 and F-9 to F-10 upgrade

* Wed Jul 2 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-6
- Fixed spec file so gpsd and gypsy are actually properly in a subpackage

* Sun May 18 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-5
- Added gypsy and gpsd providers to build as sub packages

* Mon Apr 28 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-4
- Moved api documentation to -devel

* Sat Apr 26 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-3
- Cleanup requires and group for test gui

* Sat Apr 26 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-2
- Some spec file cleanups

* Fri Apr 25 2008 Peter Robinson <pbrobinson@gmail.com> 0.11.1-1
- Initial package
