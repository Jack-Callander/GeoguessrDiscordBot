from src import ChromeDevice, GeoguessrStreak, Rules, Time

device = ChromeDevice('D:/chromedriver.exe')

TEST_RUN_1 = 'ohw7OomKkCiu28Ee'
TEST_RUN_2 = 'zGSc1dKqcWAfWvv5'
TEST_RUN_3 = 'F59n7g5h0koPpLZO'

result = GeoguessrStreak(device, TEST_RUN_1)
assert result.streak_count == 6
assert result.time_limit == Time.zero()
assert result.rules == Rules.DEFAULT

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

result = GeoguessrStreak(device, TEST_RUN_2)
assert result.streak_count == 3
assert result.time_limit == Time(2)
assert result.rules == Rules.NO_MOVE

result = GeoguessrStreak(device, TEST_RUN_3)
assert result.streak_count == 0
assert result.time_limit == Time(2)
assert result.rules == Rules.NO_MOVE
