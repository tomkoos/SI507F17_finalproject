class BoxingRecords:
  def __init__(self, boxer_id):
    self.boxer_id = boxer_id
    self.have_record = True
    self.records = []
    self.headers = []

  def set_headers(self, headers):
    self.headers = headers

  def add_record(self, record):
    self.records.append(record)

  def no_record(self):
    self.have_record = False

  def __repr__(self):
    return "Boxing records for boxer ID: {}".format(self.boxer_id)

