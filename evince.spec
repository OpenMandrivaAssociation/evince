%define build_dvi 1
%define major 1
%define libname %mklibname evince %major
%define develname %mklibname -d evince

Summary: GNOME Document viewer
Name:    evince
Version: 2.25.90
Release: %mkrel 1
License: GPLv2+ and GFDL+
Group:   Graphical desktop/GNOME
URL:     http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch1: evince-2.25.90-fix-linking.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: ghostscript ghostscript-module-X
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libxt-devel
BuildRequires: libpoppler-glib-devel >= 0.6
BuildRequires: libspectre-devel
BuildRequires: nautilus-devel
BuildRequires: libtiff-devel
BuildRequires: libxslt-proc
#BuildRequires: t1lib-devel
%if %build_dvi
BuildRequires: tetex-devel >= tetex-devel-3.0-22mdv
#gw just like xdvi, needed for rendering the fonts
Suggests: tetex
%endif
BuildRequires: djvulibre-devel >= 3.5.17
BuildRequires: libgcrypt-devel
BuildRequires: scrollkeeper
BuildRequires: ghostscript
BuildRequires: intltool
#gw if we run autoconf
BuildRequires: gnome-doc-utils
BuildRequires: gnome-common
BuildRequires: gtk-doc
Requires(post): scrollkeeper desktop-file-utils
Requires(postun): scrollkeeper desktop-file-utils

%description
Evince is the GNOME Document viewer. Its supports PDF, PostScript and other formats.

%package -n %libname
Group:System/Libraries
Summary: GNOME Document viewer library

%description -n %libname
This is the GNOME Document viewer library, the shared parts of evince.

%package -n %develname
Group:Development/C
Summary: GNOME Document viewer library
Requires: %libname = %version
Provides: libevince-devel = %version-%release

%description -n %develname
This is the GNOME Document viewer library, the shared parts of evince.

%prep
%setup -q
%patch1 -p1 -b .fix-linking
autoreconf -fi

%build
%configure2_5x --enable-tiff --enable-djvu --enable-pixbuf --enable-comics \
 --enable-impress \
%if %build_dvi
 --enable-dvi
%endif
#--enable-t1lib 

%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std _ENABLE_SK=no

%find_lang Evince --with-gnome
%find_lang %name --with-gnome
cat %name.lang >> Evince.lang
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> Evince.lang
done

rm -f %buildroot%_libdir/nautilus/extensions-*/libevince*a \
      %buildroot%_libdir/evince/*/backends/lib*a %buildroot%_libdir/lib*.a

%post
%if %mdkversion < 200900
%update_scrollkeeper
%{update_menus}
%update_desktop_database
%endif
%define schemas %name %name-thumbnailer %name-thumbnailer-djvu %{?build_dvi:%name-thumbnailer-dvi} evince-thumbnailer-comics evince-thumbnailer-ps
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f Evince.lang
%defattr(-,root,root,-)
%doc NEWS AUTHORS TODO
# README
%_sysconfdir/gconf/schemas/%name.schemas
%_sysconfdir/gconf/schemas/%name-thumbnailer.schemas
%_sysconfdir/gconf/schemas/%name-thumbnailer-djvu.schemas
%_sysconfdir/gconf/schemas/%name-thumbnailer-comics.schemas
%if %build_dvi
%_sysconfdir/gconf/schemas/%name-thumbnailer-dvi.schemas
%endif
%_sysconfdir/gconf/schemas/%name-thumbnailer-ps.schemas
%{_bindir}/*
%{_datadir}/evince
%{_datadir}/applications/*
%_datadir/icons/hicolor/*/apps/evince*
%dir %_datadir/omf/%name
%_datadir/omf/%name/%name-C.omf
%_mandir/man1/evince.1*
%_libdir/nautilus/extensions-2.0/libevince*so*
%dir %_libdir/evince/1/
%dir %_libdir/evince/1/backends
%_libdir/evince/1/backends/lib*
%_libdir/evince/1/backends/comicsdocument.evince-backend
%_libdir/evince/1/backends/djvudocument.evince-backend
%_libdir/evince/1/backends/dvidocument.evince-backend
%_libdir/evince/1/backends/impressdocument.evince-backend
%_libdir/evince/1/backends/pdfdocument.evince-backend
%_libdir/evince/1/backends/pixbufdocument.evince-backend
%_libdir/evince/1/backends/psdocument.evince-backend
%_libdir/evince/1/backends/tiffdocument.evince-backend

%files -n %libname
%defattr(-,root,root,-)
%_libdir/libevdocument.so.%{major}*
%_libdir/libevview.so.%{major}*

%files -n %develname
%defattr(-,root,root,-)
%doc ChangeLog
%_datadir/gtk-doc/html/evince
%_datadir/gtk-doc/html/libevdocument
%_datadir/gtk-doc/html/libevview
%_libdir/libevdocument.so
%_libdir/libevview.so
%_libdir/*.la
%_libdir/pkgconfig/evince*pc
%_includedir/evince*
