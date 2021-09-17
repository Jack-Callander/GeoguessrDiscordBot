from src import ChromeDevice, GeoguessrStreak

device = ChromeDevice('D:/chromedriver.exe')

STREAK_TEST_1 = 'ohw7OomKkCiu28Ee'

result = GeoguessrStreak(device, STREAK_TEST_1)
assert result.streak_count == 6

assert result.results[0].guess == "United States"
assert result.results[0].valid

assert result.results[1].guess == "Argentina"
assert result.results[1].valid

assert result.results[2].guess == "Germany"
assert result.results[2].valid

assert result.results[3].guess == "Israel"
assert result.results[3].valid

assert result.results[4].guess == "Peru"
assert result.results[4].valid

assert result.results[5].guess == "New Zealand"
assert result.results[5].valid

assert result.results[6].guess == "United States"
assert result.results[6].correct_country == "Canada"
assert not result.results[6].valid
