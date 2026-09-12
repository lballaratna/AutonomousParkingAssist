"""Owner: Pooney Joseph

**Requirement:** move the car one metre, check for a parking space while
moving and never let the car go past either end of the 500m street.

Because there is a hard limit at both ends of the street, we test both
sides of each limit specifically, not just an ordinary middle value.

(a) MoveBackward from position 500 => Position becomes 499 and it is Valid move
(b) MoveBackward from position 1 => Position becomes 0 and it is valid move 
(c) MoveBackward from position 0 (already at the lower limit) =>Position stays at 0 — rejected 
(d) Any successful move => A parking-space reading gets recorded 
"""

