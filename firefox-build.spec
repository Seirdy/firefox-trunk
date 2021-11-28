AutoReqProv: no

##Init variables

%global currenf 96
%global _optdir /opt
%global arch x86_64


##Package Version and Licences

Summary: "This package is built directly from Mozilla's nightly tarball."
Name: firefox-trunk
Version: %{currenf}
Release: 0a1_%(date +%%Y%%m%%d)_%(date +%%H%%M)%{?dist}
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Applications/Internet
URL: https://www.nightly.mozilla.org/

ExclusiveArch: %{arch}

Source0: https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.0a1.en-US.linux-%{arch}.tar.bz2
Source1: https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.0a1.en-US.linux-%{arch}.checksums

##DEPS
BuildRequires: wget tar

Requires: alsa-lib libX11 libXcomposite libXcursor libXdamage libXext libXfixes libXi libXrandr libXrender atk cairo-gobject cairo dbus dbus-glib fdk-aac-free libffi fontconfig freetype libgcc gtk3 gdk-pixbuf2 harfbuzz pango libxcb zlib p11-kit-trust pciutils-libs
Requires: nspr >= 4.26
Requires: nss >= 3.70

##Description for Package

%description
"This package is a package built directly from Mozilla's nightly tarball."

%prep

wget -O firefox-%{currenf}.0a1.en-US.linux-%{arch}.tar.bz2 -P %{_builddir} https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.0a1.en-US.linux-%{arch}.tar.bz2
wget -O firefox-%{currenf}.0a1.en-US.linux-%{arch}.checksums -P %{_builddir} https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.0a1.en-US.linux-%{arch}.checksums

if grep -q -w $(sha512sum %{_builddir}/firefox-%{currenf}.0a1.en-US.linux-%{arch}.tar.bz2) %{_builddir}/firefox-%{currenf}.0a1.en-US.linux-%{arch}.checksums; then
    exit 0
else
    echo "Checksum verification error."
    exit -1
fi

%build
tar -jxvf firefox-%{currenf}.0a1.en-US.linux-%{arch}.tar.bz2 -C %{_builddir}

## Install Instructions

%install

install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/128x128/apps},opt}
install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/64x64/apps},opt}
install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/48x48/apps},opt}
install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/32x32/apps},opt}
install -dm 755 %{buildroot}/usr/{bin,share/{applications,icons/hicolor/16x16/apps},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-trunk/browser/defaults/preferences/

install -m 644 %{_builddir}/firefox/browser/chrome/icons/default/default128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/firefox-trunk.png
install -m 644 %{_builddir}/firefox/browser/chrome/icons/default/default64.png %{buildroot}/usr/share/icons/hicolor/64x64/apps/firefox-trunk.png
install -m 644 %{_builddir}/firefox/browser/chrome/icons/default/default48.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/firefox-trunk.png
install -m 644 %{_builddir}/firefox/browser/chrome/icons/default/default32.png %{buildroot}/usr/share/icons/hicolor/32x32/apps/firefox-trunk.png
install -m 644 %{_builddir}/firefox/browser/chrome/icons/default/default16.png %{buildroot}/usr/share/icons/hicolor/16x16/apps/firefox-trunk.png

cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-trunk/
ln -s /opt/firefox-trunk/firefox %{buildroot}/usr/bin/firefox-trunk

cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF

## Desktop File

[Desktop Entry]
Version=%{currenf}.0a1
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

cat > %{buildroot}/%{_datadir}/applications/%{name}-safemode.desktop << EOF

## Safe Mode Desktop File

[Desktop Entry]
Version=%{currenf}.0a1
Name=Nightly - Safe Mode
GenericName=Firefox Nightly - Safe Mode
Comment=Browse the Web in safe mode
Exec=firefox-trunk -safe-mode %u
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

##Installed Files
%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_optdir}/firefox-trunk/

##Changes

%changelog
* Wed Nov 10 2021 Jack Greiner <jack@emoss.org> 96-0a1_211110
- Updated dependencies
- Added checksum verification for downloads
- Simplified specfile.
* Wed Oct 31 2018 Jack Greiner <jack@emoss.org> 64-0a1_181031
- Fixed icon paths
- Cleaned up some unnecessary commands in build
- Re-added a safemode desktop extension
- Updated for Release 64.0a1
