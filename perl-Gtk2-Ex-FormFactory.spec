%define pkgname Gtk2-Ex-FormFactory
%define NVR %{pkgname}-%{version}-%{release}
%define maketest 1
%define upstream_version 0.65

name:      perl-Gtk2-Ex-FormFactory
summary:   Gtk2-Ex-FormFactory - Makes building complex GUI's easy
Version:   %perl_convert_version %upstream_version
release:   %mkrel 2
license:   LGPLv2+
group:     Development/GNOME and GTK+
url:       http://www.exit1.org/download/ff
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

