Summary:	Extracts common modeling concerns from ActiveRecord
Name:		ruby-debug
Version:	0.10.4
Release:	1
License:	Ruby-alike
Source0:	http://rubygems.org/downloads/%{name}-%{version}.gem
# Source0-md5:	e7a0f9a48249a9f525ac60a500ce971c
Source1:	http://rubygems.org/downloads/%{name}-base-%{version}.gem
# Source1-md5:	e71b19d02a490f811bd3b876664c4f0e
Patch0:		%{name}-nogems.patch
Group:		Development/Languages
URL:		http://rubyforge.org/projects/ruby-debug/
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-modules
BuildRequires:	setup.rb = 3.4.1
Requires:	ruby-linecache
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ruby-debug is a debugger for Ruby 1.8. It is faster that the debugger
that ships with Ruby. Some of this debugger is used by many IDEs (from
Eclipse, Aptana, ActiveState or from JRuby).

%package rdoc
Summary:	Documentation files for %{name}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
Documentation files for %{name}.

%package ri
Summary:	ri documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{name}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{name}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{name}.

%prep
%setup -q -c
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
%{__tar} xf %{SOURCE1} -O data.tar.gz | %{__tar} xz
find -newer README  -o -print | xargs touch --reference %{SOURCE0}
mv cli/* lib
cp %{_datadir}/setup.rb .
%patch0 -p1

%build
ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README AUTHORS
%attr(755,root,root) %{_bindir}/rdebug
%{ruby_rubylibdir}/ruby-debug-base.rb
%attr(755,root,root) %{ruby_archdir}/ruby_debug.so
%{ruby_rubylibdir}/ruby-debug.rb
%{ruby_rubylibdir}/ruby-debug

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Debugger
