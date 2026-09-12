"""Owner: Harikrishna M


**Requirement:** move the car one metre, check for a parking space while
moving and never let the car go past either end of the 500m street.

Because there is a hard limit at both ends of the street, we test both
sides of each limit specifically, not just an ordinary middle value.

a) MoveForward from position 0 => Position becomes 1 (valid move)
b) MoveForward from position 499 (one before the upper limit) =>Position becomes 500 (valid move)
c) MoveForward from position 500 (already at the upper limit) => Position stays at 500 — rejected 
d) Any successful move =>A parking-space reading gets recorded 

"""