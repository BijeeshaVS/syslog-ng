Summary:	Syslog-ng - new generation of the system logger
Summary(pl):	Syslog-ng - zamiennik syskloga
Name:		syslog-ng
Version:	1.4.12
Release:	2
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://www.balabit.hu/downloads/syslog-ng/1.4/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.logrotate
Patch0:		%{name}-autoconf.patch
URL:		http://www.balabit.hu/products/syslog-ng/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libol-static >= 0.2.21
BuildRequires:	flex
Prereq:		rc-scripts >= 0.2.0
Prereq:		/sbin/chkconfig
Requires:	logrotate
Requires:	fileutils
Requires:	psmisc >= 20.1
Provides:	syslogdaemon
Obsoletes:	syslog
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

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
Syslog-ng jest zamiennikiem dla standartowo u�ywanych program�w typu
sysklog. Dzia�a w systemie SunOS, BSD, Linux. Daje znacznie wi�ksze
mo�liwo�ci logowania i kontrolowania zbieranych informacji.

%prep
%setup -q
%patch -p1

%build
aclocal
autoconf
automake -a -c
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sysconfdir}/{syslog-ng,logrotate.d}} \
	$RPM_BUILD_ROOT/var/log/{archiv,}/{news,mail}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/syslog-ng
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/syslog-ng/syslog-ng.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/syslog-ng

gzip -9nf doc/syslog-ng.conf.{demo,sample} doc/sgml/syslog-ng.txt \

touch $RPM_BUILD_ROOT/var/log/syslog

%clean
rm -rf $RPM_BUILD_ROOT

%post
for n in /var/log/{kernel,messages,secure,maillog,spooler,debug,cron,syslog,daemon,lpr,user,ppp,mail/{info,warn,err}}
do
	[ -f $n ] && continue
	touch $n
	chmod 640 $n
done

/sbin/chkconfig --add syslog-ng
if [ -f /var/lock/subsys/syslog-ng ]; then
	/etc/rc.d/init.d/syslog-ng restart &>/dev/null
else
	echo "Run \"/etc/rc.d/init.d/syslog-ng start\" to start syslog-ng daemon."
fi
if [ -f /var/lock/subsys/klogd ]; then
	/etc/rc.d/init.d/klogd restart 1>&2
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
%doc doc/*.gz doc/sgml/syslog-ng.txt*
%attr(750,root,root) %dir %{_sysconfdir}/syslog-ng
%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/syslog-ng/syslog-ng.conf
%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/logrotate.d/syslog-ng
%attr(754,root,root) /etc/rc.d/init.d/syslog-ng
%attr(755,root,root) %{_sbindir}/syslog-ng
%{_mandir}/man[58]/*

%attr(640,root,root) %ghost /var/log/syslog
%attr(750,root,root) %ghost /var/log/news
%attr(750,root,root) %dir /var/log/mail
%attr(750,root,root) %dir /var/log/archiv/mail
