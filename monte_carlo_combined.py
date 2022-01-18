import random

def price_diff_generator(price_daily_diffs):
  while True:
    yield random.choice(price_daily_diffs)

class DayInfo:
  def __init__(self, win, threshold):
    self.win = win
    self.threshold = threshold

class Instrument:
  def __init__(self, init_price, price_diffs_generator, days_info):
    self._init_price = init_price
    self._price_diffs_generator = price_diffs_generator
    self._days_info = days_info

  def get_init_price(self):
    return self._init_price

  def get_price_diff(self):
    return next(self._price_diffs_generator)

  def win_for_day(self, cur_price, day_num):
    if cur_price < self._days_info[day_num].threshold:
      return None
    return self._days_info[day_num].win

class InstrumentSim:
  def __init__(self, instrument):
    self._instrument = instrument
    self._cur_price  = instrument.get_init_price()

  def adjust_price(self):
    self._cur_price += self._instrument.get_price_diff()

  def get_win_for_day(self, day_num):
    return self._instrument.win_for_day(self._cur_price, day_num)

def one_attempt(instruments, days_count):
  total_win = 0

  runs = [ InstrumentSim(instrument) for instrument in instruments ]

  for day in range(days_count):
    todays_win = 0

    for run in runs:
      cur_win = run.get_win_for_day(day)
      if not cur_win:
        return total_win

      todays_win += cur_win
      run.adjust_price()

    total_win += todays_win

  return total_win


### tests =============

def constant_price_diff(diff):
  while True:
    yield diff

def increasing_instrument(win):
  init_price = 100
  days_info = [ DayInfo(win, init_price - 1) for d in range(1000)]  # we can do more days
  return Instrument( init_price, constant_price_diff(1), days_info )

def decreasing_instrument(days_till_stop, win):
  threshold = 10
  init_price = days_till_stop + threshold - 1
  days_info = [ DayInfo(win, threshold) for d in range(1000)]
  return Instrument( init_price, constant_price_diff(-1), days_info )

def test_process_day():
  # only increasing ==============
  assert 10 == one_attempt([increasing_instrument(win = 1)], days_count = 10)

  assert 30 == one_attempt([increasing_instrument(win = 1),
                            increasing_instrument(win = 2)],
                            days_count = 10)


  # only decreasing =============
  assert 5 == one_attempt([decreasing_instrument(days_till_stop = 5, win = 1)],
                          days_count = 10)

  ### decreasing instrument, 5 days till stop 1st, 2 days for second , 10 days
  assert 6 == one_attempt([decreasing_instrument(days_till_stop = 5, win = 2),
                           decreasing_instrument(days_till_stop = 2, win = 1)],
                           days_count = 10)

  ### increasing, decreasing
  assert 21 == one_attempt([increasing_instrument(win = 1),
                            decreasing_instrument(days_till_stop = 7, win = 2)],
                            days_count = 10)


def tests():
  test_process_day()

def main():
  tests()

if __name__ == '__main__':
  main()
