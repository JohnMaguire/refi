#!/bin/python
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

# Assumptions
property_value = 300000
original_loan = 291030
original_loan_outstanding = 282685.11
original_loan_rate = 4.625
original_loan_lifetime_years = 30
original_loan_monthly_payment = 1491.16  # calculated if None
new_loan = None  # defaults to original_loan_outstanding
new_loan_rate = 3.091
new_loan_lifetime_years = 30
new_loan_closing_costs_rate = 3.0

# Don't edit past this line
def monthly_payment(amount, rate, lifetime_months):
    i = rate / 12
    n = lifetime_months
    return amount * (
        i * ((1+i) ** n) / (((1+i) ** n) - 1)
    )

def amoritization_schedule(amount, rate, monthly_payment):
    i = 1
    while amount > 0:
        principal = monthly_payment - (amount * rate / 12)
        interest = monthly_payment - principal
        amount = amount - principal
        if amount < 0.01:
            interest += amount
            monthly_payment += amount
            amount = 0
        # payment #, payment, principal, interest, balance
        yield (i, monthly_payment, principal, interest, amount)

        i += 1

def amoritization_schedule_table(title, amount, rate, monthly_payment):
    table = Table(title=title, show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=4)
    table.add_column("Payment")
    table.add_column("Principal", style="red")
    table.add_column("Interest", style="red")
    table.add_column("Balance")

    for payment in amoritization_schedule(
            amount,
            rate,
            monthly_payment,
    ):
        table.add_row("{}".format(payment[0]),
                      "${:,.2f}".format(payment[1]),
                      "-${:,.2f}".format(payment[2]),
                      "-${:,.2f}".format(payment[3]),
                      "${:,.2f}".format(payment[4]),
        )

    return table


original_loan_rate *= .01
original_loan_lifetime_months = original_loan_lifetime_years * 12
new_loan = new_loan or original_loan_outstanding
new_loan_rate *=.01
new_loan_lifetime_months = new_loan_lifetime_years * 12
new_loan_closing_costs_rate *= .01
new_loan_closing_costs = new_loan * new_loan_closing_costs_rate

new_loan_monthly_payment = monthly_payment(
    new_loan,
    new_loan_rate,
    new_loan_lifetime_months,
)

original_loan_monthly_payment = original_loan_monthly_payment or \
    monthly_payment(
        original_loan,
        original_loan_rate,
        original_loan_lifetime_months,
    )

console = Console()

assumptions_table = Table(title="Assumptions", show_header=False)
assumptions_table.add_row("[bold white]Original Loan[/bold white]", "${:,.2f} @ {:,.3f}% (${:,.2f}/mo)".format(
    original_loan,
    original_loan_rate * 100,
    original_loan_monthly_payment,
))
assumptions_table.add_row("[bold white]New Loan[/bold white]", "${:,.2f} @ {:,.3f}% (Assuming ${:,.2f}/mo)".format(
    new_loan,
    new_loan_rate * 100,
    new_loan_monthly_payment,
))
assumptions_table.add_row("[bold white]New Loan Closing Costs[bold white]", "${:,.2f} (Assuming {:,.2f}%)".format(
    new_loan_closing_costs,
    new_loan_closing_costs_rate * 100,
))

original_loan_table = amoritization_schedule_table(
    "Original Loan Amoritization",
    original_loan_outstanding,
    original_loan_rate,
    original_loan_monthly_payment,
)

new_loan_table = amoritization_schedule_table(
    "New Loan Amoritization",
    new_loan,
    new_loan_rate,
    new_loan_monthly_payment,
)

console.print(assumptions_table)
console.print(Columns([original_loan_table, new_loan_table]))
