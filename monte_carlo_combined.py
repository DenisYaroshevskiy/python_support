import random

def price_diff_generator(price_daily_diffs):
  while True:
    yield random.choice(price_daily_diffs)

class instrument_day_info:
  def __init__(self, win, threshold):
    self.win = win
    self.threshold = threshold

class one_instrument:
  def __init__(self, init_price, price_diffs, days_info):
    self.init_price = init_price
    self.price_diffs = price_diffs
    self.days_info = days_info

  def get_price_diff(self):
    return next(self.price_diffs)

def process(instruments):
  total_win = 0

  cur_prices = [ instrument.init_price for instrument in instruments ]

  for day_number in range(len(instruments[0].days_info)):
    todays_win = 0

    for i in range(len(instruments)):
      cur_prices[i] += instruments[i].get_price_diff()
      if cur_prices[i] < instruments[i].days_info[day_number].threshold:
        return total_win

      todays_win += instruments[i].days_info[day_number].win

    total_win += todays_win

  return total_win


### tests =============

def constant_price_diff(diff):
  while True:
    yield diff

def constant_increase_instrument(init_price, win, threshold, diff, days_count):
  days_info = [ instrument_day_info(win, threshold) for d in range(days_count) ]

  return one_instrument (init_price, constant_price_diff(diff), days_info)

def test_process_day():
  increase_10_days = constant_increase_instrument(10, 1, 9, 1, 10)
  print(process([increase_10_days]))

  decrease_10_days = constant_increase_instrument(11, 1, 9, -1, 10)
  print(process([decrease_10_days]))

def tests():
  test_process_day()

def main():
  tests()

if __name__ == '__main__':
  main()
