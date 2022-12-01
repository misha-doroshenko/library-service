import datetime


from django.db import models

from books.models import Book
from library import settings


def default_expected_date(days: int):
    date_of_borrowed = datetime.date.today()
    return date_of_borrowed + datetime.timedelta(days)


class Borrowing(models.Model):
    OVERDUE_COEFFICIENT = 2
    MAX_TERM = 7
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(
        default=default_expected_date(MAX_TERM)
    )
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings",
    )

    def __str__(self):
        return (
            f"{self.book.title} was borrow {self.borrow_date}"
            f" expected return {self.expected_return_date}"
        )

    @property
    def expected_price(self):
        return self.MAX_TERM * self.book.daily_fee

    @property
    def overdue(self):
        overdue = self.actual_return_date - self.expected_return_date
        if overdue.days > 0:
            return (
                overdue.days * self.book.daily_fee * self.OVERDUE_COEFFICIENT
            )
