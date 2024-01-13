Name:           fedora-distro-aliases
Version:        1.1
Release:        1%{?dist}
Summary:        Aliases for active Fedora releases

License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/fedora-distro-aliases
Source:         %{URL}/archive/%{name}-%{version}-1/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%generate_buildrequires
%pyproject_buildrequires


%global _description %{expand:
Some projects such as Tito, Packit,
Fedora Review Service, etc operate over currently active Fedora releases.
They can use this package to find their version numbers instead of manually
defining a list.

This package queries Bodhi to find the active releases and therefore requires an
internet connection.}

%description %_description

%package -n     python3-fedora-distro-aliases
Summary:        %{summary}

%description -n python3-fedora-distro-aliases %_description


%prep
%autosetup -p1 -n fedora-distro-aliases-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files fedora_distro_aliases


%check
%pyproject_check_import -t
%{python3} -m pytest -vv


%files -n python3-fedora-distro-aliases -f %{pyproject_files}
%license LICENSES/GPL-2.0-or-later.txt
%doc README.md


%changelog
* Sat Jan 13 2024 Jakub Kadlcik <frostyx@email.cz> 1.1-1
- Fix Source URL (frostyx@email.cz)
- Unify descriptions and mention querying bodhi (frostyx@email.cz)
- Link fedfind project (frostyx@email.cz)
- make repository REUSE compliant (msuchy@redhat.com)

* Tue Jan 09 2024 Jakub Kadlcik <frostyx@email.cz> - 1.0-1
- Initial package
