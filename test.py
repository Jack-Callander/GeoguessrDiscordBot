from src import ChromeDevice, GeoguessrResult, Time

TEST_RUN = 'eOpI74g7FUbUOtkt'

device = ChromeDevice('D:/chromedriver.exe')
result = GeoguessrResult(device, TEST_RUN)
assert result.score == 24492
assert result.time == Time(4, 7)
