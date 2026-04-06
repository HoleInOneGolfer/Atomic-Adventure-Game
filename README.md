# ⚛️ Atomic Adventure

> **"In the subatomic world, balance isn't just a goal—it's the only way to survive."** 🧪

**Atomic Adventure** is a 2D physics-based survival game built with Pygame. You control a single atom navigating a chaotic field of protons, electrons, and rival nuclei. Your mission is to climb the Periodic Table from Hydrogen to Oganesson by absorbing particles while fighting the constant pull of electromagnetic forces.

## 🕹️ Gameplay

### 1. The Growth Loop

To evolve, you must collide with floating **Protons (+)**. Every proton increases your Atomic Number ($Z$), changing your element and increasing your mass.

### 2. Ionic Stability

The game tracks your **Net Charge ($q$)**.

- **Neutral State**: When Protons == Electrons, your stability bar refills.
- **Ionized State**: If your charge is unbalanced, your stability drains.
- **Fission**: If your stability hits zero, your atom undergoes nuclear fission—**Game Over**.

### 3. Navigation

The atom follows your **Mouse or Touch** location. However, movement is influenced by momentum and the electromagnetic pull of nearby particles.

## 🧪 The Science

The game's engine is driven by a modified version of **Coulomb's Law**:

$$F = k_e \frac{q_1q_2}{r^2}$$

Because of this, being a highly charged Ion ($q \neq 0$) changes the game difficulty:

- **Attraction**: If you are positive, electrons will fly toward you, making it easier to stabilize.
- **Repulsion**: If you are positive, other protons will be pushed away, making it harder to grow until you find balance.

## 💀 Death & Feedback

The universe is a dangerous place for a lonely atom. You need to watch out for:

- Collisions: Hitting the nucleus of a rival atom results in instant destruction.
  - Message: "Your [Element] atom collided with a [Element] nucleus!"
- Instability: Staying ionized for too long leads to decay.
  - Message: "Your [Element] atom became too unstable to exist."

## 🚀 Future Roadmap

These features are part of the long-term vision and are currently in development:

- [ ] Special Abilities: Unique perks for element groups (e.g., Noble Gas invulnerability).
- [ ] ChemLib Integration: Scaling mass and speed based on real-world atomic weights.
- [ ] Molecular Bonding: Combining with other atoms to form stable structures.
- [ ] Isotope System: Adding Neutrons to further refine nuclear stability.

## 🛠️ Technical Setup

### Prerequisites

- Python 3.x
- Pygame (pip install pygame)

### Running locally

```bash
python src/main.py
```

### Debugging & Testing

- Dev Keybinds: (Note: These may be commented out in main.py for production builds)
  - Press W while playing to instantly jump to the final element (Oganesson) to test the victory state.

### Building the Release

The project is configured for PyInstaller. Run this from the root directory to generate a standalone .exe:

```bash
pyinstaller --noconsole --onefile --icon="atomic.ico" --name "AtomicAdventure" --add-data "src/settings.py;." --add-data "src/physics.py;." --add-data "src/entities.py;." --add-data "atomic.png;." src/main.py
```

## 💡Original Idea

I am making a game where you play as an atom floating through space. You move around and come across other atoms and subatomic particles. Your goal is to move up the periodic table from Hydrogen, but you must combine with other particles properly or you become unstable. if you are unstable too long you die. each element has its own special ability. If you combine incorrectly you die.

I would start with you having to just collect subatomic particles to advance and avoid the other atoms though they may be attracted to you. The goal would be to collect all the elements

It takes place in a 2D plane and you can move in all directions. You can also rotate to face different directions. You move with your mouse or touch. It follows your mouse or touch location. The game would have a simple art style with bright colors.
