#!/bin/bash
set -euo pipefail

# ============================================================================
# WindowsXP Plymouth Theme Installer
# ============================================================================

THEME_NAME="WindowsXP"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/$THEME_NAME"

THEMES_DIR="/usr/share/plymouth/themes"
THEME_DIR="$THEMES_DIR/$THEME_NAME"
THEME_FILE="$THEME_DIR/$THEME_NAME.plymouth"


# ============================================================================
# Colors
# ============================================================================

if [[ -t 1 ]]; then
    RESET='\033[0m'
    BOLD='\033[1m'
    DIM='\033[2m'

    RED='\033[31m'
    GREEN='\033[32m'
    YELLOW='\033[33m'
    BLUE='\033[34m'
    CYAN='\033[36m'
else
    RESET=''
    BOLD=''
    DIM=''

    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
fi


# ============================================================================
# Output helpers
# ============================================================================

print_header() {
    echo
    echo -e "${BOLD}${BLUE}╭──────────────────────────────────────────────╮${RESET}"
    echo -e "${BOLD}${BLUE}│${RESET}         ${BOLD}WindowsXP Plymouth Installer${RESET}         ${BOLD}${BLUE}│${RESET}"
    echo -e "${BOLD}${BLUE}╰──────────────────────────────────────────────╯${RESET}"
    echo
}

info() {
    echo -e "  ${CYAN}•${RESET} $1"
}

success() {
    echo -e "  ${GREEN}✓${RESET} $1"
}

warning() {
    echo -e "  ${YELLOW}!${RESET} $1"
}

error() {
    echo -e "  ${RED}✗${RESET} $1" >&2
}

section() {
    echo
    echo -e "${BOLD}${CYAN}[$1]${RESET}"
}


# ============================================================================
# Error handling
# ============================================================================

cleanup_on_error() {
    echo
    error "Installation failed."
    echo
    exit 1
}

trap cleanup_on_error ERR


# ============================================================================
# Start
# ============================================================================

print_header

info "Theme:   ${BOLD}$THEME_NAME${RESET}"
info "Source:  ${DIM}$SOURCE_DIR${RESET}"
info "Target:  ${DIM}$THEME_DIR${RESET}"


# ============================================================================
# Privileges
# ============================================================================

section "Checking privileges"

if [[ "$EUID" -eq 0 ]]; then
    SUDO=""
    success "Running as root."
else
    info "Root privileges are required."
    info "Requesting sudo access..."

    if ! sudo -v; then
        error "Unable to obtain sudo privileges."
        exit 1
    fi

    SUDO="sudo"
    success "Sudo access granted."
fi


# ============================================================================
# Validate source
# ============================================================================

section "Validating theme"

if [[ ! -d "$SOURCE_DIR" ]]; then
    error "Source directory does not exist:"
    echo -e "    ${DIM}$SOURCE_DIR${RESET}"
    exit 1
fi

success "Source directory found."

if [[ ! -f "$SOURCE_DIR/$THEME_NAME.plymouth" ]]; then
    error "Plymouth theme file not found:"
    echo -e "    ${DIM}$SOURCE_DIR/$THEME_NAME.plymouth${RESET}"
    exit 1
fi

success "Plymouth theme file found."


# ============================================================================
# Safety check
# ============================================================================

section "Safety checks"

EXPECTED_THEME_DIR="/usr/share/plymouth/themes/$THEME_NAME"

if [[ "$THEME_DIR" != "$EXPECTED_THEME_DIR" ]]; then
    error "Unexpected installation target:"
    echo -e "    ${DIM}$THEME_DIR${RESET}"
    exit 1
fi

success "Installation target verified."


# ============================================================================
# Remove previous installation
# ============================================================================

section "Preparing installation"

if [[ -d "$THEME_DIR" ]]; then
    warning "Existing installation found."
    info "Removing previous theme..."

    $SUDO rm -rf -- "$THEME_DIR"

    success "Previous installation removed."
else
    success "No previous installation found."
fi


# ============================================================================
# Install
# ============================================================================

section "Installing theme"

info "Copying theme files..."

$SUDO cp -a -- "$SOURCE_DIR" "$THEME_DIR"

success "Theme files installed."


# ============================================================================
# Register with update-alternatives
# ============================================================================

section "Registering theme"

info "Adding $THEME_NAME to update-alternatives..."

$SUDO update-alternatives --install \
    "$THEMES_DIR/default.plymouth" \
    default.plymouth \
    "$THEME_FILE" \
    100

success "Theme registered."


# ============================================================================
# Select theme
# ============================================================================

section "Selecting theme"

info "Setting $THEME_NAME as the default Plymouth theme..."

$SUDO update-alternatives --set \
    default.plymouth \
    "$THEME_FILE"

success "Theme selected."


# ============================================================================
# Rebuild initramfs
# ============================================================================

section "Updating boot image"

info "Rebuilding initramfs..."
echo -e "  ${DIM}This may take a moment...${RESET}"

$SUDO update-initramfs -u

success "initramfs updated."


# ============================================================================
# Complete
# ============================================================================

trap - ERR

echo
echo -e "${BOLD}${GREEN}╭──────────────────────────────────────────────╮${RESET}"
echo -e "${BOLD}${GREEN}│${RESET}           ${BOLD}Installation successful!${RESET}           ${BOLD}${GREEN}│${RESET}"
echo -e "${BOLD}${GREEN}╰──────────────────────────────────────────────╯${RESET}"
echo

info "Theme:   ${BOLD}$THEME_NAME${RESET}"
info "Location: ${DIM}$THEME_DIR${RESET}"

echo
echo -e "${BOLD}Selected Plymouth theme:${RESET}"
echo

$SUDO update-alternatives --display default.plymouth

echo
echo -e "${GREEN}✓${RESET} ${BOLD}WindowsXP Plymouth theme is ready.${RESET}"
echo
