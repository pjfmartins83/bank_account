# Generated by Django 4.0.10 on 2024-07-15 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_email_bankaccount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'verbose_name': 'Bank Account', 'verbose_name_plural': 'Bank Accounts'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Custom User', 'verbose_name_plural': 'Custom Users'},
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw')], default='Deposit', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BankAccount')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            }
        ),
    ]
