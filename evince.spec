%define build_dvi 1

Summary: GNOME Document viewer
Name:    evince
Version: 2.20.0
Release: %mkrel 2
License: GPL
Group:   Graphical desktop/GNOME
URL:     http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch1: evince-kpathsea-link.patch
# (fc) 2.20.0-2mdv various fixes from SVN, mostly for forms (SVN)
Patch2: evince-2.20.0-svnfixes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: ghostscript ghostscript-module-X
BuildRequires: libglade2.0-devel
BuildRequires: libgnomeui2-devel
BuildRequires: libxt-devel
BuildRequires: libpoppler-glib-devel >= 0.6
BuildRequires: nautilus-devel
BuildRequires: libtiff-devel
BuildRequires: libxslt-proc
#BuildRequires: t1lib-devel
%if %build_dvi
BuildRequires: tetex-devel >= tetex-devel-3.0-22mdv
%endif
BuildRequires: djvulibre-devel >= 3.5.17
BuildRequires: scrollkeeper
BuildRequires: ghostscript
BuildRequires: perl-XML-Parser
#gw if we run autoconf
BuildRequires: gnome-doc-utils
BuildRequires: gnome-common
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires:	desktop-file-utils
BuildRequires: libgcrypt-devel
Requires(post): scrollkeeper desktop-file-utils
Requires(postun): scrollkeeper desktop-file-utils

%description
GNOME Document viewer, supports PDF and PostScript.

%prep
%setup -q
%if %build_dvi
%patch1 -p1 -b .makefile
%endif
%patch2 -p1 -b .svnfixes
intltoolize --copy --force
aclocal
autoconf
automake

%build
%configure2_5x --enable-print=gtk --enable-tiff --enable-djvu --enable-pixbuf --enable-comics \
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

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF >  $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{_bindir}/%name" icon="publishing_section.png" needs="x11" title="Document Viewer" longtitle="View PDF or PS files" section="Office/Publishing" startup_notify="true" mimetypes="application/pdf;application/postscript;application/x-gzpostscript;application/x-dvi;image/tiff;image/vnd.djvu" accept_url="true" multiple_files="true" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Publishing" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*




rm -f %buildroot%_libdir/nautilus/extensions-*/libevince*a

%post
%update_scrollkeeper
%{update_menus}
%update_desktop_database
%define schemas %name %name-thumbnailer %name-thumbnailer-djvu %{?build_dvi:%name-thumbnailer-dvi} evince-thumbnailer-comics evince-thumbnailer-ps
%post_install_gconf_schemas %schemas
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%clean_scrollkeeper
%{clean_menus}
%clean_desktop_database
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f Evince.lang
%defattr(-,root,root,-)
%doc ChangeLog NEWS AUTHORS TODO
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
%_datadir/gtk-doc/html/evince/
%_mandir/man1/evince.1*
%_libdir/nautilus/extensions-*/libevince*so*
%{_menudir}/*
