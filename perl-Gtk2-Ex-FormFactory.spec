%define pkgname Gtk2-Ex-FormFactory
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1
%define upstream_version 0.67

name:      perl-Gtk2-Ex-FormFactory
summary:   Gtk2-Ex-FormFactory - Makes building complex GUI's easy
Version:   %perl_convert_version %upstream_version
release:   %mkrel 2
license:   LGPLv2+
group:     Development/GNOME and GTK+
url:       https://www.exit1.org/download/ff
buildroot: %{_tmppath}/%{name}-%{version}-%(id -u -n)
buildarch: noarch
source:    http://www.exit1.org/packages/Gtk2-Ex-FormFactory/dist/Gtk2-Ex-FormFactory-%upstream_version.tar.bz2
BuildRequires: perl-Gtk2 perl-devel

%description
This is a framework which tries to make building complex GUI's easy, by
offering these two main features:

  * Consistent looking GUI without the need to code resp. tune
    each widget by hand. Instead you declare the structure of your
    GUI, connect it to the data of your program (which should be
    a well defined set of objects) and control how this structure
    is transformed into a specific layout in a very generic way.

  * Automatically keep widget and object states in sync (in both
    directions), even with complex data structures with a lot of
    internal dependencies, object nesting etc.

This manpage describes the facilities of Gtk2::Ex::FormFactory objects
which are only a small part of the whole framework. To get a full
introduction and overview of how this framework works refer to
Gtk2::Ex::FormFactory::Intro.

%prep
%setup -q -n %{pkgname}-%{upstream_version} 
chmod -R u+w %{_builddir}/%{pkgname}-%{upstream_version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=%{buildroot}%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '` INSTALLDIRS=vendor
%make
%if %maketest
%{__make} test
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%{makeinstall} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=%{buildroot}%{_prefix}| : qq|DESTDIR=%{buildroot}| '`

# remove special files
find %{buildroot} -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

# no empty directories
find %{buildroot}%{_prefix}             \
    -type d -depth                      \
    -exec rmdir {} \; 2>/dev/null


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes README
%perl_vendorlib/Gtk2/Ex/
%_mandir/man3/Gtk2::Ex*



%changelog
* Fri Jan 20 2012 Götz Waschk <waschk@mandriva.org> 0.670.0-2mdv2012.0
+ Revision: 763023
- rebuild

* Sun Aug 14 2011 Götz Waschk <waschk@mandriva.org> 0.670.0-1
+ Revision: 694477
- update to new version 0.67

* Tue Jul 26 2011 Götz Waschk <waschk@mandriva.org> 0.650.0-2
+ Revision: 691695
- rebuild

* Tue Jul 28 2009 Götz Waschk <waschk@mandriva.org> 0.650.0-1mdv2011.0
+ Revision: 401498
- use perl version macro
- update license

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 0.65-1mdv2009.0
+ Revision: 135846
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sun Jul 02 2006 Götz Waschk <waschk@mandriva.org> 0.65-1mdv2007.0
- New release 0.65

* Sun Jun 18 2006 Götz Waschk <waschk@mandriva.org> 0.64-1mdk
- New release 0.64

* Mon Apr 24 2006 Götz Waschk <waschk@mandriva.org> 0.63-1mdk
- New release 0.63

* Mon Apr 10 2006 Götz Waschk <waschk@mandriva.org> 0.62-1mdk
- New release 0.62

* Mon Apr 03 2006 Götz Waschk <waschk@mandriva.org> 0.61-1mdk
- New release 0.61

* Tue Mar 28 2006 Götz Waschk <waschk@mandriva.org> 0.60-1mdk
- New release 0.60

* Thu Dec 29 2005 Götz Waschk <waschk@mandriva.org> 0.59-1mdk
- New release 0.59

* Fri Nov 04 2005 Götz Waschk <waschk@mandriva.org> 0.58-2mdk
- fix dir (Anssi Hannuta)

* Sun Oct 09 2005 Götz Waschk <waschk@mandriva.org> 0.58-1mdk
- New release 0.58

* Tue Aug 02 2005 Götz Waschk <waschk@mandriva.org> 0.57-1mdk
- new version

* Mon Jul 25 2005 Götz Waschk <waschk@mandriva.org> 0.56-1mdk
- Initial build.

