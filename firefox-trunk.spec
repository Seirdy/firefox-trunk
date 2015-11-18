AutoReqProv: no

##Init variables

%global currenf 45.0a1
%global _optdir /opt
%global packver 0.3
%ifarch x86_64
%global arch x86_64
%else
%global arch i686
%endif

##Package Version and Licences

Summary: Firefox Nightly RPM Builds
Name: firefox-trunk
Version: 45
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

##Description for Package

%description
This package is a package built directly from Mozilla's nightly tar. This package will be updated weekly if not sooner

%prep

##Build Instructions

%build
wget -c --no-check-certificate -P %{_builddir} https://ftp.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.en-US.linux-%{arch}.tar.bz2
wget -c --no-check-certificate -P %{_builddir} http://i.imgur.com/bK15O3i.png
tar -jxvf firefox-%{currenf}.en-US.linux-*.tar.bz2  -C %{_builddir}

## Install Instructions

%install

install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/48x48/apps},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-trunk/browser/defaults/preferences/

install -m644 %{_builddir}/bK15O3i.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/firefox-trunk.png

cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-trunk/
ln -s /opt/firefox-trunk/firefox %{buildroot}/usr/bin/firefox-trunk

cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF

## Desktop File

[Desktop Entry]
Version=45.0a1
Name=Firefox Nightly
GenericName=Web Browser
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
%{_datadir}/icons//hicolor/48x48/apps/%{name}.png
%{_optdir}/firefox-trunk/
