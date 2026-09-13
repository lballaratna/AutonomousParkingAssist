from autonomous_parking_system import ParkingAssistant, FixedSensor

c = ParkingAssistant(
    FixedSensor(0),
    FixedSensor(0)
)

print(c.state)


