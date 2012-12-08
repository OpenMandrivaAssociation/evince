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
Version:	3.6.1
Release:	1
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
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
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	tiff-devel
BuildRequires:	ghostscript kpathsea-devel
BuildRequires:	intltool itstool
#gw if we run autoconf
BuildRequires:	gnome-icon-theme
BuildRequires:	gtk-doc
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
BuildRequires:	kpathsea-devel
#gw just like xdvi, needed for rendering the fonts
Requires:	texlive-xdvi
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
%if %{build_dvi}
	--enable-dvi \
%endif
	--enable-gtk-doc=no \
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

%if %{build_dvi}
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
%{_datadir}/gtk-doc/html/*
%{_libdir}/libevdocument3.so
%{_libdir}/libevview3.so
%{_libdir}/pkgconfig/evince*pc
%{_includedir}/evince*
%{_datadir}/gir-1.0/EvinceDocument-%{gir_major}.gir
%{_datadir}/gir-1.0/EvinceView-%{gir_major}.gir


%changelog
* Tue Oct 30 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.1-1
- update to 3.6.1

* Mon Oct  8 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Fri May 04 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.4.0-11
+ Revision: 796232
- rpmlint fix
- api fix
- api version mismatch fix

  + Matthew Dawkins <mattydaw@mandriva.org>
    - new version 3.4.0

* Wed Feb 29 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.1-1
+ Revision: 781456
- new version 3.2.1

* Sat Dec 24 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.32.0-7
+ Revision: 744966
- more clean ups
- added -lgmodule-2.0 to LIBS linking
- nautilus 3.0 extension dir now
- pcpa ld linker method
- cleaned up spec
- added _disable_ld_no_undefined 1 to hopefully fix last build
- clean up spec for one last build before upgrading to 3.2.x
- added missing BR to fix build
- removed .la files

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix deps
    - rebuilt against libtiff.so.5

* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 2.32.0-6
+ Revision: 677051
- br gconf2
- rebuild

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 2.32.0-5
+ Revision: 669073
- enable dvi
- find with gnome
- enable introspection back
- cleanup spec file
- about to enable dvi backend

* Wed May 04 2011 Funda Wang <fwang@mandriva.org> 2.32.0-4
+ Revision: 665980
- br icon theme
- disable dvi build for now

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild
    - sync with MDVSA-2011:005

* Thu Dec 30 2010 Funda Wang <fwang@mandriva.org> 2.32.0-2mdv2011.0
+ Revision: 626206
- rebuild for new poppler

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581473
- update to new version 2.32.0

* Mon Sep 13 2010 Götz Waschk <waschk@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 578005
- new version
- disable introspection support (b.g.o #629491)

* Tue Aug 17 2010 Götz Waschk <waschk@mandriva.org> 2.31.90-1mdv2011.0
+ Revision: 570900
- new version
- new api and major versions
- drop patch

* Tue Aug 10 2010 Götz Waschk <waschk@mandriva.org> 2.31.6.1-2mdv2011.0
+ Revision: 568299
- fix pkgconfig file

* Thu Aug 05 2010 Götz Waschk <waschk@mandriva.org> 2.31.6.1-1mdv2011.0
+ Revision: 566227
- new version
- update deps
- update file list

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 2.30.3-2mdv2011.0
+ Revision: 563922
- rebuild for new gobject-introspection

* Thu Jun 24 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.3-1mdv2010.1
+ Revision: 549101
- Release 2.30.3

* Tue Jun 22 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.2-1mdv2010.1
+ Revision: 548510
- Release 2.30.2
- Remove patch0 (merged upstream)

* Wed May 05 2010 Götz Waschk <waschk@mandriva.org> 2.30.1-3mdv2010.1
+ Revision: 542634
- don't crash on startup (bug #59093)

* Thu Apr 29 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.30.1-2mdv2010.1
+ Revision: 540828
- rebuild so that shared libraries are properly stripped again

* Mon Apr 26 2010 Götz Waschk <waschk@mandriva.org> 2.30.1-1mdv2010.1
+ Revision: 539223
- update to new version 2.30.1

* Mon Mar 29 2010 Götz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528919
- new version
- update API version

* Wed Mar 10 2010 Götz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 517500
- update to new version 2.29.92

* Mon Feb 22 2010 Götz Waschk <waschk@mandriva.org> 2.29.91-1mdv2010.1
+ Revision: 509695
- new version
- update file list

* Mon Jan 11 2010 Götz Waschk <waschk@mandriva.org> 2.29.5-1mdv2010.1
+ Revision: 489819
- update to new version 2.29.5

* Tue Dec 22 2009 Götz Waschk <waschk@mandriva.org> 2.29.4-1mdv2010.1
+ Revision: 481270
- fix build deps
- new version
- drop patch

* Wed Dec 09 2009 Götz Waschk <waschk@mandriva.org> 2.29.3-1mdv2010.1
+ Revision: 475388
- new version
- update file list

* Thu Oct 22 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.1-1mdv2010.0
+ Revision: 458819
- Release 2.28.1

* Mon Sep 21 2009 Götz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446890
- update to new version 2.28.0

* Wed Aug 12 2009 Götz Waschk <waschk@mandriva.org> 2.27.90-2mdv2010.0
+ Revision: 415268
- move typelib to the library package

* Tue Aug 11 2009 Götz Waschk <waschk@mandriva.org> 2.27.90-1mdv2010.0
+ Revision: 414824
- enable introspection
- update to new version 2.27.90

* Mon Jul 13 2009 Götz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 395645
- update to new version 2.27.4

* Tue Jun 16 2009 Götz Waschk <waschk@mandriva.org> 2.27.3-1mdv2010.0
+ Revision: 386270
- new version

* Tue May 19 2009 Götz Waschk <waschk@mandriva.org> 2.27.1-1mdv2010.0
+ Revision: 377481
- new version
- bump poppler dep
- fix build

* Tue May 19 2009 Götz Waschk <waschk@mandriva.org> 2.26.2-1mdv2010.0
+ Revision: 377446
- update to new version 2.26.2

* Thu Apr 16 2009 Götz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 367597
- update to new version 2.26.1

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 356226
- update to new version 2.26.0

* Tue Mar 03 2009 Götz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 347628
- update to new version 2.25.92

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 341832
- new version
- update the patch

* Tue Feb 03 2009 Götz Waschk <waschk@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 336782
- update build deps
- new version
- update the patch
- new major
- update file list

* Sun Jan 18 2009 Götz Waschk <waschk@mandriva.org> 2.25.5-1mdv2009.1
+ Revision: 331043
- update to the new 2.25.5 tarball
- drop patch 0
- new version
- fix build
- update file list

* Tue Jan 06 2009 Götz Waschk <waschk@mandriva.org> 2.25.4-1mdv2009.1
+ Revision: 325442
- fix build deps
- update to new version 2.25.4

* Tue Dec 02 2008 Götz Waschk <waschk@mandriva.org> 2.25.2-1mdv2009.1
+ Revision: 309078
- update to new version 2.25.2

* Sun Nov 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.25.1-2mdv2009.1
+ Revision: 301480
- rebuilt against new libxcb

* Wed Nov 05 2008 Götz Waschk <waschk@mandriva.org> 2.25.1-1mdv2009.1
+ Revision: 300143
- update to new version 2.25.1

* Tue Oct 21 2008 Götz Waschk <waschk@mandriva.org> 2.24.1-1mdv2009.1
+ Revision: 295929
- update to new version 2.24.1

* Tue Sep 23 2008 Götz Waschk <waschk@mandriva.org> 2.24.0-1mdv2009.0
+ Revision: 287289
- new version

* Wed Sep 10 2008 Götz Waschk <waschk@mandriva.org> 2.23.92-1mdv2009.0
+ Revision: 283407
- new version

* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 2.23.91-2mdv2009.0
+ Revision: 282359
- Rebuild for new djvulibre

* Mon Sep 01 2008 Götz Waschk <waschk@mandriva.org> 2.23.91-1mdv2009.0
+ Revision: 278649
- new version
- update build deps

* Wed Aug 06 2008 Götz Waschk <waschk@mandriva.org> 2.23.6-1mdv2009.0
+ Revision: 265076
- new version
- drop patch

* Tue Jul 22 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-2mdv2009.0
+ Revision: 240249
- fix mime types in desktop file
- remove obsolete configure option

* Tue Jul 22 2008 Götz Waschk <waschk@mandriva.org> 2.23.5-1mdv2009.0
+ Revision: 240054
- new version

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 2.23.4-1mdv2009.0
+ Revision: 231093
- new version
- update license
- fix buildrequires

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 29 2008 Götz Waschk <waschk@mandriva.org> 2.22.2-1mdv2009.0
+ Revision: 212896
- new version

* Wed Apr 30 2008 Götz Waschk <waschk@mandriva.org> 2.22.1.1-2mdv2009.0
+ Revision: 199718
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - better description

* Wed Apr 09 2008 Götz Waschk <waschk@mandriva.org> 2.22.1.1-1mdv2009.0
+ Revision: 192476
- new version

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 2.22.0-1mdv2008.1
+ Revision: 183812
- new version

* Tue Feb 12 2008 Götz Waschk <waschk@mandriva.org> 2.21.91-1mdv2008.1
+ Revision: 165760
- new version
- drop patches

* Fri Feb 08 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-3mdv2008.1
+ Revision: 164100
- fix pdf thumbnailer (bug #37527)

* Tue Jan 29 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-2mdv2008.1
+ Revision: 159830
- build with libspectre

* Tue Jan 29 2008 Götz Waschk <waschk@mandriva.org> 2.21.90-1mdv2008.1
+ Revision: 159682
- new version
- add library package

* Tue Jan 22 2008 Götz Waschk <waschk@mandriva.org> 2.21.1-5mdv2008.1
+ Revision: 156463
- fix nautilus extensions dir

* Fri Jan 18 2008 Götz Waschk <waschk@mandriva.org> 2.21.1-4mdv2008.1
+ Revision: 154640
- suggest tetex for rendering dvi files
- readd patch for linking static libkpathsea from tetex

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2.21.1-3mdv2008.1
+ Revision: 148473
- rebuild
- do not package big ChangeLog

* Tue Jan 08 2008 Götz Waschk <waschk@mandriva.org> 2.21.1-2mdv2008.1
+ Revision: 146810
- drop patch
- build with kpathsea from texlive

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Funda Wang <fwang@mandriva.org>
    - desktop-file-install is not needed any more
    - drop old menu

* Tue Dec 04 2007 Götz Waschk <waschk@mandriva.org> 2.21.1-1mdv2008.1
+ Revision: 115209
- new version
- rediff patch 1
- drop patch 2

* Tue Nov 27 2007 Götz Waschk <waschk@mandriva.org> 2.20.2-1mdv2008.1
+ Revision: 113313
- new version

* Wed Oct 24 2007 Pascal Terjan <pterjan@mandriva.org> 2.20.1-3mdv2008.1
+ Revision: 101853
- Fix encoding in the patch

* Wed Oct 24 2007 Pascal Terjan <pterjan@mandriva.org> 2.20.1-2mdv2008.1
+ Revision: 101851
- Allow opening links which does not contain :// (like mailto:)

* Tue Oct 16 2007 Götz Waschk <waschk@mandriva.org> 2.20.1-1mdv2008.1
+ Revision: 98883
- new version
- drop patch 2

* Fri Oct 05 2007 Frederic Crozat <fcrozat@mandriva.com> 2.20.0-2mdv2008.0
+ Revision: 95624
- Patch2 (SVN): various fixes from SVN, mostly for forms

* Mon Sep 17 2007 Götz Waschk <waschk@mandriva.org> 2.20.0-1mdv2008.0
+ Revision: 89328
- new version
- drop patch 0
- fix buildrequires

* Tue Sep 04 2007 Götz Waschk <waschk@mandriva.org> 2.19.92-1mdv2008.0
+ Revision: 79072
- new version
- bump poppler dep
- patch to fix mime list in desktop file generation

* Tue Aug 28 2007 Götz Waschk <waschk@mandriva.org> 2.19.4-1mdv2008.0
+ Revision: 72445
- fix buildrequires
- new version

* Thu Aug 09 2007 Frederic Crozat <fcrozat@mandriva.com> 0.9.3-2mdv2008.0
+ Revision: 60748
- Fix build with latest intltool
- Remove dependency on libgnomeprint, use gtk+ print support instead

* Mon Jul 30 2007 Götz Waschk <waschk@mandriva.org> 0.9.3-1mdv2008.0
+ Revision: 56704
- fix buildrequires
- new version

* Tue Jul 10 2007 Götz Waschk <waschk@mandriva.org> 0.9.2-1mdv2008.0
+ Revision: 50883
- new version
- fix buildrequires

* Tue Jun 19 2007 Götz Waschk <waschk@mandriva.org> 0.9.1-1mdv2008.0
+ Revision: 41427
- new version
- bump deps

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 0.9.0-2mdv2008.0
+ Revision: 36151
- rebuild with correct optflags

  + Götz Waschk <waschk@mandriva.org>
    - new version

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 0.8.1-1mdv2008.0
+ Revision: 14559
- fix file list
- fix schemas list
- new version

