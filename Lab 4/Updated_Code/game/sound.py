import math
from array import array

import pygame


class SoundEffects:
    """Sound effects synthesised in code (no audio files needed).

    If no audio device/mixer is available, or anything goes wrong while
    creating or playing a sound, every method quietly does nothing so the
    game keeps running silently.
    """

    def __init__(self):
        self.enabled = False
        self._eat = None
        self._game_over = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            mixer_format = pygame.mixer.get_init()
            if not mixer_format:
                return
            frequency, size, channels = mixer_format
            if size != -16:
                # Only signed 16-bit output is supported by the generator.
                return

            # Short, bright two-note blip.
            self._eat = self._build(
                [(660, 0.06), (990, 0.09)],
                frequency, channels, volume=0.35, square_mix=0.3,
            )
            # Longer, falling "wah-wah-wah" for game over.
            self._game_over = self._build(
                [(392, 0.18), (330, 0.18), (262, 0.18), (196, 0.45)],
                frequency, channels, volume=0.4, square_mix=0.5,
            )
            self.enabled = True
        except Exception:
            # No audio device, missing mixer, unsupported format, ...
            self.enabled = False

    @staticmethod
    def _build(notes, frequency, channels, volume, square_mix):
        """Return a pygame Sound made of consecutive (freq_hz, seconds) notes."""
        samples = array("h")
        peak = int(32767 * volume)
        for freq, duration in notes:
            count = int(frequency * duration)
            attack = max(1, int(frequency * 0.005))
            for i in range(count):
                phase = 2 * math.pi * freq * i / frequency
                sine = math.sin(phase)
                square = 1.0 if sine >= 0 else -1.0
                wave = (1 - square_mix) * sine + square_mix * square
                # Quick fade-in (avoids clicks) and linear fade-out.
                envelope = min(1.0, i / attack) * (1.0 - i / count)
                value = int(peak * wave * envelope)
                for _ in range(channels):
                    samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _play(self, sound):
        if not self.enabled or sound is None:
            return
        try:
            sound.play()
        except Exception:
            pass

    def play_eat(self):
        self._play(self._eat)

    def play_game_over(self):
        self._play(self._game_over)