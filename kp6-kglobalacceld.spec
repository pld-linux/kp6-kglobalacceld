#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.5
%define		qtver		5.15.2
%define		kpname		kglobalacceld
Summary:	kgglobalacceld
Name:		kp6-kglobalacceld
Version:	6.3.5
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/kglobalacceld-%{version}.tar.xz
# Source0-md5:	80d5b2fe1c78d16e647f15eb38a7d37f
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kglobalacceld

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.


%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
/etc/xdg/autostart/kglobalacceld.desktop
%{systemduserunitdir}/plasma-kglobalaccel.service
%ghost %{_libdir}/libKGlobalAccelD.so.0
%attr(755,root,root) %{_libdir}/libKGlobalAccelD.so.*.*
%dir %{_libdir}/qt6/plugins/org.kde.kglobalacceld.platforms
%attr(755,root,root) %{_libdir}/qt6/plugins/org.kde.kglobalacceld.platforms/KGlobalAccelDXcb.so
%attr(755,root,root) %{_prefix}/libexec/kglobalacceld

%files devel
%defattr(644,root,root,755)
%{_includedir}/KGlobalAccelD
%{_libdir}/cmake/KGlobalAccelD
