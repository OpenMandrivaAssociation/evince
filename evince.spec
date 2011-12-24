%define _disable_ld_no_undefined 1

%define major 3
%define api 2.32
%define libname %mklibname evince %{major}
%define develname %mklibname -d evince

%define build_dvi 1
%define build_impress 1

Summary: GNOME Document viewer
Name:    evince
Version: 2.32.0
Release: 7
License: GPLv2+ and GFDL+
Group:   Graphical desktop/GNOME
URL:     http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: evince-2.24.0-CVE-2010-2640,2641,2642,2643.diff

Requires: ghostscript ghostscript-module-X
BuildRequires: libGConf2-devel >= 2.31.2
BuildRequires: GConf2
BuildRequires: glib2.0-common
BuildRequires: gtk+2-devel
BuildRequires: libgail-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: libxt-devel
BuildRequires: libpoppler-glib-devel >= 0.14.0
BuildRequires: libspectre-devel
BuildRequires: nautilus-devel
BuildRequires: libtiff-devel
BuildRequires: libxslt-proc
BuildRequires: gnome-icon-theme
BuildRequires: gobject-introspection-devel
BuildRequires: glib2-devel >= 2.25.3
#BuildRequires: t1lib-devel
%if %build_dvi
BuildRequires: kpathsea-devel
#gw just like xdvi, needed for rendering the fonts
Suggests: texlive
%endif
BuildRequires: djvulibre-devel >= 3.5.17
BuildRequires: libgcrypt-devel
BuildRequires: ghostscript
BuildRequires: intltool
#gw if we run autoconf
BuildRequires: gnome-doc-utils
BuildRequires: gnome-common
BuildRequires: gtk-doc
BuildRequires: glib2.0-common
Requires(post,postun): desktop-file-utils

%description
Evince is the GNOME Document viewer. Its supports PDF, PostScript and other formats.

%package -n %{libname}
Group:System/Libraries
Summary: GNOME Document viewer library

%description -n %{libname}
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %{develname}
Group:Development/C
Summary: GNOME Document viewer library
Requires: %{libname} = %{version}
Provides: evince-devel = %{version}-%{release}

%description -n %{develname}
This is the GNOME Document viewer library, the shared parts of evince.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-tiff \
	--enable-djvu \
	--enable-pixbuf \
	--enable-comics \
	--disable-static \
	--disable-schemas-compile \
	--disable-schemas-install \
	--disable-scrollkeeper \
%if %build_impress
	--enable-impress \
%endif
%if %build_dvi
	--enable-dvi \
%endif
	--enable-gtk-doc \
	--enable-introspection 
#	--enable-t1lib 

%make LIBS='-lgmodule-2.0'

%install
rm -rf %{buildroot} %{name}.lang
%makeinstall_std
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%find_lang %{name} --with-gnome
for omf in %{buildroot}%{_datadir}/omf/*/{*-??,*-??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%{buildroot}!!)" >> %{name}.lang
done

%post
%define schemas %{name}-thumbnailer %{name}-thumbnailer-djvu %{?build_dvi:%{name}-thumbnailer-dvi} evince-thumbnailer-comics evince-thumbnailer-ps

%preun
%preun_uninstall_gconf_schemas %schemas

%files -f %{name}.lang
%doc NEWS AUTHORS TODO
# README
%{_sysconfdir}/gconf/schemas/%{name}-thumbnailer.schemas
%{_sysconfdir}/gconf/schemas/%{name}-thumbnailer-djvu.schemas
%{_sysconfdir}/gconf/schemas/%{name}-thumbnailer-comics.schemas
%if %build_dvi
%{_sysconfdir}/gconf/schemas/%{name}-thumbnailer-dvi.schemas
%endif
%{_sysconfdir}/gconf/schemas/%{name}-thumbnailer-ps.schemas
%{_bindir}/*
%{_datadir}/evince
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/evince*
%{_datadir}/glib-2.0/schemas/org.gnome.Evince.gschema.xml
%{_datadir}/GConf/gsettings/evince.convert
%dir %{_datadir}/omf/%{name}
%{_datadir}/omf/%{name}/%{name}-C.omf
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
%if %build_impress
%{_libdir}/evince/%{major}/backends/impressdocument.evince-backend
%endif
%{_libdir}/evince/%{major}/backends/pdfdocument.evince-backend
%{_libdir}/evince/%{major}/backends/pixbufdocument.evince-backend
%{_libdir}/evince/%{major}/backends/psdocument.evince-backend
%{_libdir}/evince/%{major}/backends/tiffdocument.evince-backend
%_libexecdir/evince-convert-metadata
%_libexecdir/evinced
%{_datadir}/dbus-1/services/org.gnome.evince.Daemon.service

%files -n %{libname}
%{_libdir}/libevdocument.so.%{major}*
%{_libdir}/libevview.so.%{major}*
%{_libdir}/girepository-1.0/*.typelib

%files -n %{develname}
%doc ChangeLog
%{_datadir}/gtk-doc/html/evince
%{_datadir}/gtk-doc/html/libevdocument-%api
%{_datadir}/gtk-doc/html/libevview-%api
%{_libdir}/libevdocument.so
%{_libdir}/libevview.so
%{_libdir}/pkgconfig/evince*pc
%{_includedir}/evince*
%{_datadir}/gir-1.0/*.gir
