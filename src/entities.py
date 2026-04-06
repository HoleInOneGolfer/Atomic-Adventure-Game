import pygame
import math
import random
from physics import PhysicsObject, Particle
from settings import *


class Element(PhysicsObject):
    """Atomic entity that manages stability and chemical notation."""

    def __init__(self, x, y, protons=1, electrons=1):
        # Radius grows slightly as the atom gains protons
        radius = 18 + (protons * 0.8)
        super().__init__(x, y, (protons - electrons), (protons + electrons), radius)
        self.protons = protons
        self.electrons = electrons
        self.stability = MAX_STABILITY
        self.font = pygame.font.SysFont("Verdana", 18, bold=True)

    def get_notation(self):
        """Generates standard chemical notation (e.g., He, Li+, O2-)."""
        idx = max(0, min(len(ELEMENT_DATA) - 1, self.protons - 1))
        symbol = ELEMENT_DATA[idx]["symbol"]
        q = self.protons - self.electrons

        if q == 0:
            return symbol
        sign = "+" if q > 0 else "-"
        val = str(abs(q)) if abs(q) > 1 else ""
        return f"{symbol}{val}{sign}"

    def update_logic(self):
        """Determines stability. Neutral atoms heal; ionized atoms decay."""
        self.charge = self.protons - self.electrons
        if self.charge == 0:
            self.stability = min(MAX_STABILITY, self.stability + REGEN_RATE)
        else:
            self.stability -= abs(self.charge) * DRAIN_MULTIPLIER

        self.stability = max(0, min(MAX_STABILITY, self.stability))

    def draw(self, screen, is_player=False):
        """Draws the atom, notation, and the outer stability ring."""
        # Stability Arc
        if self.stability < MAX_STABILITY:
            health_pct = self.stability / MAX_STABILITY
            color = (int(255 * (1 - health_pct)), int(255 * health_pct), 50)
            rect = pygame.Rect(
                self.pos.x - self.radius - 10,
                self.pos.y - self.radius - 10,
                (self.radius + 10) * 2,
                (self.radius + 10) * 2,
            )
            end_angle = math.radians((health_pct * 360) - 90)
            pygame.draw.arc(screen, color, rect, math.radians(-90), end_angle, 5)

        # Main Nucleus
        body_color = WHITE if is_player else (130, 130, 150)
        pygame.draw.circle(
            screen, body_color, (int(self.pos.x), int(self.pos.y)), self.radius, 2
        )

        # Chemical Symbol Text
        text = self.font.render(self.get_notation(), True, WHITE)
        screen.blit(text, text.get_rect(center=(self.pos.x, self.pos.y)))


class Player(Element):
    """Atom controlled by the user's mouse."""

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        target = pygame.Vector2(mouse_pos)
        dist = target - self.pos
        # Smooth lerp-like movement toward the mouse
        if dist.length() > 2:
            self.pos += dist * 0.12
        self.update_logic()
        self.check_bounds()


class NPC(Element):
    """Rival atoms that drift and hunt for particles."""

    def __init__(self, x, y, protons=1, electrons=1):
        super().__init__(x, y, protons, electrons)
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def update(self, player_pos):
        # Slight drift toward the player to encourage interaction
        drift_vec = player_pos - self.pos
        if drift_vec.length() > 0:
            drift_vec.normalize_ip()
            self.apply_force(drift_vec * 0.05)

        # Random Brownian-motion-style jitter
        if random.random() < 0.05:
            self.apply_force(
                pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            )

        self.update_physics()
        self.update_logic()
