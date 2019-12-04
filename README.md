# Evolution Simulation
---

## Creatures
### Herbivore

The following traits can be passed down to the next generation.
```
max_size: The maximum size of the creature. Hunger, the amount a creature must eat in order to produce offspring, is based on max_size. 
width, height: The size of the creature in pixels. Maximum velocity is decreased as the creature grows. 
jerk: The rate of change of acceleration.
acceleration_max: The maximum acceleration in x, y direction. 
velocity_max: The maximum velocity in x, y direction. 
num_offspring_divisor: If the creature survives the round, they will produce width/num_offspring_divisor children for the next round.  If a creature survives a round they will produce at least one child. 
search_distance: The distance that a creature can sense food at. If there is no food within the search distance, the creature will move randomly. 
```