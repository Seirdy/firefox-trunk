AutoReqProv: no

##Init variables

%global currenf 46.0a1
%global _optdir /opt
%global packver 0.7
%ifarch x86_64
%global arch x86_64
%else
%global arch i686
%endif

##Package Version and Licences

Summary: Firefox Nightly RPM Builds
Name: firefox-trunk
Version: 46
Release: 0a1_%{packver}%{?dist}
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Applications/Internet
URL: http://www.nightly.mozilla.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

##DEPS
BuildRequires: wget tar

Requires: alsa-lib libX11 libXcomposite libXdamage libnotify libXt libXext glib2 dbus-glib libjpeg-turbo cairo-gobject libffi fontconfig freetype libgcc gtk3 gtk2 hunspell zlib
Requires: nspr >= 4.10.8
Requires: nss >= 3.19.2
Requires: sqlite >= 3.8.10.2
Conflicts: firefox-46 >= 46-0a1_0.1

##Description for Package

%description
This package is a package built directly from Mozilla's nightly tarball. This package will be updated weekly if not sooner.

%prep

##Build Instructions

%build
wget -c --no-check-certificate -P %{_builddir} https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.en-US.linux-%{arch}.tar.bz2
tar -jxvf firefox-%{currenf}.en-US.linux-*.tar.bz2  -C %{_builddir}

## Install Instructions

%install

install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/128x128/apps},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-trunk/browser/defaults/preferences/

install -m644 %{_builddir}/firefox/browser/icons/mozicon128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/firefox-trunk.png

cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-trunk/
ln -s /opt/firefox-trunk/firefox %{buildroot}/usr/bin/firefox-trunk

cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF

## Desktop File

[Desktop Entry]
Version=46.0a1
Name=Nightly
GenericName=Firefox Nightly
Comment=Browse the Web
Exec=firefox-trunk %u
Icon=firefox-trunk.png
Terminal=false
Type=Application
MimeType=text/html;text/xml;application/xhtml+xml;application/vnd.mozilla.xul+xml;text/mml;x-scheme-handler/http;x-scheme-handler/https;
Categories=Network;WebBrowser;
Keywords=web;browser;internet;
EOF
## Disable Update Alert
echo '// Disable Update Alert
pref("app.update.enabled", false);' > %{buildroot}/opt/firefox-trunk/browser/defaults/preferences/vendor.js

##Cleanup

%clean
rm -rf $RPM_BUILD_ROOT

##Installed Files

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/icons//hicolor/128x128/apps/%{name}.png
%{_optdir}/firefox-trunk/
