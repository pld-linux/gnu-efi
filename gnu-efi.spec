Summary:	GNU-EFI - building EFI applications using the GNU toolchain
Summary(pl.UTF-8):	GNU-EFI - tworzenie aplikacji EFI przy użyciu narzędzi GNU
Name:		gnu-efi
# NOTE: don't use early 3.1, it doesn't support EFI x86_64
Version:	3.0.13
Release:	1
Epoch:		1
# Intel and HP's BSD-like license, except setjmp code coming from GRUB
License:	BSD-like
Group:		Development/Libraries
Source0:	https://downloads.sourceforge.net/gnu-efi/%{name}-%{version}.tar.bz2
# Source0-md5:	8ec4221f505c78e6fc375c2fd7f0c549
URL:		https://sourceforge.net/projects/gnu-efi/
BuildRequires:	binutils >= 3:2.17.50.0.14
BuildRequires:	gcc >= 6:4.1.1
Requires:	binutils >= 3:2.17.50.0.14
Requires:	gcc >= 6:4.1.1
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ia64 mips64el
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		efi_arch	%(echo %{_target_base_arch} | sed -e 's/i386/ia32/')

%description
GNU-EFI development environment allows to create EFI applications for
IA-64, x86, ARM and MIPS platforms using the GNU toolchain.

%description -l pl.UTF-8
Środowisko programistyczne GNU-EFI umożliwia tworzenie aplikacji EFI
dla platform IA-64, x86, ARM i MIPS przy użyciu narzędzi GNU.

%prep
%setup -q

%build
ARCHFLAGS=
%ifarch ia64
ARCHFLAGS=-frename-registers
%endif
# on x32: use x86_64 EFI ABI
CFLAGS="%{rpmcflags} $ARCHFLAGS" \
%{__make} -j1 \
	ARCH=%{efi_arch} \
%ifarch x32
	ARCH3264=-m64 \
%endif
	CC="%{__cc}" \
	OBJCOPY=objcopy

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ARCH=%{efi_arch} \
	INSTALLROOT=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a apps/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README.*
%{_libdir}/libefi.a
%{_libdir}/libgnuefi.a
%{_libdir}/crt0-efi-*.o
%{_libdir}/elf_*_efi.lds
%{_includedir}/efi
%{_examplesdir}/%{name}-%{version}
