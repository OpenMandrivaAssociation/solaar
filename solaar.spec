%define	oname	Solaar

Summary:	Device manager for Logitech's Unifying Receiver
Name:		solaar
Version:	1.1.1
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
# Url:		  http://pwr.github.com/Solaar/
Url:      https://github.com/pwr-Solaar/Solaar
# wget https://github.com/pwr/%{oname}/archive/%{version}.tar.gz -O %{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
Requires:	pyudev
Requires:	python-gi
Requires:	typelib(AppIndicator3)
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
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/*/apps/%{name}.svg
%{python_sitelib}/hidapi/
%{python_sitelib}/logitech_receiver/
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}-*.egg-info
%config %{_udevrulesdir}/42-logitech-unify-permissions.rules

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}%{_udevrulesdir}
cp rules.d/42-logitech-unify-permissions.rules %{buildroot}%{_udevrulesdir}

