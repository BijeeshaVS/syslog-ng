%define		mainver		1.6
%define		minorver	5

Summary:	Syslog-ng - new generation of the system logger
Summary(pl):	Syslog-ng - zamiennik syskloga
Summary(pt_BR):	Daemon de log nova gera��o
Name:		syslog-ng
Version:	%{mainver}.%{minorver}
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://www.balabit.hu/downloads/syslog-ng/%{mainver}/src/%{name}-%{version}.tar.gz
# Source0-md5:	ce70b4230e73ad79191618530c8c3a72
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.logrotate
URL:		http://www.balabit.com/products/syslog_ng/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libol-static >= 0.3.14
BuildRequires:	libwrap-devel
PreReq:		rc-scripts >= 0.2.0
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires:	logrotate
Requires:	psmisc >= 20.1
Provides:	syslogdaemon
Obsoletes:	syslog
Obsoletes:	msyslog
Obsoletes:	klogd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
syslog-ng is a syslogd replacement for unix and unix-like systems. It
has been tested on Solaris, BSDi and Linux, and were found to run
reliably. syslog-ng gives you a much enhanced configuration scheme,
which lets you filter messages based on not only priority/facility
pairs, but also on message content. You can use regexps to direct log
stream to different destinations. A destination can be anything from a
simple file to a network connection. syslog-ng supports TCP
logforwarding, together with hashing to prevent unauthorized
modification on the line.

%description -l pl
Syslog-ng jest zamiennikiem dla standardowo u�ywanych program�w typu
sysklog. Dzia�a w systemie SunOS, BSD, Linux. Daje znacznie wi�ksze
mo�liwo�ci logowania i kontrolowania zbieranych informacji.

%description -l pt_BR
Syslog-ng � um substituto para o syslog tradicional, mas com diversas
melhorias, como, por exemplo, a habilidade de filtrar mensagens de log
por seu conte�do (usando express�es regulares) e n�o apenas pelo par
facility/prioridade como o syslog original.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-tcp-wrapper
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d},%{_sysconfdir}/syslog-ng} \
	$RPM_BUILD_ROOT/var/log/{mail,archiv/mail}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog-ng
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/syslog-ng/syslog-ng.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/syslog-ng

> $RPM_BUILD_ROOT/var/log/syslog

%clean
rm -rf $RPM_BUILD_ROOT

%post
for n in /var/log/{cron,daemon,debug,kernel,lpr,maillog,messages,ppp,secure,spooler,syslog,user,mail/{info,warn,err}}
do
	[ -f $n ] && continue
	touch $n
	chmod 640 $n
done

/sbin/chkconfig --add syslog-ng
if [ -f /var/lock/subsys/syslog-ng ]; then
	/etc/rc.d/init.d/syslog-ng restart >&2
else
	echo "Run \"/etc/rc.d/init.d/syslog-ng start\" to start syslog-ng daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/syslog-ng ]; then
		/etc/rc.d/init.d/syslog-ng stop >&2
	fi
	/sbin/chkconfig --del syslog-ng
fi

%files
%defattr(644,root,root,755)
%doc doc/syslog-ng.conf.{demo,sample} doc/sgml/syslog-ng.txt* contrib/syslog-ng.conf.{doc,RedHat}
%attr(750,root,root) %dir %{_sysconfdir}/syslog-ng
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/syslog-ng/syslog-ng.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/syslog-ng
%attr(754,root,root) /etc/rc.d/init.d/syslog-ng
%attr(755,root,root) %{_sbindir}/syslog-ng
%{_mandir}/man[58]/*

%attr(640,root,root) %ghost /var/log/syslog
%dir /var/log/mail
%dir /var/log/archiv
%dir /var/log/archiv/mail
