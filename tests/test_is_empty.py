"""Owner: Pooney Joseph

**Requirement:** 
query both ultrasonic sensors at least 5 times each,
filter out noise, disregard a sensor that is continuously noisy and
return a distance between 0–200cm.

**Not provided in requiremnt: ** 
Both sensors are noisy at the same time and Reading outside 0–200cm 

is sensor A noisy? Is sensor B noisy?

(a) Both sensors are clean and agree => Filter average of the two readings 
(b) Sensor A is noisy and B is clean  => A is disregarded entirely; return B's reading 
(c) Sensor B is noisy and A is clean => B is disregarded entirely; return A's reading
(d) Both sensors are noisy at the same time => raise an error instead of guessing 
                                               (because it isnot mentioned in the REQUIREMENTS)
(e) Reading exactly 0cm (lower boundary) => Accepted as valid 
(f) Reading exactly 200cm (upper boundary) => Accepted as valid 
(g) Reading outside 0–200cm => treat it as invalid, same as a noisy reading 
                               (because it isnot mentioned in the REQUIREMENTS)
(f) Checking how many times each sensor is actually queried => Each sensor is read at least 5 times 

"""

#testing code starts here
