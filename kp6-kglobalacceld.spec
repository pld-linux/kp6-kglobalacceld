#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeplasmaver	6.5.0
%define		qt_ver		6.7.0
%define		kf_ver		6.10.0
%define		kpname		kglobalacceld
Summary:	KDE global shortcuts server and library
Summary(pl.UTF-8):	Biblioteka i serwer globalnych skrótów klawiszowych KDE
Name:		kp6-kglobalacceld
Version:	6.5.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/kglobalacceld-%{version}.tar.xz
# Source0-md5:	d2817f495dddbd728792b4238901b833
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kcrash-devel >= %{kf_ver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kglobalaccel-devel >= %{kf_ver}
BuildRequires:	kf6-kio-devel >= %{kf_ver}
BuildRequires:	kf6-kjobwidgets-devel >= %{kf_ver}
BuildRequires:	kf6-kservice-devel >= %{kf_ver}
BuildRequires:	kf6-kwindowsystem-devel >= %{kf_ver}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt6DBus >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Qml >= %{qt_ver}
Requires:	Qt6Widgets >= %{qt_ver}
Requires:	kf6-kconfig >= %{kf_ver}
Requires:	kf6-kcoreaddons >= %{kf_ver}
Requires:	kf6-kcrash >= %{kf_ver}
Requires:	kf6-kdbusaddons >= %{kf_ver}
Requires:	kf6-kglobalaccel >= %{kf_ver}
Requires:	kf6-kio >= %{kf_ver}
Requires:	kf6-kjobwidgets >= %{kf_ver}
Requires:	kf6-kservice >= %{kf_ver}
Requires:	kf6-kwindowsystem >= %{kf_ver}
Requires:	qt6-qdbus
%requires_eq_to Qt6Core Qt6Core-devel
Provides:	kf5-kglobalaccel-service = %{version}-%{release}
Obsoletes:	kf5-kglobalaccel-service < 6
Conflicts:	kf5-kglobalaccel < 5.116.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE global shortcuts server and library.

%description -l pl.UTF-8
Biblioteka i serwer globalnych skrótów klawiszowych KDE.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf6-kglobalaccel-devel >= %{kf_ver}
Requires:	libstdc++-devel >= 6:8

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
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-Dqdbus_EXECUTABLE:PATH=/usr/bin/qdbus-qt6

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{_libdir}/libKGlobalAccelD.so.*.*
%ghost %{_libdir}/libKGlobalAccelD.so.0
/etc/xdg/autostart/kglobalacceld.desktop
%{systemduserunitdir}/plasma-kglobalaccel.service
%dir %{_libdir}/qt6/plugins/org.kde.kglobalacceld.platforms
%{_libdir}/qt6/plugins/org.kde.kglobalacceld.platforms/KGlobalAccelDXcb.so
%attr(755,root,root) %{_prefix}/libexec/kglobalacceld
%{_datadir}/qlogging-categories6/kglobalacceld.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KGlobalAccelD
%{_libdir}/cmake/KGlobalAccelD
