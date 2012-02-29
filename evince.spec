%define _disable_ld_no_undefined 1

%define major 3
%define api 3.0
%define gir_major 3.0
%define libevdocument %mklibname evdocument 3 %{major}
%define libevview %mklibname evview 3 %{major}
%define girname	%mklibname %{name}-gir %{gir_major}
%define develname %mklibname -d %{name}

%define build_dvi 1

Summary: GNOME Document viewer
Name:    evince
Version: 3.2.1
Release: 1
License: GPLv2+ and GFDL+
Group:   Graphical desktop/GNOME
URL:     http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	ghostscript
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-icon-theme
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	tiff-devel
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
Requires: ghostscript
Requires: ghostscript-module-X
Requires(post,postun): desktop-file-utils

%if %build_dvi
BuildRequires: kpathsea-devel
#gw just like xdvi, needed for rendering the fonts
Suggests: texlive
%endif

%description
Evince is the GNOME Document viewer. It supports PDF, PostScript and other 
formats.

%package -n %{libevdocument}
Group:System/Libraries
Summary: GNOME Document viewer library

%description -n %{libevdocument}
This is the shared evdocument library for %{name}.

%package -n %{libevview}
Group:System/Libraries
Summary: GNOME Document viewer library

%description -n %{libevview}
This is the shared evview library for %{name}.

%package -n %{girname}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries
Requires: %{libevview} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Group:Development/C
Summary: GNOME Document viewer library
Requires: %{libevdocument} = %{version}
Requires: %{libevview} = %{version}
Provides: evince-devel = %{version}-%{release}

%description -n %{develname}
This is the GNOME Document viewer library, the shared parts of evince.

%prep
%setup -q
%apply_patches

%build
%configure \
	--disable-static \
	--enable-tiff \
	--enable-djvu \
	--enable-comics \
	--disable-schemas-compile \
	--disable-scrollkeeper \
%if %build_dvi
	--enable-dvi \
%endif
	--enable-gtk-doc \
	--enable-introspection 

%make LIBS='-lgmodule-2.0'

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc NEWS AUTHORS TODO
%{_bindir}/*
%{_datadir}/evince
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/evince*
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/GConf/gsettings/evince.convert
%{_datadir}/thumbnailers/evince.thumbnailer
%{_mandir}/man1/evince.1*
%{_libdir}/nautilus/extensions-3.0/libevince*so*
%dir %{_libdir}/evince/%{major}/
%dir %{_libdir}/evince/%{major}/backends
%{_libdir}/evince/%{major}/backends/lib*
%{_libdir}/evince/%{major}/backends/comicsdocument.evince-backend
%{_libdir}/evince/%{major}/backends/djvudocument.evince-backend
%if %build_dvi
%{_libdir}/evince/%{major}/backends/dvidocument.evince-backend
%endif
%{_libdir}/evince/%{major}/backends/pdfdocument.evince-backend
%{_libdir}/evince/%{major}/backends/psdocument.evince-backend
%{_libdir}/evince/%{major}/backends/tiffdocument.evince-backend
%{_libdir}/evince/%{major}/backends/xpsdocument.evince-backend
%{_libexecdir}/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service

%files -n %{libevdocument}
%{_libdir}/libevdocument3.so.%{major}*

%files -n %{libevview}
%{_libdir}/libevview3.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/EvinceDocument-%{gir_major}.typelib
%{_libdir}/girepository-1.0/EvinceView-%{gir_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_datadir}/gtk-doc/html/evince
%{_datadir}/gtk-doc/html/libevdocument-%{api}
%{_datadir}/gtk-doc/html/libevview-%{api}
%{_libdir}/libevdocument3.so
%{_libdir}/libevview3.so
%{_libdir}/pkgconfig/evince*pc
%{_includedir}/evince*
%{_datadir}/gir-1.0/*.gir
