import random

def price_diff_generator(price_daily_diffs):
  while True:
    yield random.choice(price_daily_diffs)

class Asset:
  def __init__(self, init_price, price_diffs_generator):
    self._init_price = init_price
    self._price_diffs_generator = price_diffs_generator

  def get_init_price(self):
    return self._init_price

  def get_next_price(self, cur_price):
    return cur_price + next(self._price_diffs_generator)

class AssetSim:
  def __init__(self, asset):
    self._asset = asset
    self._cur_price = asset.get_init_price()

  def adjust_price(self):
    self._cur_price = self._asset.get_next_price(self._cur_price)

  def get_asset(self):
    return self._asset

  def get_cur_price(self):
    return self._cur_price

class DayInfo:
  def __init__(self, win, increase):
    ''' win - fixed, increase - percentage from init price '''
    self.win = win
    self.increase = increase

class Contract:
  def __init__(self, schedule):
    ''' schedule - list of DayInfo '''
    self._schedule = schedule

  def get_expected_price(self, asset, day_num):
    return asset.get_init_price() * self._schedule[day_num].increase

  def get_win(self, day_num):
    return self._schedule[day_num].win


def one_attempt(contract, assets, days_count):
  total_win = 0

  asset_sims = [ AssetSim(asset) for asset in assets ]

  for day in range(days_count):

    for asset_sim in asset_sims:
      expected_price = contract.get_expected_price(asset_sim.get_asset(), day)
      if asset_sim.get_cur_price() < expected_price:
        return total_win
      asset_sim.adjust_price()

    total_win += contract.get_win(day)

  return total_win


### tests =============

def constant_price_diff(diff):
  while True:
    yield diff

def test_process_day():
  # 1 first 3 days, After 3, if increases by 10% - 2  ==============
  expected_10_after_5 = Contract(
    [DayInfo(1, 1.0), DayInfo(1, 1.0), DayInfo(1, 1.0),
     DayInfo(2, 1.1), DayInfo(2, 1.1), DayInfo(2, 1.1)])

  do_nothing_asset     = Asset(100, constant_price_diff(0))
  increase_fast_enough = Asset(100, constant_price_diff(20))

  # untill threshold
  assert 2 == one_attempt(expected_10_after_5, [do_nothing_asset], 2)  # before expected increase
  assert 3 == one_attempt(expected_10_after_5, [do_nothing_asset], 3)  # on     expected increase
  assert 3 == one_attempt(expected_10_after_5, [do_nothing_asset], 4)  # after  expected increase

  assert 3 == one_attempt(expected_10_after_5, [do_nothing_asset, increase_fast_enough], 4)  # after  expected increase

  # passed the threshold
  assert 5 == one_attempt(expected_10_after_5, [increase_fast_enough], 4)
  assert 7 == one_attempt(expected_10_after_5, [increase_fast_enough, increase_fast_enough], 5)

def somewhat_real():
  asset_1 = Asset(100, price_diff_generator([ -1, 0, 1]))
  asset_2 = Asset(100, price_diff_generator([ -1, 0, 1, 2, 3]))

  contract = Contract([DayInfo(1, 1.0), DayInfo(1, 1.0), DayInfo(1, 1.02)])

  print(one_attempt(contract, [asset_1, asset_2], 3))

def tests():
  test_process_day()

def main():
  tests()
  somewhat_real()

if __name__ == '__main__':
  main()
