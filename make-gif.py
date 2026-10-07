from PIL import Image
from pathlib import Path

# ============================================================================
# Configuration
# ============================================================================

THEME_DIR = Path("WindowsXP")
OUTPUT = Path("WindowsXP-preview.gif")

# Match the Plymouth display resolution.
# Change these if you are rendering for another resolution.
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

REFRESH_TIME = 20
MOVEMENT_TIME = 80
PAUSE_TIME = 80

BAR_PADDING = 10
BLOCK_GAP = 4

# ============================================================================
# Load the exact assets used by WindowsXP.script
# ============================================================================

background = Image.open(
    THEME_DIR / "Background.png"
).convert("RGBA")

bar = Image.open(
    THEME_DIR / "Bar.png"
).convert("RGBA")

blocks = [
    Image.open(THEME_DIR / "Block-1.png").convert("RGBA"),
    Image.open(THEME_DIR / "Block-2.png").convert("RGBA"),
    Image.open(THEME_DIR / "Block-3.png").convert("RGBA"),
]

block_width = blocks[0].width
block_height = blocks[0].height

block_step = block_width + BLOCK_GAP

# ============================================================================
# BOOT SETUP
# ============================================================================

# Exactly as in the Plymouth script:
#
# background.x =
#     Window.GetWidth() / 2 -
#     background.image.GetWidth() / 2;

background_x = (
    WINDOW_WIDTH // 2
    - background.width // 2
)

background_y = (
    WINDOW_HEIGHT // 2
    - background.height // 2
)

# Exactly as in the Plymouth script:
#
# loading_bar.x =
#     Window.GetWidth() / 2 -
#     loading_bar.image.GetWidth() / 2;
#
# loading_bar.y =
#     Window.GetHeight() / 2 + 134;

bar_x = (
    WINDOW_WIDTH // 2
    - bar.width // 2
)

bar_y = (
    WINDOW_HEIGHT // 2
    + 134
)

# Animation track.
track_left = bar_x + BAR_PADDING

track_right = (
    bar_x
    + bar.width
    - BAR_PADDING
)

# Exactly:
#
# animation_position =
#     -(block_step * 3) + 1;

animation_position = (
    -(block_step * 3) + 1
)

# Exactly:
#
# animation_timer = 0;
# end_pause_frames = 0;

animation_timer = 0
end_pause_frames = 0

# ============================================================================
# Rendering
# ============================================================================

def render_frame(animation_position):
    """
    Render exactly what the Plymouth sprites would look like
    for the supplied animation_position.
    """

    frame = Image.new(
        "RGBA",
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        (0, 0, 0, 255)
    )

    # ------------------------------------------------------------------------
    # Background
    # ------------------------------------------------------------------------

    frame.alpha_composite(
        background,
        (background_x, background_y)
    )

    # ------------------------------------------------------------------------
    # Loading bar
    # ------------------------------------------------------------------------

    frame.alpha_composite(
        bar,
        (bar_x, bar_y)
    )

    # ------------------------------------------------------------------------
    # Loading blocks
    # ------------------------------------------------------------------------

    block_y = (
        bar_y
        + (bar.height - block_height) // 2
    )

    for index, block in enumerate(blocks):

        # Exactly:
        #
        # block[index].x =
        #     track_left +
        #     animation_position +
        #     index * block_step;

        block_x = (
            track_left
            + animation_position
            + index * block_step
        )

        # Exactly the same visibility test:
        #
        # if (
        #     block[index].x + block_width <= track_left ||
        #     block[index].x >= track_right
        # )

        if (
            block_x + block_width <= track_left
            or
            block_x >= track_right
        ):
            continue

        frame.alpha_composite(
            block,
            (block_x, block_y)
        )

    return frame


# ============================================================================
# Simulate Plymouth's refresh() function
# ============================================================================

def generate_cycle():
    """
    Reproduce one complete execution cycle of refresh():

        initial hidden state
        -> movement
        -> end detection
        -> 80 ms pause
        -> reset

    The important part is that Plymouth refreshes every 20 ms.
    """

    frames = []

    animation_position = -(block_step * 3) + 1
    animation_timer = 0
    end_pause_frames = 0

    # ------------------------------------------------------------------------
    # Initial state
    #
    # This is the state immediately after BOOT SETUP.
    # All blocks exist but have opacity 0.
    # ------------------------------------------------------------------------

    frames.append(
        render_frame(animation_position)
    )

    while True:

        # ================================================================
        # This is one call to refresh()
        # ================================================================

        if end_pause_frames > 0:

            # Exactly:
            #
            # end_pause_frames -= 1;

            end_pause_frames -= 1

            # When it reaches zero, Plymouth resets the animation.
            if end_pause_frames == 0:

                # Exactly:
                #
                # animation_position =
                #     -(block_step * 3) + 1;

                animation_position = (
                    -(block_step * 3) + 1
                )

                # Exactly:
                #
                # animation_timer = 0;

                animation_timer = 0

                # This is now the new visual state.
                frames.append(
                    render_frame(animation_position)
                )

                break

            # During the pause, the frame does not change.
            continue

        # ================================================================
        # NORMAL MOVEMENT
        # ================================================================

        # Exactly:
        #
        # animation_timer += 20;

        animation_timer += REFRESH_TIME

        if animation_timer >= MOVEMENT_TIME:

            animation_timer = 0

            # Exactly:
            #
            # animation_position += block_step;

            animation_position += block_step

            # Render the newly moved position.
            frames.append(
                render_frame(animation_position)
            )

            # Exactly:
            #
            # if (
            #     track_left +
            #     animation_position >=
            #     track_right
            # )

            if (
                track_left
                + animation_position
                >= track_right
            ):
                # Exactly:
                #
                # end_pause_frames = 4;

                end_pause_frames = (
                    PAUSE_TIME // REFRESH_TIME
                )

    return frames


# ============================================================================
# Generate exactly two animation cycles
# ============================================================================

cycle = generate_cycle()

frames = cycle + cycle

# Every visible state produced by the script lasts until
# the next state-changing refresh.
#
# Movement occurs every 80 ms.
# The final reset occurs after an 80 ms pause.

durations = [
    MOVEMENT_TIME
] * len(frames)

# ============================================================================
# Save GIF
# ============================================================================

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=1,
    disposal=2,
)

print(f"Created: {OUTPUT}")
print(f"Resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
print(f"Frames per cycle: {len(cycle)}")
print(f"Total frames: {len(frames)}")
print("Playback: exactly 2 cycles")
