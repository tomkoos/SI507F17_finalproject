import re

class Boxer:
  totalBoxers = 0

  def __init__(self, params):
    Boxer.totalBoxers += 1
    self.boxer_id = Boxer.totalBoxers
    self.pic_url = params.get('pic_url', None)

    # profile    
    self.name = params.get('name', None)
    self.real_name = params.get('real_name', '').replace('\n', ' ')
    if not self.real_name:
      self.real_name = self.name
    self.real_name = re.sub('[0-9\\[\\]]+', '', self.real_name)
    self.nickname = params.get('nickname', None)
    if self.nickname:
      self.nickname = re.sub('[0-9\\[\\]]+', '', self.nickname).replace('\n', ', ')
    self.weight = re.sub('[0-9\\[\\]]+', '', params.get('weight', 'Heavyweight')) \
                    .replace('\n', ', ')
    height = params.get('height', '')
    height_cm = re.search('([0-9.]+) cm', height)
    if not height_cm:
      height_m = re.search('([0-9.]+) m', height)
      if not height_m:
        self.height = 0
      else:
        self.height = round(float(height_m.group(1))*100, 1)
    else:
      self.height = float(height_cm.group(1))
    self.reach = params.get('reach', None)
    if self.reach:
      self.reach = int(re.search('([0-9.]+) cm', self.reach).group(1))
    self.country_id = params['country']['id']
    self.born = params.get('born', None)
    self.died = params.get('died', None)
    self.stance = params.get('stance', None)
    if self.stance:
      self.stance = re.sub('[0-9\\[\\]]+', '', self.stance)

    # records
    self.total_fights = re.search('([0-9]+)', params.get('total_fights', None)).group(1)
    self.wins = params.get('wins', None)
    self.wins_by_ko = params.get('wins_by_ko', 0)
    self.losses = params.get('losses', 0)
    self.draws = params.get('draws', 0)
    self.no_contests = params.get('no_contests', 0)

    self.recognitions = ''
    self.reign_days = 0

  def set_recognitions(self, recognitions):
    self.recognitions = recognitions

  def set_reign_days(self, reign_days):
    self.reign_days = reign_days

  def get_name(self):
    return self.name

  def __repr__(self):
    return self.name

  def __contains__(self, string):
    return (string in self.name) or (string in self.real_name) or (string in self.nickname)