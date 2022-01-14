import datetime

### Creating a class in case youu need more stuff in it, like multipliers
class Contract:
  def __init__(self, dates, tresholds):
    self._dates_to_tresholds = { day : treshold for day, treshold in zip(dates, tresholds) }

  def get_treshold(self, day):
    ''' returns None if day is not listed '''
    return self._dates_to_tresholds.get(day)

def dates_range(start_day, count):
  while count > 0:
    yield start_day
    start_day += datetime.timedelta(days = 1)
    count -= 1


def process( contract, dates, prices ):
  ''' returns date and price at which it stopped '''

  res = (None, None)

  for day, price in zip(dates, prices):
    res = (day, price)
    treshold = contract.get_treshold(day)
    if treshold and treshold < price:
      return res

  return res

### =====================
# This is not how you do testing. I just put a few things together so that I have smth running.
# I can show you how to do it proper.

def test_Contract():
  contract = Contract(
    [ datetime.date(2022, 1, 20), datetime.date(2022, 1, 22), datetime.date(2022, 1, 25) ],
    [                          2,                          5,                          3 ]
  )

  assert not contract.get_treshold(datetime.date(2022, 1, 19))
  assert     contract.get_treshold(datetime.date(2022, 1, 20)) == 2
  assert not contract.get_treshold(datetime.date(2022, 1, 21))
  assert     contract.get_treshold(datetime.date(2022, 1, 22)) == 5

def test_dates_range():
  as_list = [ day for day in dates_range(datetime.date(2022, 1, 20), 3) ]
  assert as_list == [ datetime.date(2022, 1, 20), datetime.date(2022, 1, 21), datetime.date(2022, 1, 22) ]

def test_process():
  contract = Contract(
    [ datetime.date(2022, 1, 21), datetime.date(2022, 1, 23) ],
    [                          2,                         4  ]
  )

  ### empty
  res = process(contract, dates_range(datetime.date(2022, 1, 20), 0), [])
  assert res == (None, None)

  ### below treshold
  res = process(
                contract, dates_range(datetime.date(2022, 1, 20), 5),
                [ 0, 1, 2, 3, 3 ]
               )
  assert res == (datetime.date(2022, 1, 24), 3)

  ### above treshold
  res = process(
                contract, dates_range(datetime.date(2022, 1, 20), 5),
                [ 0, 1, 2, 5, 3 ]
               )
  assert res == (datetime.date(2022, 1, 23), 5)


def tests():
  try:
    test_Contract()
    test_dates_range()
    test_process()
  except AssertionError as e:
    print("Tests failed")
    exit(1)


### ===================
# start

def main():
  tests()

if __name__ == '__main__':
  main()
