import pygame
import sys
import os
import random
from settings import *
from physics import Particle
from entities import Player, NPC


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Atomic Adventure")

# Set the Window Icon
try:
    icon_img = pygame.image.load(resource_path("atomic.png"))
    pygame.display.set_icon(icon_img)
except Exception as e:
    print(f"Could not load icon: {e}")

clock = pygame.time.Clock()

# --- Assets & Fonts ---
gui_font = pygame.font.SysFont("Verdana", 14, bold=True)
msg_font = pygame.font.SysFont("Verdana", 60, bold=True)
sub_font = pygame.font.SysFont("Verdana", 22)
credit_font = pygame.font.SysFont("Verdana", 16)

# --- Game State ---
player = Player(WIDTH // 2, HEIGHT // 2)
particles = []
npcs = []
game_won = False
game_over = False
death_reason = ""


def get_dynamic_limits():
    """Calculates entity limits based on screen area."""
    w, h = screen.get_size()
    area = w * h
    p_limit = int((area / 100000) * PARTICLE_DENSITY)
    n_limit = int((area / 100000) * NPC_DENSITY)
    return max(10, p_limit), max(2, n_limit)


def spawn_random_particle():
    """Spawns a proton or electron at a random location."""
    w, h = screen.get_size()
    x, y = random.randint(20, w - 20), random.randint(GUI_HEIGHT + 20, h - 20)
    p_type = random.choice(["proton", "electron"])
    particles.append(Particle(x, y, p_type))


def spawn_npc():
    """Spawns a random NPC atom."""
    w, h = screen.get_size()
    p = random.randint(1, 3)
    e = random.choice([p, p + 1, p - 1])
    npcs.append(
        NPC(
            random.randint(50, w - 50),
            random.randint(GUI_HEIGHT + 50, h - 50),
            p,
            max(1, e),
        )
    )


def reset_game():
    """Resets all game variables to start a new session."""
    global player, npcs, particles, game_over, game_won, death_reason
    w, h = screen.get_size()
    player = Player(w // 2, h // 2)
    npcs = []
    particles = []
    game_over = False
    game_won = False
    death_reason = ""
    p_max, n_max = get_dynamic_limits()
    for _ in range(p_max):
        spawn_random_particle()
    for _ in range(n_max):
        spawn_npc()


def draw_gui(screen, player):
    """Draws the top HUD with the progress bar."""
    w, h = screen.get_size()
    pygame.draw.rect(screen, BLACK, (0, 0, w, GUI_HEIGHT))
    pygame.draw.line(screen, GRAY, (0, GUI_HEIGHT), (w, GUI_HEIGHT), 2)

    total_elements = len(ELEMENT_DATA)
    progress_pct = min(1.0, player.protons / total_elements)

    pygame.draw.rect(screen, GRAY, (20, 10, w - 40, 20))
    if progress_pct > 0:
        pygame.draw.rect(screen, GOLD, (20, 10, int((w - 40) * progress_pct), 20))

    current_name = ELEMENT_DATA[min(player.protons - 1, total_elements - 1)]["name"]
    text = gui_font.render(
        f"PROGRESS: {current_name} ({player.protons}/{total_elements})", True, WHITE
    )
    screen.blit(text, (w // 2 - text.get_width() // 2, 12))


# Initial Setup
reset_game()

# --- Main Game Loop ---
running = True
while running:
    screen.fill(BLACK)
    w, h = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over or game_won:
                reset_game()

        # --- DEBUG KEYBINDS ---
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w:  # Press 'W' to instant win
        #         player.protons = WIN_Z
        #         player.electrons = WIN_Z  # Keep it stable for the victory screen
        #     if event.key == pygame.K_d:  # Press 'D' to instant death
        #         player.stability = 0
        #     if event.key == pygame.K_a:  # 1 from win
        #         player.protons = WIN_Z - 1
        #         player.electrons = WIN_Z - 1

    if not game_over and not game_won:
        # Maintain populations based on screen size
        p_max, n_max = get_dynamic_limits()
        while len(particles) < p_max:
            spawn_random_particle()
        while len(npcs) < n_max:
            spawn_npc()

        player.update()
        player.draw(screen, is_player=True)

        # Check for Win Condition
        if player.protons >= WIN_Z:
            game_won = True

        # Check for Stability Death
        if player.stability <= 0:
            game_over = True
            p_name = ELEMENT_DATA[player.protons - 1]["name"]
            death_reason = f"Your {p_name} atom became too unstable to exist."

        # NPC Logic
        for n in npcs[:]:
            n.pull_towards(player)
            for other_n in npcs:
                if n != other_n:
                    n.pull_towards(other_n)
            n.update(player.pos)
            n.draw(screen)

            # Collision Death
            if player.pos.distance_to(n.pos) < (player.radius + n.radius):
                game_over = True
                p_name = ELEMENT_DATA[player.protons - 1]["name"]
                n_name = ELEMENT_DATA[n.protons - 1]["name"]
                death_reason = f"Your {p_name} atom collided with a {n_name} nucleus!"

            # NPC absorption
            for p in particles[:]:
                if n.pos.distance_to(p.pos) < (n.radius + 15):
                    if p.type == "proton":
                        n.protons += 1
                    else:
                        n.electrons += 1
                    particles.remove(p)

            if n.stability <= 0:
                npcs.remove(n)

        # Particle Logic
        for p in particles[:]:
            targets = [player] + npcs
            closest = min(targets, key=lambda t: p.pos.distance_to(t.pos))
            p.pull_towards(closest)
            p.update_physics()
            p.draw(screen)

            if player.pos.distance_to(p.pos) < (player.radius + 15):
                if p.type == "proton":
                    player.protons += 1
                else:
                    player.electrons += 1
                particles.remove(p)

        draw_gui(screen, player)

    else:
        # --- END SCREEN (VICTORY OR DEATH) ---
        draw_gui(screen, player)
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        if game_won:
            title_text = "CONGRATULATIONS!"
            title_color = GOLD
            sub_text = (
                f"You synthesized the final element: {ELEMENT_DATA[WIN_Z-1]['name']}"
            )
        else:
            title_text = "GAME OVER!"
            title_color = PROTON_COLOR
            sub_text = death_reason

        m_text = msg_font.render(title_text, True, title_color)
        s_text = sub_font.render(sub_text, True, WHITE)
        r_text = sub_font.render("Click anywhere to Restart", True, GRAY)

        credit_lines = [f"Atomic Adventure {VERSION}","Developed by Ben","© 2026 Ben All rights reserved."]

        screen.blit(m_text, (w // 2 - m_text.get_width() // 2, h // 2 - 120))
        screen.blit(s_text, (w // 2 - s_text.get_width() // 2, h // 2 - 40))
        screen.blit(r_text, (w // 2 - r_text.get_width() // 2, h // 2 + 20))

        # Render Credits
        start_y = h - 110
        for i, line in enumerate(credits_lines):
            c_surf = credit_font.render(line, True, (140, 140, 140))
            screen.blit(c_surf, (w // 2 - c_surf.get_width() // 2, start_y + (i * 22)))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
