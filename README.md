# WindowsXP Plymouth Theme

A Windows XP-inspired Plymouth boot splash theme for Linux.

This theme recreates the classic Windows XP boot experience using a custom background, loading-bar frame, and animated loading blocks.

> **Windows XP boot animation, now running on Linux.**
>
> Because apparently we weren't done with that era yet.

---

## Preview

<img width="1920" height="1080" alt="WindowsXP-preview" src="https://github.com/user-attachments/assets/0a598200-680b-43ce-bd63-b4f6ad23e871" />


The theme recreates the classic Windows XP boot screen with:

* Windows XP logo and background
* Microsoft branding
* Classic loading-bar frame
* Three-block animated loading indicator
* 80 ms animation interval
* 80 ms pause between animation loops
* Centered layout
* Black background
* Resolution-independent positioning

---

## Requirements

* Plymouth
* `update-alternatives`
* A Linux distribution using `/usr/share/plymouth/themes`
* Root/sudo access

The included installer is designed primarily for Debian/Ubuntu-based systems.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/BFUR64/WindowsXP-Plymouth.git
cd WindowsXP-Plymouth
```

Make the installer executable:

```bash
chmod +x install.sh
```

Run it:

```bash
./install.sh
```

The installer will:

1. Check for root privileges.
2. Request sudo access if necessary.
3. Validate the theme files.
4. Remove an existing WindowsXP installation.
5. Copy the theme into `/usr/share/plymouth/themes/`.
6. Register the theme with `update-alternatives`.
7. Select WindowsXP as the default Plymouth theme.
8. Rebuild the initramfs.

A successful installation will end with:

```text
✓ WindowsXP Plymouth theme is ready.
```

If you are using Kubuntu with KDE Plasma, see [Kubuntu / KDE Plasma](#kubuntu--kde-plasma-666) after installation.

---

## Kubuntu / KDE Plasma 6.6.6

### Important

If you are using **Kubuntu with KDE Plasma 6.6.6**, manually select the Windows XP splash screen through KDE System Settings after installing the theme.

KDE Plasma maintains its own boot splash selection. Changing the Plymouth `default.plymouth` alternative does not necessarily change KDE's stored preference.

This can result in Windows XP appearing during boot while a previously selected splash appears during shutdown or restart.

### Select the theme in KDE

Open:

**System Settings → Colors & Themes → Boot Splash Screen**

Select **Windows XP** and apply the change.

Afterward, the theme should be used consistently for:

* Booting
* Restarting
* Shutting down

This is a KDE-specific configuration step and is not required on systems that do not manage the splash screen through KDE Plasma.

---

## How It Works

The theme is composed of several image assets and a Plymouth script:

```text
WindowsXP/
├── WindowsXP.plymouth
├── WindowsXP.script
├── Background.png
├── Bar.png
├── Block-1.png
├── Block-2.png
└── Block-3.png

preview.gif
```

### `Background.png`

Contains the complete Windows XP background artwork.

It is centered automatically according to the current display resolution.

### `Bar.png`

The static loading-bar frame.

The bar is centered horizontally and positioned beneath the XP logo.

### `Block-1.png`, `Block-2.png`, `Block-3.png`

The three individual loading blocks used by the animation.

Each block is positioned with a fixed spacing of:

```text
14 px block + 4 px gap = 18 px
```

The animation advances in exact 18 px increments.

### `WindowsXP.script`

Controls the Plymouth animation, including:

* Background positioning
* Loading-bar positioning
* Block positioning
* Animation timing
* Block visibility
* Animation looping
* End-of-loop pause
* Boot-dialog hiding

The animation refreshes every 20 ms and advances every 80 ms.

After the final block leaves the animation track, the script pauses for 80 ms before restarting the animation.

---

## Manual Installation

If you do not want to use the installer, install the theme manually.

Copy the theme:

```bash
sudo cp -a WindowsXP /usr/share/plymouth/themes/
```

Register it:

```bash
sudo update-alternatives --install \
    /usr/share/plymouth/themes/default.plymouth \
    default.plymouth \
    /usr/share/plymouth/themes/WindowsXP/WindowsXP.plymouth \
    100
```

Select it:

```bash
sudo update-alternatives --set \
    default.plymouth \
    /usr/share/plymouth/themes/WindowsXP/WindowsXP.plymouth
```

Rebuild the initramfs:

```bash
sudo update-initramfs -u
```

If you use Kubuntu/KDE Plasma, also follow the [KDE configuration steps](#kubuntu--kde-plasma-666).

---

## Testing

You can inspect the currently selected Plymouth theme with:

```bash
update-alternatives --display default.plymouth
```

You should see:

```text
/usr/share/plymouth/themes/WindowsXP/WindowsXP.plymouth
```

You can also inspect the installed theme:

```bash
ls -la /usr/share/plymouth/themes/WindowsXP
```

Plymouth itself normally runs during the boot process, so testing the complete splash generally requires a reboot.

---

## Troubleshooting

### Windows XP appears during boot, but another theme appears during shutdown/restart

If you are using Kubuntu with KDE Plasma 6.6.6, follow the [KDE configuration steps](#kubuntu--kde-plasma-666).

KDE may still have a different splash theme selected independently of the Plymouth `default.plymouth` alternative.

### The theme does not appear

Check that the theme was installed:

```bash
ls /usr/share/plymouth/themes/WindowsXP
```

Then check the active Plymouth alternative:

```bash
update-alternatives --display default.plymouth
```

If necessary, select it again:

```bash
sudo update-alternatives --set \
    default.plymouth \
    /usr/share/plymouth/themes/WindowsXP/WindowsXP.plymouth
```

Then rebuild the initramfs:

```bash
sudo update-initramfs -u
```

### Changes to the theme are not appearing

Plymouth is loaded from the initramfs during early boot.

After modifying the installed theme, rebuild the initramfs:

```bash
sudo update-initramfs -u
```

Without this step, the system may continue booting with the previous version of the theme.

---

## Development

The theme intentionally uses a simple Plymouth scripting implementation.

The animation consists of three separate block images moving across a fixed track.

The primary animation parameters are:

```text
Block width:       14 px
Block gap:          4 px
Animation step:    18 px
Bar padding:       10 px
Refresh interval:  20 ms
Movement interval: 80 ms
Loop pause:        80 ms
```

The 20 ms refresh interval is used by the Plymouth script's refresh function. The animation itself advances every fourth refresh, resulting in an 80 ms movement interval.

The loading blocks are hidden whenever they are completely outside the usable animation track.

The animation is positioned relative to the display dimensions rather than assuming a fixed screen resolution.

### Preview GIF

`preview.gif` is generated from the same animation logic used by `WindowsXP.script`.

It reproduces two complete animation cycles for convenient repository previews without requiring Plymouth to be running.

---

## License

This project is provided for personal and educational use.

Windows XP, Windows, and related Microsoft trademarks and artwork belong to their respective owners.

This project is **not affiliated with or endorsed by Microsoft**.

---

## Credits

Inspired by the classic **Microsoft Windows XP** boot experience.

Built for **Plymouth** on Linux.

Tested on **Kubuntu / KDE Plasma 6.6.6**.
