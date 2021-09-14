from src import ChromeDevice, GeoguessrResult, Time

TEST_RUN_1 = 'eOpI74g7FUbUOtkt'
TEST_RUN_2 = 'F2YjiBJYYh81l3gE'
TEST_RUN_3 = 'bBbTwb9T8uc6jOhR'

device = ChromeDevice('D:/chromedriver.exe')
result = GeoguessrResult(device, TEST_RUN_1)
assert result.score == 24492
assert result.time == Time(4, 7)
assert result.map == "5e22e9fc1e34a04cbcba3fc"
assert result.time_limit == Time(0, 0)

result = GeoguessrResult(device, TEST_RUN_2)
assert result.score == 8620
assert result.time == Time(0, 27)
assert result.map == "59a1514f17631e74145b6f47"
assert result.time_limit == Time(9, 40)

result = GeoguessrResult(device, TEST_RUN_3)
assert result.score == 3569
assert result.time == Time(0, 37)
assert result.map == "famous-places"
assert result.time_limit == Time(0, 50)