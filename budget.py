class Category(object):

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        text = self.category.center(30, '*')
        # https://pyformat.info/
        # Using % and .format() for great good!
        for d in self.ledger:
            description = '{:23}'.format(d['description'])[:23]
            amount = '{:7.2f}'.format(d['amount'])
            text += '\n' + description + amount
        balance = '{:.2f}'.format(self.get_balance())
        text += '\nTotal: ' + balance
        return text

    def deposit(self, amount, description=''):
        self.ledger.append({
            'amount': amount,
            'description': description,
            })

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({
                'amount': -amount,
                'description': description,
                })
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for x in self.ledger:
            balance += x['amount']
        return balance

    def transfer(self, amount, obj):
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to ' + obj.category)
            obj.deposit(amount, 'Transfer from ' + self.category)
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def get_spents(self):
        return -sum(x['amount'] for x in self.ledger if x['amount'] < 0)



def create_spend_chart(categories):
    total_spent = sum(cat.get_spents() for cat in categories)
    dados = []
    for cat in categories:
        dados.append({
            'category': cat.category,
            'percent': int(cat.get_spents() * 10 / total_spent) * 10
            })
    dados_sorted = dados[:]
    #dados_sorted = sorted(dados, key=lambda k: k['percent'], reverse=True)
    #print(dados_sorted)
    chart = 'Percentage spent by category\n'
    for x in range(100, -10, -10):
        chart += '{:3d}'.format(x) + '| '
        lst = ['o  ' if dct['percent'] >= x else '   ' for dct in dados_sorted]
        chart += ''.join(lst) + '\n'
    dashes = 3 * len(categories) + 1
    chart += ' ' * 4 + '-' * dashes
    len_words = max(len(d['category']) for d in dados_sorted)
    for i in range(len_words):
        line = '\n' + ' ' * 5
        for d in dados_sorted:
            if i >= len(d['category']):
                line += ' '
            else:
                line += d['category'][i]
            line += '  '
        chart += line
    return chart
