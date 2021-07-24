import random
from datetime import date, datetime, time,timedelta
import pytz
from django.core.management.base import BaseCommand
from books.models import Book, Purchase
from random import randint


#will use to generate a 3 digit number to act as price of a book
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class Command(BaseCommand):
    help='Populates the db wit random generated data'

    def add_arguments(self, parser):
        parser.add_argument('--amount',type=int, help='The number of purchases that should be created.')

    def handle(self, *args, **kwargs):
        books= [
                'Sapiens',
                'Man’s search for meaning',
                'The War of Art',
                'How to win friends and influence people',
                'Meditation',
                'Shoe Dog',
                'The Predatory Female',
                'The Rationale Male - Religion',
                'The lean startup',
                'In Pursuit of Purpose',
                'The 4 -Hour work week',
                '7 habits of Highly Effective Men',
                'As a Man Thinketh',
                'The Intelligent Investor',
                'How Not To Die',
                'The Manipulated Man',
                'The Lessons of History',
                'Why we eat too much',
                'The Art of War',
                'Can’t hurt me',
                'Made to Stick',
                'Atomic Habits',
                'Homo Deus',
                '12 Rules for Life',
                'The Power of Habit',
                'Good to Great',
                'Why we sleep',
                'The Emperor of All Maladies',
                'Why Nations Fail',
                'Blood and Oil'
                ]
        authors=[
                'Yuval Harari',
                'Viktor Frankl',
                'Steven Pressfield',
                'Dale Carnegie',
                'Marcus Aurelius',
                'Phil Knight',
                'Lawrence Shannon',
                'Rollo Tomassi',
                'Eric Ries',
                'Myles Munroe',
                'Tim Ferris',
                'Stephen R Covey',
                'James Allen',
                'Benjamin Graham',
                'Dr. Michael Greger',
                'Esther Vilar',
                'Will & Ariel Durant',
                'Dr. Andrew Jenkinson',
                'Sun Tzu',
                'David Goggins',
                'Chip Heath & Dan Heath',
                'James Clear',
                'Noah Harari',
                'Jordan B Peterson',
                'Charles Duhigg',
                'Jim Collins',
                'Matthew Walker',
                'Siddhartha Mukherjee',
                'Daron Acemoglu & James Robinson',
                'Bradley Hope & Justin Scheck',
                ]
        prices=[]
        customers=['Nick','Kibet','Vin','Lyn','Mary','John','Dan','Doro']
        for i in range(31):
            price=random_with_N_digits(3)
            prices.append(price)
        book_list=[]
        for book, author, price in zip(books, authors, prices):
            x=Book.objects.get_or_create(
                title=book,
                author=author,
                price=price
            )
            book_list.append(x)
            print(book_list)
        amount=kwargs['amount'] if kwargs['amount'] else 150
        for i in range(0, amount):
            dt=pytz.utc.localize(datetime.now() - timedelta(days=random.randint(0, 1200)))
            purchase = Purchase.objects.create(
                customer=random.choice(customers),
                book=random.choice(book_list)[0],
                payment_method=random.choice(Purchase.PAYMENT_METHODS)[0],
                is_successful=True if random.randint(1,2)==1 else False

            )
            purchase.time_created=dt
            print(purchase)
            purchase.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Done populating the database'
            )
        )