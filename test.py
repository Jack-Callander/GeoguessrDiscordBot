from src.Challenge import Challenge
from src import ChromeDevice, Distance, GeoguessrMap, GeoguessrResult, Rules, Time, Units

device = ChromeDevice('D:/chromedriver.exe')

TEST_RUN_1 = 'eOpI74g7FUbUOtkt'
TEST_RUN_2 = 'F2YjiBJYYh81l3gE'
TEST_RUN_3 = 'bBbTwb9T8uc6jOhR'
TEST_RUN_4 = 'M1MOmkoi8ouEd4kI'

MAP_SYDNEY = GeoguessrMap(device, "5e22e9fc1e34a04cbcba3fce")
MAP_DIVERSE_WORLD = GeoguessrMap(device, "59a1514f17631e74145b6f47")
MAP_FAMOUS_PLACES = GeoguessrMap(device, "famous-places")
MAP_FLAGS_OTW = GeoguessrMap(device, "5d0ce72c8b19a91fe05aa7a8")

assert Distance(50) + Distance(20) == Distance(70)
assert Distance(50) - Distance(20) == Distance(30)
assert Distance(1500, Units.METRES) == Distance(1.5, Units.KILOMETRES)
assert Distance(1, Units.KILOMETRES) + Distance(500, Units.METRES) == Distance(1.5, Units.KILOMETRES)

challenge = Challenge(MAP_DIVERSE_WORLD, Rules.NO_MOVE, time_limit=Time(mins=2, secs=0))

result = GeoguessrResult(device, TEST_RUN_1)
assert result.score == 24492
assert result.distance == Distance(178)
assert result.time == Time(mins=4, secs=7)
assert result.map == MAP_SYDNEY
assert result.time_limit == Time.zero()
assert result.rules == Rules.DEFAULT
assert not challenge.is_applicable(result)

rounds = result.get_rounds()
assert rounds[0].points == 4901
assert rounds[0].distance == Distance(27)
assert rounds[0].time == Time(secs=10)

assert rounds[1].points == 5000
assert rounds[1].distance == Distance(11)
assert rounds[1].time == Time(secs=10)

assert rounds[2].points == 5000
assert rounds[2].distance == Distance(6)
assert rounds[2].time == Time(mins=1, secs=20)

assert rounds[3].points == 4591
assert rounds[3].distance == Distance(114)
assert rounds[3].time == Time(secs=50)

assert rounds[4].points == 5000
assert rounds[4].distance == Distance(21)
assert rounds[4].time == Time(mins=1, secs=37)

result = GeoguessrResult(device, TEST_RUN_2)
assert result.score == 8620
assert result.time == Time(0, 27)
assert result.map == MAP_DIVERSE_WORLD
assert result.time_limit == Time(9, 40)
assert result.rules == Rules.NO_MOVE_NO_PAN_NO_ZOOM
assert challenge.is_applicable(result)

result = GeoguessrResult(device, TEST_RUN_3)
assert result.score == 3569
assert result.time == Time(0, 37)
assert result.map == MAP_FAMOUS_PLACES
assert result.time_limit == Time(0, 50)
assert result.rules == Rules.DEFAULT
assert not challenge.is_applicable(result)

result = GeoguessrResult(device, TEST_RUN_4)
assert result.score == 24958
assert result.time == Time(3, 0)
assert result.map == MAP_FLAGS_OTW
assert result.time_limit == Time(2, 0)
assert result.rules == Rules.NO_MOVE
assert not challenge.is_applicable(result)
