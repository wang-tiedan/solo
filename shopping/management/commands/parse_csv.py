import os
import csv
from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError
from shopping.models import Category, Product, ProductCategory, User, ProductModification

class Command(BaseCommand):
    help = 'from CSV file import product list to database.'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
            
                # Relative path from the manage.py directory to the CSV files directory
                csv_dir_name = 'shopping_data'
                csv_file_path = os.path.join(settings.BASE_DIR, csv_dir_name)

                # Make sure to join the paths with the CSV filenames correctly
                products_file = os.path.join(csv_file_path, 'Products.csv')
                categories_file = os.path.join(csv_file_path, 'Categories.csv')
                product_categories_file = os.path.join(csv_file_path, 'Product_Categories.csv')
                user_file = os.path.join(csv_file_path, 'Users.csv')
                product_modifications_file = os.path.join(csv_file_path, 'Product_Modifications.csv')
                
                
                def parse_datetime(dt_str):
                    try:
                        # Parse the datetime string into a naive datetime object
                        naive_datetime = datetime.strptime(dt_str, '%Y/%m/%d %H:%M')
                        # Make it timezone-aware
                        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_default_timezone())
                        return aware_datetime
                    except ValueError:
                        raise ValidationError("Date format must be YYYY-MM-DD HH:MM")
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import failed: '+str(e)))
                
        try:
            with transaction.atomic():
                # import categories from csv file
                with open(categories_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # if parent id is empty, set parent id to None
                        parent_id = None if row['Parent ID'] == '' else row['Parent ID']
                        category = Category(
                            category_id=row['Category ID'],
                            name=row['Category Name'],
                            parent_id=parent_id
                        )
                        # save category instance to database
                        category.save()
                        
                self.stdout.write(self.style.SUCCESS('Categories imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import failed: '+str(e)))
                
        try:
            with transaction.atomic():
                # from csv file import categories
                with open(products_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Create Product instance for each row in the CSV
                        product = Product(
                            product_id=row['Product ID'],
                            name=row['Name'],
                            price=row['Price'],
                            description=row['Description'],
                            sku=row['SKU']
                        )
                        # save product instance to database
                        product.save()
                self.stdout.write(self.style.SUCCESS('Products imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import failed: '+str(e)))

        try:
            with transaction.atomic():
                # from csv file import product categories, modification records, and save to database.
                with open(product_categories_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        product_category = ProductCategory(
                            association_id=row['Association ID'],
                            product_id=row['Product ID'],
                            category_id=row['Category ID']
                        )
                        # save product class to database
                        product_category.save()
                self.stdout.write(self.style.SUCCESS('ProductCategories imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import failed: '+str(e)))

        try:
            with transaction.atomic():
                # from csv file import product modification records, and save to database.
                with open(product_modifications_file, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        modification = ProductModification(
                            modification_id=row['Modification ID'],
                            product_id=row['Product ID'],
                            creation_time=parse_datetime(row['Creation Time']),
                            creator_id=row['Creator ID'],
                            last_modified_time=parse_datetime(row['Last Modified Time']),
                            last_modified_by_id=row['Last Modified By ID']
                        )
                        # save product revise recording to database
                        modification.save()
                self.stdout.write(self.style.SUCCESS('ProductModifications imported successfully'))

                # output success message
                self.stdout.write(self.style.SUCCESS('All data imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Data import failed: '+str(e)))