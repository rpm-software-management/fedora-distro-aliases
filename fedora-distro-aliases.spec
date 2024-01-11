Name:           fedora-distro-aliases
Version:        1.0
Release:        1%{?dist}
Summary:        Aliases for active Fedora releases

License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/fedora-distro-aliases
Source:         %{URL}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel

%generate_buildrequires
%pyproject_buildrequires


%global _description %{expand:
Some projects such as Tito, Packit, Fedora Review Service, etc operate over
currently active Fedora releases. They either need to manualy define them
in a list or implement a code similar to this.}


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
* Tue Jan 09 2024 Jakub Kadlcik <frostyx@email.cz> - 1.0-1
- Initial package
