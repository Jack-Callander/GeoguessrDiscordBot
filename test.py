from src import ChromeDevice, Distance, GeoguessrResult, Rules, Time, Units

TEST_RUN_1 = 'eOpI74g7FUbUOtkt'
TEST_RUN_2 = 'F2YjiBJYYh81l3gE'
TEST_RUN_3 = 'bBbTwb9T8uc6jOhR'

assert Distance(50) + Distance(20) == Distance(70)
assert Distance(50) - Distance(20) == Distance(30)
assert Distance(1500, Units.METRES) == Distance(1.5, Units.KILOMETRES)
assert Distance(1, Units.KILOMETRES) + Distance(500, Units.METRES) == Distance(1.5, Units.KILOMETRES)

device = ChromeDevice('D:/chromedriver.exe')
result = GeoguessrResult(device, TEST_RUN_1)
assert result.score == 24492
assert result.distance == Distance(178)
assert result.time == Time(mins=4, secs=7)
assert result.map == "5e22e9fc1e34a04cbcba3fce"
assert result.time_limit == Time.zero()
assert result.rules == Rules.DEFAULT

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
assert result.map == "59a1514f17631e74145b6f47"
assert result.time_limit == Time(9, 40)
assert result.rules == Rules.NO_MOVE_NO_PAN_NO_ZOOM

result = GeoguessrResult(device, TEST_RUN_3)
assert result.score == 3569
assert result.time == Time(0, 37)
assert result.map == "famous-places"
assert result.time_limit == Time(0, 50)
assert result.rules == Rules.DEFAULT
