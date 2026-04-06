import pygame
from settings import *


class PhysicsObject:
    """Base class handling motion, forces, and screen boundaries."""

    def __init__(self, x, y, charge, mass, radius):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.charge = charge
        self.mass = mass
        self.radius = radius
        # Font used for '+' and '-' symbols on particles
        self.p_font = pygame.font.SysFont("Arial", 12, bold=True)

    def apply_force(self, force):
        """Standard F=ma implementation."""
        if self.mass > 0:
            self.acc += force / self.mass

    def check_bounds(self):
        """Bounces object off screen edges with 50% energy loss."""
        curr_w, curr_h = pygame.display.get_surface().get_size()

        # Horizontal boundaries
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.vel.x *= -0.5
        elif self.pos.x + self.radius > curr_w:
            self.pos.x = curr_w - self.radius
            self.vel.x *= -0.5

        # Vertical boundaries (accounts for GUI bar)
        if self.pos.y - self.radius < GUI_HEIGHT:
            self.pos.y = GUI_HEIGHT + self.radius
            self.vel.y *= -0.5
        elif self.pos.y + self.radius > curr_h:
            self.pos.y = curr_h - self.radius
            self.vel.y *= -0.5

    def pull_towards(self, other):
        """Applies an attractive or repulsive force based on charge."""
        if self.charge == 0 or other.charge == 0:
            return

        direction = other.pos - self.pos
        dist_sq = direction.length_squared()

        # Collision safety: prevents divide-by-zero or infinite force
        min_dist_sq = (self.radius + other.radius) ** 2
        actual_dist_sq = max(dist_sq, min_dist_sq)

        if actual_dist_sq < 640000:  # Effective interaction radius
            direction.normalize_ip()
            # Force strength = -G * (q1 * q2) / r^2
            strength = (
                -G_CONSTANT * (self.charge * other.charge) * 2500 / actual_dist_sq
            )
            self.apply_force(direction * strength)

    def update_physics(self):
        """Integrates acceleration into velocity and updates position."""
        self.vel += self.acc
        self.pos += self.vel

        # Speed limit to maintain game stability
        if self.vel.length() > 7:
            self.vel.scale_to_length(7)

        self.check_bounds()
        self.vel *= FRICTION
        self.acc *= 0


class Particle(PhysicsObject):
    """Smallest units of the game: Protons and Electrons."""

    def __init__(self, x, y, p_type):
        charge = 1 if p_type == "proton" else -1
        super().__init__(x, y, charge, 0.2, 8)
        self.type = p_type

    def draw(self, screen):
        """Renders the colored circle and the +/- text symbol."""
        color = PROTON_COLOR if self.type == "proton" else ELECTRON_COLOR
        pygame.draw.circle(
            screen, color, (int(self.pos.x), int(self.pos.y)), self.radius
        )

        symbol = "+" if self.type == "proton" else "-"
        text_surf = self.p_font.render(symbol, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.pos.x, self.pos.y))
        screen.blit(text_surf, text_rect)
