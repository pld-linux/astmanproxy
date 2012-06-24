#
#
%define		timestamp 20060407-2351
Summary:	Asterisk's manager interface proxy
Name:		astmanproxy
Version:	1.20
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.popvox.com/astmanproxy/%{name}-%{version}-%{timestamp}.tgz
# Source0-md5:	2489f3885436391d75342cf58210da50
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-rpm.patch
URL:		http://www.voip-info.org/tiki-index.php?page=AstManProxy
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The need for a proxy to Asterisk's manager interface has been clear;
almost all GUIs and other interfaces to asterisk implement a proxy of
some kind. Why? A proxy offers:

 - A single persistent connection to asterisk
 - A more secure (non-root) TCP interface
 - Ability to offer filtered input/output
 - Less connections and networking load for asterisk

%prep
%setup -q -cn %{name}-%{version}
%patch0 -p1

%build
cd %{version}
%{__make} astmanproxy \
	rpmcflags="%{rpmcflags}" \
	rpmldflags="%{rpmldflags}"
cp configs/* .

%install
rm -rf $RPM_BUILD_ROOT
cd %{version}
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc %{version}/{README,TODO,VERSIONS}
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_sysconfdir}/asterisk/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
