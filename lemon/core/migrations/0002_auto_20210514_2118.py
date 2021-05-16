# Generated by Django 3.2 on 2021-05-14 15:18

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0002_auto_20210514_2118'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='Ключ')),
                ('value', models.CharField(max_length=50, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Характеристика продукта',
                'verbose_name_plural': 'Характеристики продукта',
            },
        ),
        migrations.RemoveField(
            model_name='clothes',
            name='product_ptr',
        ),
        migrations.RemoveField(
            model_name='shoes',
            name='product_ptr',
        ),
        migrations.RemoveField(
            model_name='category',
            name='type',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='product',
            name='in_top',
            field=models.BooleanField(default=False, verbose_name='В топе?'),
        ),
        migrations.AddField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sub_categories', to='core.category', verbose_name='Родитель категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='core.brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='src',
            field=models.ImageField(upload_to='images/promotions'),
        ),
        migrations.DeleteModel(
            name='Accessories',
        ),
        migrations.DeleteModel(
            name='Clothes',
        ),
        migrations.DeleteModel(
            name='Shoes',
        ),
        migrations.AddField(
            model_name='productspecification',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='core.product', verbose_name='Продукт'),
        ),
    ]