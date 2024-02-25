%global	oname	Solaar

# don't require because it uses Ayatana Appindicator
%global __requires_exclude  ^typelib\\(AppIndicator3\\).*$

Summary:	Device manager for Logitech's Unifying Receiver
Name:		solaar
Version:	1.1.11
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
# Url:		http://pwr.github.com/Solaar/
Url:		https://github.com/pwr-Solaar/Solaar/releases
Source0:	https://github.com/pwr-Solaar/Solaar/archive/refs/tags/%{version}/%{oname}-%{version}.tar.gz
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pygobject)
BuildRequires:	python%{pyver}dist(pyudev)
BuildRequires:	python%{pyver}dist(psutil)
BuildRequires:	python%{pyver}dist(setuptools)

Requires:	python-gi

BuildArch:	noarch

%description
Solaar is a Linux device manager for Logitech’s Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver, and
for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for
each device, and also pair/unpair supported devices with the receiver.

%files
%doc share/README docs
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
#{_datadir}/%{name}/
%{_datadir}/metainfo/io.github.pwr_solaar.solaar.metainfo.xml
%{_iconsdir}/hicolor/*/apps/%{name}*.{png,svg}
%{python_sitelib}/hidapi/
%{python_sitelib}/keysyms/
%{python_sitelib}/logitech_receiver/
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-*.egg-info
%config %{_udevrulesdir}/42-logitech-unify-permissions.rules

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
%py_build

%install
%py_install

install -pm 0755 -d %{buildroot}%{_udevrulesdir}
install -pm 0644 rules.d/42-logitech-unify-permissions.rules %{buildroot}%{_udevrulesdir}

