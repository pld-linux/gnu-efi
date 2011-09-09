Summary:	GNU-EFI - building EFI applications using the GNU toolchain
Summary(pl.UTF-8):	GNU-EFI - tworzenie aplikacji EFI przy użyciu narzędzi GNU
Name:		gnu-efi
# NOTE: don't use 3.1, it doesn't support EFI x86_64
Version:	3.0m
Release:	1
# Intel and HP's BSD-like license, except setjmp code coming from GRUB
License:	GPL v2+ (setjmp code), BSD-like (all the rest)
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/gnu-efi/%{name}_%{version}.orig.tar.gz
# Source0-md5:	d0a21125aee56c0c7291ad260e916cb3
URL:		http://gnu-efi.sourceforge.net/
BuildRequires:	binutils >= 3:2.17.50.0.14
BuildRequires:	gcc >= 6:4.1.1
Requires:	binutils >= 3:2.17.50.0.14
Requires:	gcc >= 6:4.1.1
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia64	-frename-registers

%description
GNU-EFI development environment allows to create EFI applications for
IA-64 and x86 platforms using the GNU toolchain.

%description -l pl.UTF-8
Środowisko programistyczne GNU-EFI umożliwia tworzenie aplikacji EFI
dla platform IA-64 i x86 przy użyciu narzędzi GNU.

%prep
%setup -q -n %{name}-3.0

%build
%ifarch %{x8664}
CFADD=" -DEFI_FUNCTION_WRAPPER -mno-red-zone"
%else
%ifarch ia64
CFADD=" -mfixed-range=f32-f127"
%else
CFADD=
%endif
%endif
%{__make} -j1 \
	ARCH=$(echo %{_target_base_arch} | sed -e 's/i386/ia32/') \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fpic -Wall -fshort-wchar -fno-strict-aliasing -fno-merge-constants -fno-stack-protector$CFADD" \
	OBJCOPY=objcopy

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT%{_prefix}

%if "%{_lib}" != "lib"
	mv -f $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}
%endif

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
