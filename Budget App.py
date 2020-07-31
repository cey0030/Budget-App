import math

class Category:
  def __init__(self, category):
    self.ledger = []
    self.category = category

  def deposit(self, amount, description=None):
    if description is None:
      description = ""
    self.ledger.append({"amount": amount, "description": description})
  
  def withdraw(self, amount, description=None):
    if description is None:
      description = ""
    if 0 > sum(event['amount'] for event in self.ledger) - amount:
      return False
    else:
      self.ledger.append({"amount": -amount, "description": description})
      return True

  def get_balance(self):
    return sum(event['amount'] for event in self.ledger)

  def transfer(self, amount, category):
    if 0 > self.get_balance() - amount:
      return False
    self.ledger.append({"amount": -amount, "description": "Transfer to " + category.category})
    category.ledger.append({"amount": amount, "description": "Transfer from " + self.category})
    return True
  
  def check_funds(self, amount):
    if self.get_balance() < amount:
      return False
    else: 
      return True

  def __str__(self):
    width = 30
    string = self.category.center(30, "*") + "\n"
    for event in self.ledger:
      string += event['description'][0:23] + (30-len(event['description'][0:23])-len(str('%.2f' % event['amount'])))*" " + str('%.2f' % event['amount']) + "\n"
    string += 'Total: ' + str('%.2f' % self.get_balance())
    return string
  
def create_spend_chart(categories):
  string = "Percentage spent by category\n"
  grand_total = 0
  category_list = []
  for category in categories:
    total = 0
    for event in category.ledger:
      if event['amount'] < 0:
        total += event['amount']
    category_list.append({category.category: total})
    grand_total += total
  for category in category_list:
    for key, value in category.items():
      category[key] = int(math.floor((value / grand_total * 100) / 10.0)) * 10
  y_axis = 100
  while y_axis >= 0:
    width_to_add = 3*len(categories) + 1
    if len(str(y_axis)) == 2:
      string += ' ' + str(y_axis) + '|'
    elif len(str(y_axis)) == 1:
      string += 2*' ' + str(y_axis) + '|'
    else:
      string += str(y_axis) + '|'
    for category in category_list:
      for key, value in category.items():
        if value >= y_axis:
          string += " o "
          width_to_add -= 3
        else:
          string += 3*' '
          width_to_add -= 3
    string += width_to_add*" " + "\n"
    y_axis -= 10
  string += ' '*4 + '-' + len(category_list)*3*'-' + '\n'
  category_names = []
  for category in categories:
    category_names.append(category.category)
  counter = 0
  while counter < len(max(category_names, key=len)):
    string += 4*' '
    for category_name in category_names:
      try:
        string += ' ' + category_name[counter] + ' '
      except IndexError:
        string += 3*' '
    string += ' ' + '\n'
    counter += 1
  return string.strip() + 2*' '