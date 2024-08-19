Name:           fedora-distro-aliases
Version:        1.4
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
* Tue Aug 20 2024 Jakub Kadlcik <frostyx@email.cz> 1.4-1
- Add an attribute with always numeric version number (frostyx@email.cz)

* Sat Feb 24 2024 Jakub Kadlcik <frostyx@email.cz> 1.3-1
- Make sure everything behaves correctly during the branching window
  (frostyx@email.cz)
- Add releasers.conf (frostyx@email.cz)

* Tue Jan 23 2024 Jakub Kadlcik <frostyx@email.cz> 1.2-1
- Drop bodhi-client dependency (frostyx@email.cz)
- Add installation instructions (frostyx@email.cz)
- Show how to get only version numbers (frostyx@email.cz)

* Sat Jan 13 2024 Jakub Kadlcik <frostyx@email.cz> 1.1-1
- Fix Source URL (frostyx@email.cz)
- Unify descriptions and mention querying bodhi (frostyx@email.cz)
- Link fedfind project (frostyx@email.cz)
- make repository REUSE compliant (msuchy@redhat.com)

* Tue Jan 09 2024 Jakub Kadlcik <frostyx@email.cz> - 1.0-1
- Initial package
