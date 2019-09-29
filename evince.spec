%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define build_dvi	1
%define major	4
%define major_evdocument	4
%define major_evview		3
%define api	3
%define gmajor	3.0
%define libevdocument	%mklibname evdocument %{api} %{major_evdocument}
%define libevview	%mklibname evview %{api} %{major_evview}
%define girname	%mklibname %{name}-gir %{gmajor}
%define devname	%mklibname -d %{name}
%define _userunitdir /usr/lib/systemd/user/

Summary:	GNOME Document viewer
Name:		evince
Version:	3.34.0
Release:	1
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	ghostscript
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	kpathsea-devel
BuildRequires:	tiff-devel
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(cairo-pdf)
BuildRequires:	pkgconfig(cairo-ps)
BuildRequires:	pkgconfig(ddjvuapi) >= 3.5.17
BuildRequires:	pkgconfig(gail-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gio-2.0) >= 2.31.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:  pkgconfig(gspell-1)
BuildRequires:	pkgconfig(adwaita-icon-theme) >= 2.17.1
BuildRequires:	pkgconfig(gnome-keyring-1) >= 2.22.0
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
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
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-base-1.0)
BuildRequires:	pkgconfig(gstreamer-video-1.0)
BuildRequires:	pkgconfig(synctex)
BuildRequires:	gnome-common
BuildRequires:	yelp-tools
BuildRequires:	gettext-devel

Requires:	ghostscript
Requires:	ghostscript-module-X

%description
Evince is the GNOME Document viewer.
It supports PDF, PostScript and other formats.
To view .dvi files as produced by TeX in evince,
install the %{name}-dvi package.

%if %{build_dvi}
%package dvi
Summary:	TeX DVI document support for evince
Group:		Graphical desktop/GNOME
#gw just like xdvi, needed for rendering the fonts
Requires:	texlive-xdvi
Requires:	%{name} = %{version}-%{release}

%description dvi
This package adds support for displaying .dvi files to evince.
These files are
produced by TeX, often using
a macro package like LaTeX.
%endif

%package -n %{libevdocument}
Group:		System/Libraries
Summary:	GNOME Document viewer library
Obsoletes:	%{mklibname %{name} 3} < 3.3.92

%description -n %{libevdocument}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{libevview}
Group:		System/Libraries
Summary:	GNOME Document viewer library

%description -n %{libevview}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Group:		Development/C
Summary:	GNOME Document viewer library
Requires:	%{libevdocument} = %{version}-%{release}
Requires:	%{libevview} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This is the GNOME Document viewer library, the shared parts of evince.

%prep
%setup -q
%apply_patches

%build
autoreconf -vfi
%configure \
	--enable-tiff \
	--enable-djvu \
	--enable-comics \
	--enable-gnome-desktop \
	--enable-multimedia \
%if %{build_dvi}
	--enable-dvi \
%endif
	--enable-gtk-doc=no \
	--enable-introspection \
	--disable-schemas-compile \
	--enable-compile-warnings=no

%make

%install
%makeinstall_std

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc NEWS AUTHORS TODO
%{_bindir}/*
%{_datadir}/evince
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/org.gnome.Evinc*
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
#{_libdir}/evince/%{major}/backends/libpsdocument.so
#{_libdir}/evince/%{major}/backends/psdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libtiffdocument.so
%{_libdir}/evince/%{major}/backends/tiffdocument.evince-backend
%{_libdir}/evince/%{major}/backends/libxpsdocument.so
%{_libdir}/evince/%{major}/backends/xpsdocument.evince-backend
#{_libdir}/mozilla/plugins/*.so
%{_libexecdir}/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service
%{_datadir}/thumbnailers/evince.thumbnailer
%{_datadir}/metainfo/org.gnome.Evince.appdata.xml
%{_datadir}/metainfo/%{name}*.metainfo.xml
%{_userunitdir}/org.gnome.Evince.service

%if %{build_dvi}
%files dvi
%{_libdir}/evince/%{major}/backends/libdvidocument.so
%{_libdir}/evince/%{major}/backends/dvidocument.evince-backend
%endif

%files -n %{libevdocument}
%{_libdir}/libevdocument%{api}.so.%{major_evdocument}*

%files -n %{libevview}
%{_libdir}/libevview%{api}.so.%{major_evview}*

%files -n %{girname}
%{_libdir}/girepository-1.0/EvinceDocument-%{gmajor}.typelib
%{_libdir}/girepository-1.0/EvinceView-%{gmajor}.typelib

%files -n %{devname}
%doc ChangeLog
%{_datadir}/gtk-doc/html/*
%{_libdir}/libevdocument%{api}.so
%{_libdir}/libevview%{api}.so
%{_libdir}/pkgconfig/evince*pc
%{_includedir}/evince*
%{_datadir}/gir-1.0/EvinceDocument-%{gmajor}.gir
%{_datadir}/gir-1.0/EvinceView-%{gmajor}.gir

