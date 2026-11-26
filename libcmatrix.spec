#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Matrix protocol library written in C using GObject
Summary(pl.UTF-8):	Biblioteka protokołu Matrix napisana w C z użyciem GObject
Name:		libcmatrix
Version:	0.0.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://source.puri.sm/Librem5/libcmatrix/-/releases
Source0:	https://source.puri.sm/Librem5/libcmatrix/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	f6d3c82fd083133444c6d37f00fb53c1
URL:		https://source.puri.sm/Librem5/libcmatrix
# -std=gnu18
BuildRequires:	gcc >= 6:7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.70
BuildRequires:	json-glib-devel >= 1.8.0
BuildRequires:	libgcrypt-devel
BuildRequires:	libsecret-devel
BuildRequires:	libsoup3-devel >= 3.4.4
BuildRequires:	meson >= 0.63.0
BuildRequires:	ninja >= 1.5
BuildRequires:	olm-devel >= 3.2.11
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sqlite3-devel >= 3.26.0
Requires:	glib2 >= 1:2.70
Requires:	json-glib >= 1.8.0
Requires:	libsoup3 >= 3.4.4
Requires:	olm >= 3.2.11
Requires:	sqlite3 >= 3.26.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matrix protocol library written in C using GObject.

%description -l pl.UTF-8
Biblioteka protokołu Matrix napisana w C z użyciem GObject.

%package devel
Summary:	Header files for libcmatrix library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcmatrix
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.70

%description devel
Header files for libcmatrix library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcmatrix.

%package static
Summary:	Static libcmatrix library
Summary(pl.UTF-8):	Statyczna biblioteka libcmatrix
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcmatrix library.

%description static -l pl.UTF-8
Statyczna biblioteka libcmatrix.

%package apidocs
Summary:	API documentation for libcmatrix library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libcmatrix
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libcmatrix library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libcmatrix.

%prep
%setup -q -n %{name}-v%{version}

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dbuild-examples=false \
	-Dbuild-tests=false \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dintrospection=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libcmatrix-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_libdir}/libcmatrix.so.0u
%{_libdir}/girepository-1.0/CM-0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcmatrix.so
%{_includedir}/libcmatrix
%{_datadir}/gir-1.0/CM-0.gir
%{_pkgconfigdir}/libcmatrix.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmatrix.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libcmatrix-0
%endif
