# Generated by Django 3.1.2 on 2021-04-13 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20210104_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalDetails',
            fields=[
                ('add_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_diff', models.CharField(max_length=1)),
                ('cust_name', models.CharField(max_length=25)),
                ('cust_type', models.CharField(max_length=25)),
                ('inc_holder', models.CharField(max_length=3)),
                ('prop_owner', models.CharField(max_length=3)),
                ('applicant_type', models.CharField(max_length=25)),
                ('relation', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PropertyDetails',
            fields=[
                ('prop_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('prop_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='leads',
            name='sub_product',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='StudentExistingLoanDetails',
            fields=[
                ('loan_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('product', models.CharField(max_length=10)),
                ('loan_amt', models.CharField(max_length=10)),
                ('emi', models.CharField(max_length=10)),
                ('roi', models.CharField(max_length=3)),
                ('tenure', models.CharField(max_length=3)),
                ('emi_start_date', models.DateField()),
                ('emi_end_date', models.DateField()),
                ('outstanding_paid', models.CharField(max_length=10)),
                ('outstanding_amt', models.CharField(max_length=10)),
                ('any_bounce', models.CharField(max_length=10)),
                ('moratorium_taken', models.CharField(max_length=10)),
                ('applicant_type', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='StudentExistingCardDetails',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('credit_limit', models.CharField(max_length=20)),
                ('limit_utilized', models.CharField(max_length=20)),
                ('min_due', models.CharField(max_length=20)),
                ('card_age', models.CharField(max_length=3)),
                ('pay_delay', models.CharField(max_length=5)),
                ('pay_delay_year', models.CharField(max_length=20)),
                ('moratorium_taken', models.CharField(max_length=20)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField()),
                ('age', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=10)),
                ('alt_phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=6)),
                ('location', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('pincode', models.CharField(max_length=6)),
                ('nationality', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('end_use', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalOtherIncomes',
            fields=[
                ('inc_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('rental_income', models.CharField(max_length=10)),
                ('Lessee_Type', models.CharField(max_length=50)),
                ('Lessee_Name', models.CharField(max_length=50)),
                ('rent_amount', models.CharField(max_length=10)),
                ('tenure_of_arguement', models.CharField(max_length=10)),
                ('tenure_pending', models.CharField(max_length=10)),
                ('valid_rent_agreement', models.CharField(max_length=10)),
                ('Will_u_make_agreement', models.CharField(max_length=10)),
                ('How_old_is_agreement', models.CharField(max_length=50)),
                ('agreement_Type', models.CharField(max_length=50)),
                ('reflection_in_bank_acc', models.CharField(max_length=10)),
                ('reflection_in_ITR_acc', models.CharField(max_length=100)),
                ('extension_expected_in_years', models.CharField(max_length=70)),
                ('addi_details_id_other_inc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalIncomeDetails',
            fields=[
                ('inc_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('salaryType', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=70)),
                ('gross_sal', models.CharField(max_length=10)),
                ('net_sal', models.CharField(max_length=10)),
                ('bonusType', models.CharField(max_length=50)),
                ('bonus_amt', models.CharField(max_length=10)),
                ('incentivesType', models.CharField(max_length=50)),
                ('incentive_amt', models.CharField(max_length=10)),
                ('addi_details_id_inc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalExistingLoanDetails',
            fields=[
                ('existing_loan_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=50)),
                ('products', models.CharField(max_length=100)),
                ('loan_amount', models.CharField(max_length=10)),
                ('emi', models.CharField(max_length=10)),
                ('rate_of_interest', models.CharField(max_length=5)),
                ('tenure', models.CharField(max_length=50)),
                ('emi_start_date', models.CharField(max_length=50)),
                ('emi_end_date', models.CharField(max_length=50)),
                ('outstan_paid_by_customer', models.CharField(max_length=10)),
                ('outstanding_amount', models.CharField(max_length=10)),
                ('any_bounces', models.CharField(max_length=50)),
                ('moratorium_taken', models.CharField(max_length=10)),
                ('application_type', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalExistingCardDetails',
            fields=[
                ('existing_card_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_bank_name', models.CharField(max_length=50)),
                ('credit_limit', models.CharField(max_length=100)),
                ('limit_utilized', models.CharField(max_length=10)),
                ('min_due', models.CharField(max_length=10)),
                ('credit_card_age', models.CharField(max_length=5)),
                ('payment_delay', models.CharField(max_length=50)),
                ('payment_delay_year', models.CharField(max_length=50)),
                ('mor_taken', models.CharField(max_length=50)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalCompanyDetails',
            fields=[
                ('comp_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('comp_type', models.CharField(max_length=50)),
                ('comp_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('paid_up_cap', models.CharField(max_length=10)),
                ('comp_age', models.CharField(max_length=3)),
                ('nature_business', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=50)),
                ('des_type', models.CharField(max_length=50)),
                ('curr_exp', models.CharField(max_length=3)),
                ('total_exp', models.CharField(max_length=3)),
                ('emp_type', models.CharField(max_length=50)),
                ('form16', models.CharField(max_length=3)),
                ('office_phone', models.CharField(max_length=11)),
                ('office_email', models.CharField(max_length=50)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalAdditonalOtherIncome',
            fields=[
                ('inc_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('other_income', models.CharField(max_length=50)),
                ('income_amount', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='SalAdditionalDetails',
            fields=[
                ('sal_add_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('inw_cheque_return', models.CharField(max_length=50)),
                ('loan_enq_disburse', models.CharField(max_length=100)),
                ('loan_enq_det', models.CharField(max_length=100)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredResidenceDetails',
            fields=[
                ('res_id', models.AutoField(primary_key=True, serialize=False)),
                ('res_type', models.CharField(max_length=50)),
                ('current_location', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredPensionDetails',
            fields=[
                ('pension_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=50)),
                ('net_pension', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredOtherDetails',
            fields=[
                ('other_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('inward_cheque', models.CharField(max_length=30)),
                ('multiple_enquiry', models.CharField(max_length=30)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredInvestmentDetails',
            fields=[
                ('invest_id', models.AutoField(primary_key=True, serialize=False)),
                ('investment', models.CharField(max_length=30)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredExistingLoanDetails',
            fields=[
                ('loan_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('product', models.CharField(max_length=10)),
                ('loan_amt', models.CharField(max_length=10)),
                ('emi', models.CharField(max_length=10)),
                ('roi', models.CharField(max_length=3)),
                ('tenure', models.CharField(max_length=3)),
                ('emi_start_date', models.DateField()),
                ('emi_end_date', models.DateField()),
                ('outstanding_paid', models.CharField(max_length=10)),
                ('outstanding_amt', models.CharField(max_length=10)),
                ('any_bounce', models.CharField(max_length=10)),
                ('moratorium_taken', models.CharField(max_length=10)),
                ('applicant_type', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredExistingCardDetails',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('credit_limit', models.CharField(max_length=20)),
                ('limit_utilized', models.CharField(max_length=20)),
                ('min_due', models.CharField(max_length=20)),
                ('card_age', models.CharField(max_length=3)),
                ('pay_delay', models.CharField(max_length=5)),
                ('pay_delay_year', models.CharField(max_length=20)),
                ('moratorium_taken', models.CharField(max_length=20)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='RetiredDetails',
            fields=[
                ('retired_id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField()),
                ('age', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=10)),
                ('alt_phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('pincode', models.CharField(max_length=6)),
                ('nationality', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('end_use', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='PropType3',
            fields=[
                ('prop_id', models.AutoField(primary_key=True, serialize=False)),
                ('bnk_name', models.CharField(max_length=30)),
                ('prod_services', models.CharField(max_length=30)),
                ('loan_amt', models.CharField(max_length=10)),
                ('emi', models.CharField(max_length=10)),
                ('outstanding_amt', models.CharField(max_length=10)),
                ('tenure', models.CharField(max_length=3)),
                ('foreclosure', models.CharField(max_length=3)),
                ('lod', models.CharField(max_length=30)),
                ('prop_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.propertydetails')),
            ],
        ),
        migrations.CreateModel(
            name='PropType2',
            fields=[
                ('prop_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=30)),
                ('finance_approved_by', models.CharField(max_length=30)),
                ('building_age', models.CharField(max_length=30)),
                ('agree_val', models.CharField(max_length=10)),
                ('mkt_val', models.CharField(max_length=10)),
                ('property_loc', models.CharField(max_length=30)),
                ('property_city', models.CharField(max_length=30)),
                ('property_state', models.CharField(max_length=30)),
                ('cc_available', models.CharField(max_length=3)),
                ('oc_available', models.CharField(max_length=3)),
                ('mun_approved', models.CharField(max_length=3)),
                ('areasize', models.CharField(max_length=10)),
                ('areain', models.CharField(max_length=30)),
                ('areatype', models.CharField(max_length=30)),
                ('property_type', models.CharField(max_length=10)),
                ('agree_type', models.CharField(max_length=30)),
                ('stp_duty', models.CharField(max_length=30)),
                ('prev_agree_available', models.CharField(max_length=3)),
                ('dup_available_or_notice', models.CharField(max_length=10)),
                ('reg_prev_agreement', models.CharField(max_length=3)),
                ('con_area', models.CharField(max_length=30)),
                ('payment_till_date', models.CharField(max_length=10)),
                ('prop_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.propertydetails')),
            ],
        ),
        migrations.CreateModel(
            name='PropType1',
            fields=[
                ('prop_id', models.AutoField(primary_key=True, serialize=False)),
                ('builder_name', models.CharField(max_length=50)),
                ('proj_name', models.CharField(max_length=50)),
                ('apf_num', models.CharField(max_length=50)),
                ('apf_approved_lender', models.CharField(max_length=50)),
                ('const_stage', models.CharField(max_length=50)),
                ('per_complete', models.CharField(max_length=3)),
                ('possession_date', models.DateField()),
                ('total_floors', models.CharField(max_length=3)),
                ('buy_floor', models.CharField(max_length=3)),
                ('slabs_done', models.CharField(max_length=2)),
                ('agreement_val', models.CharField(max_length=50)),
                ('market_val', models.CharField(max_length=50)),
                ('prop_loc', models.CharField(max_length=50)),
                ('prop_city', models.CharField(max_length=50)),
                ('prop_state', models.CharField(max_length=50)),
                ('prop_in', models.CharField(max_length=50)),
                ('cc_rec', models.CharField(max_length=3)),
                ('cc_rec_upto', models.CharField(max_length=3)),
                ('municipal_approved', models.CharField(max_length=3)),
                ('area_size', models.CharField(max_length=5)),
                ('area_in', models.CharField(max_length=10)),
                ('area_type', models.CharField(max_length=15)),
                ('room_type', models.CharField(max_length=15)),
                ('agreement_type', models.CharField(max_length=50)),
                ('pay_till_date', models.CharField(max_length=10)),
                ('stamp_duty', models.CharField(max_length=3)),
                ('stamp_duty_amt', models.CharField(max_length=10)),
                ('cost_sheet', models.CharField(max_length=3)),
                ('cost_sheet_amt', models.CharField(max_length=7)),
                ('prop_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.propertydetails')),
            ],
        ),
        migrations.AddField(
            model_name='propertydetails',
            name='lead_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.leads'),
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('per_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_amt', models.CharField(max_length=10, null=True)),
                ('cibil_type', models.CharField(max_length=50)),
                ('cibil_score', models.CharField(max_length=20)),
                ('loanTaken', models.CharField(max_length=3, null=True)),
                ('repaymentHistory', models.CharField(max_length=20)),
                ('defaultYear', models.CharField(max_length=50)),
                ('details_bout_default', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=20)),
                ('dob', models.DateField(null=True)),
                ('age', models.CharField(max_length=3, null=True)),
                ('retire_age', models.CharField(max_length=3)),
                ('maritalStatus', models.CharField(max_length=50)),
                ('qualification', models.CharField(max_length=50)),
                ('degree_others', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=50)),
                ('lawyerType', models.CharField(max_length=50)),
                ('nationality', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('enduse', models.CharField(max_length=100)),
                ('addi_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='Investments',
            fields=[
                ('sal_inv_id', models.AutoField(primary_key=True, serialize=False)),
                ('investments_u_have', models.CharField(max_length=50)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='HousewifePersonalDetails',
            fields=[
                ('hw_per_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_Amt', models.CharField(max_length=10)),
                ('cibil_type', models.CharField(max_length=10)),
                ('cibil_score', models.CharField(max_length=10)),
                ('loan_cc', models.CharField(max_length=10)),
                ('repayment_history', models.CharField(max_length=10)),
                ('default_year', models.CharField(max_length=10)),
                ('details_default', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='HousewifeInvestmentDetails',
            fields=[
                ('invest_id', models.AutoField(primary_key=True, serialize=False)),
                ('investment', models.CharField(max_length=30)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='HousewifeExistingLoanDetails',
            fields=[
                ('loan_det_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('product', models.CharField(max_length=10)),
                ('loan_amt', models.CharField(max_length=10)),
                ('emi', models.CharField(max_length=10)),
                ('roi', models.CharField(max_length=3)),
                ('tenure', models.CharField(max_length=3)),
                ('emi_start_date', models.DateField()),
                ('emi_end_date', models.DateField()),
                ('outstanding_paid', models.CharField(max_length=10)),
                ('outstanding_amt', models.CharField(max_length=10)),
                ('any_bounce', models.CharField(max_length=10)),
                ('moratorium_taken', models.CharField(max_length=10)),
                ('applicant_type', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='HousewifeExistingCardDetails',
            fields=[
                ('card_id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=20)),
                ('credit_limit', models.CharField(max_length=20)),
                ('limit_utilized', models.CharField(max_length=20)),
                ('min_due', models.CharField(max_length=20)),
                ('card_age', models.CharField(max_length=3)),
                ('pay_delay', models.CharField(max_length=5)),
                ('pay_delay_year', models.CharField(max_length=20)),
                ('moratorium_taken', models.CharField(max_length=20)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='HousewifeDetails',
            fields=[
                ('hw_id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField()),
                ('age', models.CharField(max_length=3)),
                ('phone', models.CharField(max_length=10)),
                ('alt_phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=6)),
                ('address', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('pincode', models.CharField(max_length=6)),
                ('nationality', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('end_use', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('con_id', models.AutoField(primary_key=True, serialize=False)),
                ('con_person', models.CharField(max_length=25)),
                ('con_phone', models.CharField(max_length=10)),
                ('add_det_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.additionaldetails')),
            ],
        ),
        migrations.AddField(
            model_name='additionaldetails',
            name='lead_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.leads'),
        ),
    ]
