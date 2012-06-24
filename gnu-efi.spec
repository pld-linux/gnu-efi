Summary:	GNU-EFI - building EFI applications using the GNU toolchain
Summary(pl.UTF-8):	GNU-EFI - tworzenie aplikacji EFI przy użyciu narzędzi GNU
Name:		gnu-efi
Version:	3.0c
Release:	1
# efilib is on Intel's BSD-like license, HP's glue code is GPL'd
License:	GPL v2+, portions on Intel's BSD-like license (see README.*)
Group:		Development/Libraries
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/%{name}-%{version}.tar.gz
# Source0-md5:	823e5f04d1c0a7b88831f91fbf12d470
BuildRequires:	binutils >= 2.11
BuildRequires:	gcc >= 5:3.0
Requires:	binutils >= 2.11
Requires:	gcc >= 5:3.0
ExclusiveArch:	%{ix86} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia64	-frename-registers

%description
GNU-EFI development environment allows to create EFI applications for
IA-64 and x86 platforms using the GNU toolchain.

%description -l pl.UTF-8
Środowisko programistyczne GNU-EFI umożliwia tworzenie aplikacji EFI
dla platform IA-64 i x86 przy użyciu narzędzi GNU.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fpic -Wall -fshort-wchar"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT%{_prefix}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a apps/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README.*
%{_libdir}/lib*efi.a
%{_libdir}/crt0-efi-*.o
%{_libdir}/elf_*_efi.lds
%{_includedir}/efi
%{_examplesdir}/%{name}-%{version}
