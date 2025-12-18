%global	oname	Solaar
%global	app_id	io.github.pwr_solaar.solaar
# don't require because it uses Ayatana Appindicator
%global	__requires_exclude	^typelib\\(AppIndicator3\\).*$

%bcond tests 1

Name:		solaar
Version:	1.1.18
Release:	1
License:	GPL-2.0-or-later
Summary:	Device manager for Logitech's Unifying Receiver
Group:		System/Hardware
URL:		https://github.com/pwr-Solaar/Solaar/releases
Source0:	https://github.com/pwr-Solaar/Solaar/archive/refs/tags/%{version}/%{oname}-%{version}.tar.gz
# Patches for 1.1.18, should be resolved in next upstream release
Patch0:		https://github.com/pwr-Solaar/Solaar/pull/3070/commits/f5872095e64ab51b95c72c6b0d890e36128491be.patch#/1.1.18.fix-crash-when-reading-notification-flags.patch
Patch1:		https://github.com/pwr-Solaar/Solaar/pull/3078/commits/d92b3a68b3d9dd6452132d4ef5c665bc95c04d33.patch#/1.1.18.fix-bug-when-showing-details-about-direct-connected-device.patch
Patch2:		https://github.com/pwr-Solaar/Solaar/pull/3082/commits/b0fc8d9f4d12f2346794704f0a1bacc107e6c78b.patch#/1.1.18.add-new-lightspeed-reciever.patch

BuildRequires:	appstream
BuildRequires:	appstream-util
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	hicolor-icon-theme
BuildRequires:	pkgconfig(appstream)
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(pygobject-3.0)
BuildRequires:	python%{pyver}dist(dbus-python)
BuildRequires:	python%{pyver}dist(evdev) >= 1.1.2
BuildRequires:	python%{pyver}dist(hid-parser)
BuildRequires:	python%{pyver}dist(psutil) >= 5.4.3
BuildRequires:	python%{pyver}dist(pygobject)
BuildRequires:	python%{pyver}dist(python-xlib) >= 0.27
BuildRequires:	python%{pyver}dist(pyudev) >= 0.13
BuildRequires:	python%{pyver}dist(pyyaml) >= 3.12
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(typing-extensions)
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-mock)
%endif

Requires:	python%{pyver}dist(evdev)
Requires:	python%{pyver}dist(pygobject)
Requires:	python%{pyver}dist(pyudev)


BuildArch:	noarch

%description
Solaar is a Linux device manager for Logitech’s Unifying Receiver
peripherals. It is able to pair/unpair devices to the receiver, and
for most devices read battery status.

It comes in two flavors, command-line and GUI. Both are able to list
the devices paired to a Unifying Receiver, show detailed info for
each device, and also pair/unpair supported devices with the receiver.


%prep
%autosetup -n %{oname}-%{version} -p1

%build
%py_build
# build translations
tools/po-compile.sh

%install
%py_install

# Remove pointless shebangs
sed -i -e '1d' %{buildroot}/%{python3_sitelib}/solaar/{gtk,tasks}.py

# install hidconsole
install -pm755 tools/hidconsole %{buildroot}%{_bindir}
# Fix shebang line
sed -i -e '1s,^#!.*$,#!/usr/bin/python3,' %{buildroot}/%{_bindir}/hidconsole

# install desktop files
desktop-file-install --dir %{buildroot}/%{_datadir}/applications share/applications/solaar.desktop
desktop-file-install --dir %{buildroot}%{_sysconfdir}/xdg/autostart share/autostart/solaar.desktop

# install metainfo
install -Dpm644 share/solaar/%{app_id}.metainfo.xml %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml
appstreamcli validate --no-net --explain %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

# install udev rules
install -Dpm 0644 rules.d/42-logitech-unify-permissions.rules %{buildroot}%{_udevrulesdir}/42-logitech-unify-permissions.rules

# install translations
for dir in share/locale/* ; do
    lang=$(basename $dir)
    install -dm755 %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
    install -pm644 $dir/LC_MESSAGES/solaar.mo %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
done

ln -s solaar %{buildroot}%{_bindir}/solaar-cli

# We use the system package
rm -rf %{buildroot}%{python3_sitelib}/hid_parser
# We do not need generate keysymdef.py
rm -f %{buildroot}%{python3_sitelib}/keysyms/__pycache__/generate*.pyc
rm -f %{buildroot}%{python3_sitelib}/keysyms/generate.py

%find_lang %{name}

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
export GI_TYPELIB_PATH=%{_prefix}/%{_lib}/girepository-1.0
# run pytest but skip show tests as desktop notification tests dont work in CI
pytest -v -rs tests/ -k "not test_show"
%endif

%posttrans
# This is needed to apply permissions to existing devices when the package is
# installed.
# Skip triggering udevd when it is not accessible, e.g. containers or
# rpm-ostree-based systems.
if [ -S /run/udev/control ]; then
    /usr/bin/udevadm trigger --subsystem-match=hidraw --action=add
fi

%files -f %{name}.lang
%license LICENSE.txt
%doc share/README COPYRIGHT
%{_bindir}/%{name}*
%{_bindir}/hidconsole
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{app_id}.metainfo.xml
%{_iconsdir}/hicolor/*/apps/%{name}*.{png,svg}
%{python_sitelib}/hidapi/
%{python_sitelib}/keysyms/
%{python_sitelib}/logitech_receiver/
%{python_sitelib}/%{name}/
%{python_sitelib}/%{name}-%{version}.*-info
%config %{_udevrulesdir}/42-logitech-unify-permissions.rules
%config(noreplace) %{_sysconfdir}/xdg/autostart/solaar.desktop
