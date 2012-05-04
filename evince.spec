%define build_dvi 1

%define major			4
%define major_evdocument	4
%define major_evview		3
%define api			3.0
%define gir_major		3.0
%define devname			%mklibname -d %{name}
%define libname_evdocument	%mklibname evdocument 3 %{major_evdocument}
%define libname_evview		%mklibname evview 3 %{major_evview}

%define girname			%mklibname %{name}-gir %{gir_major}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Summary:	GNOME Document viewer
Name:		evince
Version:	3.4.0
Release:	11
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(cairo-pdf)
BuildRequires:	pkgconfig(cairo-ps)
BuildRequires:	pkgconfig(ddjvuapi) >= 3.5.17
BuildRequires:	pkgconfig(gail-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gio-2.0) >= 2.31.0
BuildRequires:	pkgconfig(gnome-icon-theme) >= 2.17.1
BuildRequires:	pkgconfig(gnome-keyring-1) >= 2.22.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.6
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gtk+-unix-print-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gtk+-x11-3.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libgxps) >= 0.2.0
BuildRequires:	pkgconfig(libnautilus-extension) >= 2.91.4
BuildRequires:	pkgconfig(libspectre) >= 0.2.0
BuildRequires:	pkgconfig(libxml-2.0) >= 2.5.0
BuildRequires:	pkgconfig(poppler-glib) >= 0.18.0
BuildRequires:	pkgconfig(sm) >= 1.0.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	tiff-devel
BuildRequires:	ghostscript
BuildRequires:	intltool
#gw if we run autoconf
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-icon-theme
BuildRequires:	gtk-doc
Requires:	ghostscript
Requires:	ghostscript-module-X

%description
Evince is the GNOME Document viewer.
It supports PDF, PostScript and other formats.
To view .dvi files as produced by TeX in evince,
install the %{name}-dvi package.

%if %build_dvi
%package dvi
Summary:	TeX DVI document support for evince
Group:		Graphical desktop/GNOME
BuildRequires:	kpathsea-devel
#gw just like xdvi, needed for rendering the fonts
Requires:	texlive
Requires:	texlive-texmf
Requires:	%{name} = %{version}-%{release}

%description dvi
This package adds support for displaying .dvi files to evince.
These files are 
produced by TeX, often using
a macro package like LaTeX.
%endif

%package -n %{libname_evdocument}
Group:		System/Libraries
Summary:	GNOME Document viewer library
Obsoletes:	%{mklibname %{name} 3} < 3.3.92

%description -n %{libname_evdocument}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{libname_evview}
Group:		System/Libraries
Summary:	GNOME Document viewer library

%description -n %{libname_evview}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{devname}
Group:		Development/C
Summary:	GNOME Document viewer library
Requires:	%{libname_evdocument} = %{version}-%{release}
Requires:	%{libname_evview} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname_evdocument} = %{version}-%{release}
Requires:	%{libname_evview} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-tiff \
	--enable-djvu \
	--enable-comics \
%if %build_dvi
	--enable-dvi \
%endif
	--enable-gtk-doc \
	--enable-introspection \
	--disable-static \
	--disable-scrollkeeper \
	--disable-schemas-compile

%make

%install
%makeinstall_std

%find_lang %{name} --with-gnome

find %{buildroot} -name *.la -delete

%files -f %name.lang
%doc NEWS AUTHORS TODO
%{_bindir}/*
%{_datadir}/evince
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/evince*
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/GConf/gsettings/evince.convert
%{_mandir}/man1/evince.1*
%{_libdir}/nautilus/extensions-3.0/libevince*so*
%dir %{_libdir}/evince/%{major}/
%dir %{_libdir}/evince/%{major}/backends
%{_libdir}/evince/%{major}/backends/libcomicsdocument.so
%{_libdir}/evince/%{major}/backends/comicsdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libdjvudocument.so
%{_libdir}/evince/%{major}/backends/djvudocument.evince-backend
%{_libdir}/evince/%{major}/backends/libpdfdocument.so
%{_libdir}/evince/%{major}/backends/pdfdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libpsdocument.so
%{_libdir}/evince/%{major}/backends/psdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libtiffdocument.so
%{_libdir}/evince/%{major}/backends/tiffdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libxpsdocument.so
%{_libdir}/evince/%{major}/backends/xpsdocument.evince-backend
%{_libexecdir}/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%{_datadir}/thumbnailers/evince.thumbnailer

%if %build_dvi
%files dvi
%{_libdir}/evince/%{major}/backends/libdvidocument.so
%{_libdir}/evince/%{major}/backends/dvidocument.evince-backend
%endif

%files -n %{libname_evdocument}
%{_libdir}/libevdocument3.so.%{major_evdocument}*

%files -n %{libname_evview}
%{_libdir}/libevview3.so.%{major_evview}*

%files -n %{girname}
%{_libdir}/girepository-1.0/EvinceDocument-%{gir_major}.typelib
%{_libdir}/girepository-1.0/EvinceView-%{gir_major}.typelib

%files -n %{devname}
%doc ChangeLog
%{_datadir}/gtk-doc/html/evince
%{_datadir}/gtk-doc/html/libevdocument-%{api}
%{_datadir}/gtk-doc/html/libevview-%{api}
%{_libdir}/libevdocument3.so
%{_libdir}/libevview3.so
%{_libdir}/pkgconfig/evince*pc
%{_includedir}/evince*
%{_datadir}/gir-1.0/EvinceDocument-%{gir_major}.gir
%{_datadir}/gir-1.0/EvinceView-%{gir_major}.gir
