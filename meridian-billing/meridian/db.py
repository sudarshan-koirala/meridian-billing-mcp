"""A very small in-memory database."""

_ACCOUNTS = {}
_INVOICES = []
_TICKETS = []


class Database:
    """Stores accounts, invoices and support tickets."""

    def save_account(self, account):
        _ACCOUNTS[account.account_id] = account

    def load_account(self, account_id):
        return _ACCOUNTS[account_id]

    def all_accounts(self):
        return list(_ACCOUNTS.values())

    def save_invoice(self, invoice):
        _INVOICES.append(invoice)

    def invoices_for(self, account_id):
        return [i for i in _INVOICES if i.account_id == account_id]

    def save_ticket(self, ticket):
        _TICKETS.append(ticket)

    def tickets_for(self, account_id):
        return [t for t in _TICKETS if t.account_id == account_id]
