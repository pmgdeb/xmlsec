Summary: Library providing support for "XML Signature" and "XML Encryption" standards
Name: xmlsec
Version: 0.1.0
Release: 1
License: MIT
Group: Development/Libraries
Vendor: Aleksey Sanin <aleksey@aleksey.com>
Distribution:  Aleksey Sanin <aleksey@aleksey.com>
Packager: Aleksey Sanin <aleksey@aleksey.com>
Source: ftp://ftp.aleksey.com/pub/xmlsec/releases/xmlsec-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.aleksey.com/xmlsec
Requires: libxml2 >= 2.4.24
Requires: libxslt >= 1.0.20
Requires: openssl >= 0.9.6
BuildRequires: libxml2-devel >= 2.4.24
BuildRequires: libxslt-devel >= 1.0.20
BuildRequires: openssl-devel >= 0.9.6
Prefix: %{_prefix}
Docdir: %{_docdir}

%description
XML Security Library is a C library based on LibXML2  and OpenSSL. 
The library was created with a goal to support major XML security 
standards "XML Digital Signature" and "XML Encryption". 

%package devel 
Summary: Libraries, includes, etc. to develop applications with XML Digital Signatures and XML Encryption support.
Group: Development/Libraries 
Requires: xmlsec = %{version}
Requires: libxml2-devel >= 2.4.24
Requires: libxslt-devel >= 1.0.20
Requires: openssl-devel >= 0.9.6
Requires: zlib-devel 

%description devel
Libraries, includes, etc. you can use to develop applications with XML Digital 
Signatures and XML Encryption support.

%package nss
Summary: NSS crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec = %{version}
Requires: libxml2 >= 2.4.24
Requires: libxslt >= 1.0.20
Requires: mozilla-nss >= 3.6.0

%description nss
NSS plugin for XML Security Library provides NSS based crypto services
for the xmlsec library

%package nss-devel
Summary: NSS crypto plugin for XML Security Library
Group: Development/Libraries 
Requires: xmlsec = %{version}
Requires: xmlsec-devel = %{version}
Requires: xmlsec-nss = %{version}
Requires: libxml2-devel >= 2.4.24
Requires: libxslt-devel >= 1.0.20
Requires: mozilla-nss-devel >= 3.6.0
Requires: zlib-devel 

%description nss-devel
Libraries, includes, etc. for developing XML Security applications with NSS


%prep
%setup -q

%build
# Needed for snapshot releases.
if [ ! -f configure ]; then
%ifarch alpha
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --host=alpha-redhat-linux --prefix=%prefix --sysconfdir="/etc" --mandir=%{_mandir}
%else
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%prefix --sysconfdir="/etc" --mandir=%{_mandir}
%endif
else
%ifarch alpha
  CFLAGS="$RPM_OPT_FLAGS" ./configure --host=alpha-redhat-linux --prefix=%prefix --sysconfdir="/etc" --mandir=%{_mandir}
%else
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --sysconfdir="/etc" --mandir=%{_mandir}
%endif
fi
if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/include
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
make prefix=$RPM_BUILD_ROOT%{prefix} mandir=$RPM_BUILD_ROOT%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README Copyright
%doc %{_mandir}/man1/xmlsec.1*  

%{prefix}/lib/libxmlsec.so.*
%{prefix}/lib/libxmlsec.so
%{prefix}/lib/libxmlsec-openssl.so.*
%{prefix}/lib/libxmlsec-openssl.so
%{prefix}/bin/xmlsec

%files devel
%defattr(-, root, root)  

%doc AUTHORS ChangeLog NEWS README Copyright
%doc %{_mandir}/man1/xmlsec-config.1*  
%doc docs/* 
%{prefix}/bin/xmlsec-config
%{prefix}/include/xmlsec/*.h
%{prefix}/include/xmlsec/openssl/*.h
%{prefix}/lib/libxmlsec.*a
%{prefix}/lib/libxmlsec-openssl.*a
%{prefix}/lib/pkgconfig/xmlsec.pc

%files nss
%defattr(-, root, root)  

%{prefix}/lib/libxmlsec-nss.so.*
%{prefix}/lib/libxmlsec-nss.so

%files nss-devel
%defattr(-, root, root)  

%{prefix}/include/xmlsec/nss/*.h
%{prefix}/lib/libxmlsec-nss.*a

%changelog
