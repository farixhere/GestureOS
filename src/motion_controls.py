
import time


class MotionController:
    """
    GestureOS motion engine.
    Tracks total palm movement instead of frame-to-frame movement.
    """

    def __init__(self):
        self.anchor = None
        self.last_action = 0

        # Movement sensitivity
        self.vertical_threshold = 0.055
        self.horizontal_threshold = 0.075

        # Prevent repeated slide changes during one swipe
        self.horizontal_locked = False

        # Action timing
        self.cooldown = 0.45

    def get_hand_position(self, hand):
        """
        Use the palm centre for more stable tracking.
        """

        points = [0, 5, 9, 13, 17]

        x = sum(hand.landmark[i].x for i in points) / len(points)
        y = sum(hand.landmark[i].y for i in points) / len(points)

        return x, y

    def update(self, hand):

        position = self.get_hand_position(hand)

        if self.anchor is None:
            self.anchor = position
            return None

        x, y = position
        start_x, start_y = self.anchor

        # Total movement from the starting position
        dx = x - start_x
        dy = y - start_y

        now = time.time()

        if now - self.last_action < self.cooldown:
            return None

        action = None

        # Vertical movement: scrolling
        if (
            abs(dy) >= self.vertical_threshold
            and abs(dy) > abs(dx) * 1.15
        ):
            action = "SCROLL DOWN" if dy > 0 else "SCROLL UP"

            # Re-anchor for another scroll movement
            self.anchor = position
            self.last_action = now

        # Horizontal movement: slide navigation
        elif (
            abs(dx) >= self.horizontal_threshold
            and abs(dx) > abs(dy) * 1.15
            and not self.horizontal_locked
        ):
            action = "SWIPE RIGHT" if dx > 0 else "SWIPE LEFT"

            self.horizontal_locked = True
            self.last_action = now

        return action

    def reset(self):
        self.anchor = None
        self.last_action = 0
        self.horizontal_locked = False
