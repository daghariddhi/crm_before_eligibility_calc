from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import auth
from .models import CustomUser, Leads, AdditionalDetails, ContactPerson, PersonalDetails, SalIncomeDetails, SalOtherIncomes, SalAdditonalOtherIncome, SalCompanyDetails, SalExistingLoanDetails, SalExistingCardDetails, SalAdditionalDetails, Investments
from .models import PropertyDetails, PropType1, PropType2, PropType3
from .models import StudentDetails,StudentExistingCardDetails, StudentExistingLoanDetails
from .models import HousewifeDetails, HousewifePersonalDetails, HousewifeExistingLoanDetails, HousewifeExistingCardDetails, HousewifeInvestmentDetails  
from .models import RetiredDetails, RetiredPensionDetails, RetiredResidenceDetails, RetiredExistingLoanDetails, RetiredExistingCardDetails, RetiredInvestmentDetails, RetiredOtherDetails
from master.models import *
from django.contrib import messages
from django.conf import settings 
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator, render_to_pdf
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Case, When
from django.http import FileResponse, Http404
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from django.core.files import File
import json
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
# def random_password(size=8):
#     return BaseUserManager().make_random_password(size)
from leadgenerator.settings import EMAIL_HOST_USER


def register(request):
    if request.method == 'POST':
        
        fname = request.POST['fname']
        Email = request.POST['email']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        designation = request.POST['designation']
        if(designation == "Other"):
            designation = request.POST['other']
        address = request.POST['address']
        role = "Referral Partner"
        mapped_to = "admin"
        mapped_to_nm = "admin"
        by_online = "yes"

        if CustomUser.objects.filter(email=Email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')
        else:
            
            user = CustomUser.objects.create_user(username=Email, password="", email=Email, first_name=fname, phone=phone, alt_phone=alt_phone, designation=designation, address=address, role = role, mapped_to = mapped_to, mapped_to_name = mapped_to_nm, by_online = by_online)
            user.is_active = False
            user.save()
            ini = ""
            if user.designation == "Salaried":
                ini += "SAL"
            elif user.designation == "Self Employed":
                ini += "SE"
            elif user.designation == "Freelancer":
                ini += "FL"
            elif user.designation == "Student":
                ini += "ST"
            elif user.designation == "Home Maker":
                ini += "HM"
            elif user.designation == "DSA":
                ini += "DSA"
            elif user.designation == "Insurance Agent":
                ini += "IA"
            elif user.designation == "Chartered Accountant":
                ini += "CA"
            elif user.designation == "Tax Consultants":
                ini += "TC"
            elif user.designation == "Banker":
                ini += "BNK"
            elif user.designation == "Company Secretary":
                ini += "CS"
            elif user.designation == "Real Estate Agent":
                ini += "REA"
            elif user.designation == "Builder":
                ini += "BLD"
            else:
                ini+="O"

            if user.role == "Referral Partner":
                ini += "RP"

            num = '{:04d}'.format(user.id)
            newusername = ini+num
            user.username = newusername
            user.save()


            # if user.role == "Referral Partner":
            #     ini = "ORP"
            #     num = '{:03d}'.format(user.id)
            #     newusername = ini+num
            #     user.username = newusername
            #     user.save()
            

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = "http://"+domain+link
            email_body = 'Hi ' + user.first_name + ' Please use this link to verify your account\n'+ activate_url
            email = EmailMessage(
                'Activate your account',
                email_body,
                'rohan@gmail.com',
                [Email],
            )
            email.send(fail_silently=False)

            template = get_template('account/Agreement.html')
            context = {
            "partner_name" : user.first_name
            }
            html = template.render(context)
            pdf = render_to_pdf('account/Agreement.html', context)

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Agreement_%s.pdf" %(user.username)
            content = "attachment; filename='%s'" %(filename)
            # response['Content-Disposition'] = content
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            


            user.agreement.save(filename, File(BytesIO(pdf.content)))

            message="this is test mail"
            subject="terms and conditions"
            mail_id=request.POST.get('email','')
            # mail_id="daghariddhi12@gmail.com"
    
            email=EmailMessage(subject,message, EMAIL_HOST_USER, [mail_id,])
            email.content_subtype='html'

            # file2=open("abcd.txt","r")
            # file=open("manage.py","r")
            # email.attach("abcd.txt",file2.read(),'text/plain')
            # email.attach("manage.py",file.read(), 'text/plain')
            email.attach_file('D:/crm_internship/final_crms/final_crm1/abc.pdf')

            email.send()
            # return render(request, 'account/terms.html')
            
            
        #else:
            #messages.info(request, 'Password did not match')
            #return redirect('register')

            return redirect('email_ver_msg')


        #else:
            #messages.info(request, 'Password did not match')
            #return redirect('register')
    else:    
        return render(request, 'account/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('uname_pw_gen')
            user.is_active = True
            password = BaseUserManager().make_random_password(10)
            user.set_password(password)
            user.save()
            email_body = 'Hi ' + user.first_name+' \n Your username: '+ user.username+ '\n Your Password: '+password
            email = EmailMessage(
                'Account Activated',
                email_body,
                'rohan@gmail.com',
                [user.email],
            )
            email.send(fail_silently=False)
            

            messages.success(request, 'Account activated successfully')
            return redirect('uname_pw_gen')

        except Exception as ex:
            pass

        return redirect('uname_pw_gen')

def email_ver_msg(request):
    return render(request, 'account/email_ver_msg.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            
            auth.login(request, user)
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')

    else:
        return render(request, 'account/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def forgot_uname(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            p = CustomUser.objects.raw('SELECT * FROM account_customuser WHERE email = %s', [email])
            subject = 'Request for username'
            message = f'Hi Your Username is: {p[0].username}'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list ) 
            return redirect('login')
        else:
            messages.info(request, 'Email not registered')
            return redirect('forgot_uname')
    else:
        return render(request, 'account/forgot_uname.html')

def uname_pw_gen(request):
    return render(request, 'account/uname_pw_gen.html')
    
@login_required (redirect_field_name='login', login_url='login')
def add_leads(request):
    if request.method == 'POST':
        name = request.POST['name']
        ref = request.POST['ref']
        #username = request.POST['username']
        email = request.POST['email']
        #password1 = request.POST['password1']
        #password2 = request.POST['password2']
        product = request.POST['pdt']
        sub_product = request.POST['subpdt']
        loan_amt = request.POST['amt']
        address = request.POST['address']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        added_by = request.user.id
        user = request.user

        lead = Leads(name = name, phone = phone, alt_phone = alt_phone, email = email, reference = ref, product = product, sub_product = sub_product, loan_amt = loan_amt, address = address, pincode = pincode, country = country, state = state, city= city, added_by = added_by )
        lead.save()





        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')

            elif user.role == "Referral Partner":
                return redirect('base')
        if 'next' in request.POST:
            return redirect(f"additionaldetails/{lead.lead_id}") # additionaldetails/20

    products = Product.objects.all()
    subproducts = SubProduct.objects.all()
    subproductdict = dict()
    for subproduct in subproducts:
        if subproduct.product.id in subproductdict:
            subproductdict[subproduct.product.id].append({
                'id':subproduct.id,
                'sub_product':subproduct.sub_product,
                'effective_date': subproduct.effective_date,
                'ineffective_date': subproduct.ineffective_date
            })
        else :
            subproductdict[subproduct.product.id] = []
            subproductdict[subproduct.product.id].append({
                'id':subproduct.id,
                'sub_product':subproduct.sub_product,
                'effective_date': subproduct.effective_date,
                'ineffective_date': subproduct.ineffective_date
            })
    # print(json.dumps(subproductdict))
    context = {
        'products': products,
        'subproducts': json.dumps(subproductdict)
    }
    return render(request, 'account/add_leads.html', context=context)

 
def create_mem(request):

    if request.method == 'POST':
        
        fname = request.POST['name']
        Email = request.POST['email']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        designation = request.POST['designation']
        address = request.POST['address']
        role = request.POST['role']
        mapped_to = request.POST['mapped_to']
        mapped_to_nm = request.POST['mapped_to_nm']
        by_online = "no"

        if CustomUser.objects.filter(email=Email).exists():
            messages.info(request, 'Email Taken')
            return redirect('create_mem')
        else:
            password = BaseUserManager().make_random_password(10)
            user = CustomUser.objects.create_user(username=Email, password=password, email=Email, first_name=fname, phone=phone, alt_phone=alt_phone, designation=designation, address=address, role = role, mapped_to = mapped_to, mapped_to_name = mapped_to_nm, by_online = by_online)
            user.save()


            ini = ""
            if user.designation == "Salaried":
                ini += "SAL"
            elif user.designation == "Self Employed":
                ini += "SE"
            elif user.designation == "Freelancer":
                ini += "FL"
            elif user.designation == "Student":
                ini += "ST"
            elif user.designation == "Home Maker":
                ini += "HM"
            elif user.designation == "DSA":
                ini += "DSA"
            elif user.designation == "Insurance Agent":
                ini += "IA"
            elif user.designation == "Chartered Accountant":
                ini += "CA"
            elif user.designation == "Tax Consultants":
                ini += "TC"
            elif user.designation == "Banker":
                ini += "BNK"
            elif user.designation == "Company Secretary":
                ini += "CS"
            elif user.designation == "Real Estate Agent":
                ini += "REA"
            elif user.designation == "Builder":
                ini += "BLD"
            else:
                ini+="O"

            if user.role == "Referral Partner":
                ini += "RP"

            elif user.role == "Branch User":
                ini += "BU"

            elif user.role == "Business Associates":
                ini += "BA"
            
            elif user.role == "Business Partner":
                ini += "BP"

            elif user.role == "Coordinator":
                ini += "CO"

            elif user.role == "Creative Finserver Center":
                ini += "CFC"

            elif user.role == "Development Partner":
                ini += "DP"

            elif user.role == "Doc boy":
                ini += "DB"
            
            elif user.role == "Execution Partner":
                ini += "EP"

            elif user.role == "Execution team internal":
                ini += "ETI"

            elif user.role == "Field executive":
                ini += "FE"
            
            elif user.role == "Referral Agent":
                ini += "RA"

            elif user.role == "Relationship manager":
                ini += "RM"

            elif user.role == "Secured Vertical Head":
                ini += "SVH"
            
            elif user.role == "Sr. Development Partner":
                ini += "SDP"

            elif user.role == "Team Manager":
                ini += "TM"
            
            elif user.role == "Tele Sales":
                ini += "TS"

            elif user.role == "Users":
                ini += "Us"
    
            elif user.role == "Vertical Head":
                ini += "VH"
                 


            num = '{:04d}'.format(user.id)
            newusername = ini+num
            user.username = newusername
            user.save()


            # if user.role == "Referral Partner":
            #     ini = "ORP"
            #     num = '{:03d}'.format(user.id)
            #     newusername = ini+num
            #     user.username = newusername
            #     user.save()

            email_body = 'Hi ' + user.first_name+' \n Your username: '+ user.username+ '\n Your Password: '+ password
            email = EmailMessage(
                'Account Activated',
                email_body,
                '',
                [user.email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Account Created successfully')
            if request.user.role == "Admin":
            # return render(request, 'account/dashboard.html')
                return redirect('dashboard')

            elif request.user.role == "Referral Partner":
            # return render(request, 'account/base.html')
                return redirect('base')
            
    return render(request, 'account/create_mem.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def base(request):
    return render(request, 'account/base.html')

def list_leads(request):
    if request.user.role == "Admin":
        ll = Leads.objects.all()
    elif request.user.role == "Referral Partner":  
        ll = Leads.objects.filter(added_by=str(request.user.id))
    ids = []
    for i in ll:
        ids.append(i.lead_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    listleads = Leads.objects.filter(lead_id__in=ids).order_by(preserved)   
    # return render(request, 'music/songs.html',  {'song': song})
    return render(request, 'account/list_leads.html', {'listleads': listleads})

def terms(request):
    try:
        return FileResponse(open('terms.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def additionaldetails(request,id):
    if request.method == 'POST':
        user = request.user
        lead = Leads.objects.filter(lead_id=id).first()

        con_person = request.POST['con_person']
        con_phone = request.POST['con_phone']
        name = request.POST['name']
        incomeHolder = request.POST['incomeHolder']
        propertyOwner = request.POST['propertyOwner']
        applicantType = request.POST['applicantType']
        relation = request.POST['relation']
        customerType = request.POST['customerType']

        if con_person != "":
            add1 = AdditionalDetails(is_diff="Y", cust_name = name, inc_holder = incomeHolder, prop_owner = propertyOwner, 
                                     applicant_type = applicantType, relation = relation, cust_type = customerType, lead_id = lead)
            add1.save()

            con = ContactPerson(con_person = con_person, con_phone = con_phone, add_det_id = add1)
            con.save()
            

        name_1 = request.POST.getlist('name_1')
        incomeHolder_1 = request.POST.getlist('incomeHolder_1')
        propertyOwner_1 = request.POST.getlist('propertyOwner_1')
        applicantType_1 = request.POST.getlist('applicantType_1')
        relation_1 = request.POST.getlist('relation_1')
        customerType_1 = request.POST.getlist('customerType_1')
            
        if name_1 != "":
            for (a,b,c,d,e,f) in zip(name_1, incomeHolder_1, propertyOwner_1, applicantType_1, relation_1, customerType_1):
                add2 = AdditionalDetails(is_diff="N", cust_name = a, 
                                     inc_holder = b, prop_owner = c, applicant_type = d,
                                     relation = e, cust_type = f, lead_id = lead)
                add2.save()

        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')

            elif user.role == "Referral Partner":
                return redirect('base')

        if 'next' in request.POST:
            nxt = AdditionalDetails.objects.filter(lead_id = lead.lead_id, applicant_type = "Applicant").first()
            cust_type = nxt.cust_type.lower()
            return redirect(f"/account/{cust_type}/{nxt.add_det_id}")


    lead = Leads.objects.filter(lead_id=id) # list of objects
    customertypes = CustomerType.objects.all()
    applicanttypes =  ApplicantType.objects.all()
    return render(request, 'account/Additional_Details.html', {'customertypes': customertypes, 'applicanttypes':applicanttypes, 'lead':lead[0]})

def housewife(request, id):

    if request.method == 'POST':
        user = request.user
        add = AdditionalDetails.objects.filter(add_det_id=id).first()

        dob = request.POST['dob']
        age = request.POST['age']
        phone = request.POST['mobile_no']
        alt_phone = request.POST['alt_mobile']
        email = request.POST['email']
        gender = request.POST['gender']
        location = request.POST['address']
        state = request.POST['state']
        pincode = request.POST['pincode']
        nationality = request.POST['nationality']
        country = request.POST['country']
        end_use = request.POST['end_use']
        hw_det = HousewifeDetails(dob=dob, age=age, phone=phone, alt_phone=alt_phone, email=email, gender=gender, address=location,
                                  state=state, pincode=pincode, nationality=nationality, country=country, end_use=end_use, add_det_id=add)
        hw_det.save()

        loan_Amt = request.POST['loan_amt']
        cibil_type = request.POST['cibil_type']
        cibil_score = request.POST['cibil_score']
        loan_cc = request.POST['loan_cc']
        repayment_history = request.POST['repayment_history']
        default_year = request.POST['default_year']
        details_default = request.POST['details_default']

        if loan_Amt != "":
            hw_per_det = HousewifePersonalDetails(loan_Amt = loan_Amt, cibil_type = cibil_type, cibil_score = cibil_score, loan_cc = loan_cc,
                                                  repayment_history = repayment_history, default_year = default_year, 
                                                  details_default = details_default, add_det_id=add)
            hw_per_det.save()

        bank_name = request.POST.getlist('bank_name')
        product = request.POST.getlist('product')
        loan_amts = request.POST.getlist('loan_amts')
        emi = request.POST.getlist('emi')
        roi = request.POST.getlist('roi')
        tenure = request.POST.getlist('tenure')
        emi_start_date = request.POST.getlist('emi_start_date')
        emi_end_date = request.POST.getlist('emi_end_date')
        outstanding_paid = request.POST.getlist('outstanding_paid')
        outstanding_amt = request.POST.getlist('outstanding_amt')
        any_bounce = request.POST.getlist('any_bounce')
        moratorium_taken = request.POST.getlist('moratorium_taken')
        applicant_type = request.POST.getlist('applicant_type')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h,i,j,k,l,m) in zip(bank_name, product, loan_amts, emi, roi, tenure, emi_start_date, emi_end_date, 
                                                  outstanding_paid, outstanding_amt, any_bounce, moratorium_taken, applicant_type):
                
                loan_det = HousewifeExistingLoanDetails(bank_name=a, product=b, loan_amt=c, emi=d, roi=e, tenure=f, emi_start_date=g,
                                                      emi_end_date=h, outstanding_paid=i, outstanding_amt=j, any_bounce=k, 
                                                      moratorium_taken=l, applicant_type=m, add_det_id=add)

                loan_det.save()


        bank_name = request.POST.getlist('bank_name')
        credit_limit = request.POST.getlist('credit_limit')
        limit_utilized = request.POST.getlist('limit_utilized')
        min_due = request.POST.getlist('min_due')
        card_age = request.POST.getlist('card_age')
        pay_delay = request.POST.getlist('pay_delay')
        pay_delay_year = request.POST.getlist('pay_delay_year')
        moratorium_taken = request.POST.getlist('moratorium_taken')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h) in zip(bank_name, credit_limit, limit_utilized, min_due, 
            card_age, pay_delay, pay_delay_year, moratorium_taken):
                
                card_det = HousewifeExistingCardDetails(bank_name=a, credit_limit=b, limit_utilized=c, 
                min_due=d, card_age=e, pay_delay=f, pay_delay_year=g, moratorium_taken=h, add_det_id=add)

                card_det.save()

        investment = request.POST['investment']

        if investment != "":
            inv_det = HousewifeInvestmentDetails(investment = investment, add_det_id = add)
            inv_det.save()



        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')

        if 'next' in request.POST:
            # cust_type = nxt.cust_type.lower()
            # return redirect(f"/account/{cust_type}/{nxt.add_det_id}")
            if add.applicant_type == "Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "1st Co-Applicant").first()
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "1st Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "2nd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "2nd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "3rd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "3rd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "4th Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            else:
                return redirect(f"/account/property_details/{add.lead_id.lead_id}")

    cust = AdditionalDetails.objects.filter(add_det_id=id).first()
    nationalities = Nationality.objects.all()
    products = Product.objects.all()
    applicanttypes =  ApplicantType.objects.all()
    return render(request, 'account/Housewife.html', {'applicanttypes':applicanttypes, 'products':products, 'nationalities':nationalities, 'cust':cust})



def property_details(request,id):

    if request.method == 'POST':
        user = request.user
        lead = Leads.objects.filter(lead_id = id).first()

        prop_type = request.POST['prop_type']
        prop_det = PropertyDetails(prop_type = prop_type, lead_id = lead)
        prop_det.save()

                

        if prop_type == "Underconstruction and Buying From Builder" or prop_type == "Underconstruction and Buying From Seller" or prop_type == "Ready Possession and Buying From Builder":
            builder_name = request.POST['builder_name']
            proj_name = request.POST['proj_name']
            apf_num = request.POST['apf_num']
            apf_approved_lender = request.POST['apf_approved_lender']
            const_stage = request.POST['const_stage']
            per_complete = request.POST['per_complete']
            possession_date = request.POST['possession_date']
            total_floors = request.POST['total_floors']
            buy_floor = request.POST['buy_floor']
            slabs_done = request.POST['slabs_done']
            agreement_val = request.POST['agreement_val']
            market_val = request.POST['market_val']
            prop_loc = request.POST['prop_loc']
            prop_city = request.POST['prop_city']
            prop_state = request.POST['prop_state']
            prop_in = request.POST['prop_in']
            cc_rec = request.POST['cc_rec']
            cc_rec_upto = request.POST['cc_rec_upto']
            municipal_approved = request.POST['municipal_approved']
            area_size = request.POST['area_size']
            area_in = request.POST['area_in']
            area_type = request.POST['area_type']
            room_type = request.POST['room_type']
            agreement_type = request.POST['agreement_type']
            pay_till_date = request.POST['pay_till_date']
            stamp_duty = request.POST['stamp_duty']
            stamp_duty_amt = request.POST['stamp_duty_amt']
            cost_sheet = request.POST['cost_sheet']
            cost_sheet_amt = request.POST['cost_sheet_amt']
            
            prop_det_1 = PropType1(
                builder_name = builder_name,
                proj_name = proj_name,
                apf_num = apf_num,
                apf_approved_lender = apf_approved_lender,
                const_stage = const_stage,
                per_complete = per_complete,
                possession_date = possession_date,
                total_floors = total_floors,
                buy_floor = buy_floor,
                slabs_done = slabs_done,
                agreement_val = agreement_val,
                market_val = market_val,
                prop_loc = prop_loc,
                prop_city = prop_city,
                prop_state = prop_state,
                prop_in = prop_in,
                cc_rec = cc_rec,
                cc_rec_upto = cc_rec_upto,
                municipal_approved = municipal_approved,
                area_size = area_size,
                area_in = area_in,
                area_type = area_type,
                room_type = room_type,
                agreement_type = agreement_type,
                pay_till_date = pay_till_date,
                stamp_duty = stamp_duty,
                stamp_duty_amt = stamp_duty_amt,
                cost_sheet = cost_sheet,
                cost_sheet_amt = cost_sheet_amt,
                prop_det_id = prop_det
            )
            prop_det_1.save()

        if prop_type == "Resale and Buying From Seller":
            project_name = request.POST['project_name']
            finance_approved_by = request.POST['finance_approved_by']
            building_age = request.POST['building_age']
            agree_val = request.POST['agree_val']
            mkt_val = request.POST['mkt_val']
            property_loc = request.POST['property_loc']
            property_city = request.POST['property_city']
            property_state = request.POST['property_state']
            cc_available = request.POST['cc_available']
            oc_available = request.POST['oc_available']
            mun_approved = request.POST['mun_approved']
            areasize = request.POST['areasize']
            areain = request.POST['areain']
            areatype = request.POST['areatype']
            property_type = request.POST['property_type']
            agree_type = request.POST['agree_type']
            stp_duty = request.POST['stp_duty']
            prev_agree_available = request.POST['prev_agree_available']
            dup_available_or_notice = request.POST['dup_available_or_notice']
            reg_prev_agreement = request.POST['reg_prev_agreement']
            con_area = request.POST['con_area']
            payment_till_date = request.POST['payment_till_date']

            prop_det_2 = PropType2(
                project_name = project_name,
                finance_approved_by = finance_approved_by,
                building_age = building_age,
                agree_val = agree_val,
                mkt_val = mkt_val,
                property_loc = property_loc,
                property_city = property_city,
                property_state = property_state,
                cc_available = cc_available,
                oc_available = oc_available,
                mun_approved = mun_approved,
                areasize = areasize,
                areain = areain,
                areatype = areatype,
                property_type = property_type,
                agree_type = agree_type,
                stp_duty = stp_duty,
                prev_agree_available = prev_agree_available,
                dup_available_or_notice = dup_available_or_notice,
                reg_prev_agreement = reg_prev_agreement,
                con_area = con_area,
                payment_till_date = payment_till_date,
                prop_det_id = prop_det
            )
            prop_det_2.save()


        if prop_type == "Balance Transfer" or prop_type == "Balance Transfer Top Up":
            bnk_name = request.POST['bnk_name']
            prod_services = request.POST['prod_services']
            loan_amt = request.POST['loan_amt']
            emi = request.POST['emi']
            outstanding_amt = request.POST['outstanding_amt']
            tenure = request.POST['tenure']
            foreclosure = request.POST['foreclosure']
            lod = request.POST['lod']

            prop_det3 = PropType3(bnk_name=bnk_name,prod_services=prod_services,loan_amt=loan_amt,emi=emi,outstanding_amt=outstanding_amt,
                                  tenure=tenure,foreclosure=foreclosure,lod=lod,prop_det_id=prop_det)
            prop_det3.save()

        
        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('/account/dashboard')

            elif user.role == "Referral Partner":
                return redirect('/account/base')

        if 'next' in request.POST:
            nxt = AdditionalDetails.objects.filter(lead_id = lead.lead_id, applicant_type = "Applicant").first()
            cust_type = nxt.cust_type.lower()
            return redirect(f"/account/{cust_type}/{nxt.add_det_id}")


    
    lead = Leads.objects.filter(lead_id = id).first()
    propertyins = PropertyIn.objects.all()
    agreementtypes = AgreementType.objects.all()
    return render(request, 'account/Property Details.html', {'propertyins':propertyins, 'agreementtypes':agreementtypes, 'lead':lead})



def retired(request,id):


    if request.method == 'POST':
        user = request.user
        add = AdditionalDetails.objects.filter(add_det_id=id).first()

        dob = request.POST['dob']
        age = request.POST['age']
        phone = request.POST['mobile_no']
        alt_phone = request.POST['alt_mobile']
        email = request.POST['email']
        gender = request.POST['gender']
        location = request.POST['address']
        state = request.POST['state']
        pincode = request.POST['pincode']
        nationality = request.POST['nationality']
        country = request.POST['country']
        end_use = request.POST['end_use']
        ret_det = RetiredDetails(dob=dob, age=age, phone=phone, alt_phone=alt_phone, email=email, gender=gender, address=location,
                                  state=state, pincode=pincode, nationality=nationality, country=country, end_use=end_use, add_det_id=add)
        ret_det.save()

        comp_name = request.POST['comp_name']
        bank_name = request.POST['bank_name']
        net_pen = request.POST['net_pen']

        if comp_name != "":
            ret_pen_det = RetiredPensionDetails(company_name = comp_name, bank_name = bank_name, net_pension = net_pen, add_det_id=add)
            ret_pen_det.save()

        res_type = request.POST['res_type']
        cur_loc = request.POST['cur_loc']
        state = request.POST['state']

        if res_type != "":
            ret_res_det = RetiredResidenceDetails(res_type = res_type, current_location = cur_loc, state =state, add_det_id = add)
            ret_res_det.save()


        bank_name = request.POST.getlist('bank_namee')
        product = request.POST.getlist('pro_ser')
        loan_amt = request.POST.getlist('loan_amt')
        emi = request.POST.getlist('emi')
        roi = request.POST.getlist('roi')
        tenure = request.POST.getlist('tenure')
        emi_start_date = request.POST.getlist('emi_start_date')
        emi_end_date = request.POST.getlist('emi_end_date')
        outstanding_paid = request.POST.getlist('outstanding_paid')
        outstanding_amt = request.POST.getlist('outstanding_amt')
        any_bounce = request.POST.getlist('any_bounce')
        moratorium_taken = request.POST.getlist('moratorium_taken')
        applicant_type = request.POST.getlist('applicant_type')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h,i,j,k,l,m) in zip(bank_name, product, loan_amt, emi, roi, tenure, emi_start_date, emi_end_date, 
                                                  outstanding_paid, outstanding_amt, any_bounce, moratorium_taken, applicant_type):
                
                ret_loan_det = RetiredExistingLoanDetails(bank_name=a, product=b, loan_amt=c, emi=d, roi=e, tenure=f, emi_start_date=g,
                                                      emi_end_date=h, outstanding_paid=i, outstanding_amt=j, any_bounce=k, 
                                                      moratorium_taken=l, applicant_type=m, add_det_id=add)

                ret_loan_det.save()

        bank_name = request.POST.getlist('bank_nameee')
        credit_limit = request.POST.getlist('credit_limit')
        limit_utilized = request.POST.getlist('limit_utilized')
        min_due = request.POST.getlist('min_due')
        card_age = request.POST.getlist('card_age')
        pay_delay = request.POST.getlist('pay_delay')
        pay_delay_year = request.POST.getlist('pay_delay_year')
        moratorium_taken = request.POST.getlist('moratorium_taken')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h) in zip(bank_name, credit_limit, limit_utilized, min_due, 
            card_age, pay_delay, pay_delay_year, moratorium_taken):
                
                ret_card_det = RetiredExistingCardDetails(bank_name=a, credit_limit=b, limit_utilized=c, 
                min_due=d, card_age=e, pay_delay=f, pay_delay_year=g, moratorium_taken=h, add_det_id=add)

                ret_card_det.save()

        
        investment = request.POST['investment']

        if investment != "":
            ret_inv_det = RetiredInvestmentDetails(investment = investment, add_det_id = add)
            ret_inv_det.save()

        inward_cheque = request.POST['inward_cheque']
        multiple_enquiry = request.POST['multiple_enquiry']
    
        if inward_cheque != "":
            ret_oth_det = RetiredOtherDetails(inward_cheque = inward_cheque, multiple_enquiry = multiple_enquiry, add_det_id = add)
            ret_oth_det.save()

        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')

        if 'next' in request.POST:
            # cust_type = nxt.cust_type.lower()
            # return redirect(f"/account/{cust_type}/{nxt.add_det_id}")
            if add.applicant_type == "Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "1st Co-Applicant").first()
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "1st Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "2nd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "2nd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "3rd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "3rd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "4th Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            else:
                return redirect(f"/account/property_details/{add.lead_id.lead_id}")
    
    cust = AdditionalDetails.objects.filter(add_det_id=id).first()
    nationalities = Nationality.objects.all()
    products = Product.objects.all()
    nationalities = Nationality.objects.all()
    applicanttypes =  ApplicantType.objects.all()
    return render(request, 'account/retired.html', {'applicanttypes':applicanttypes, 'products':products, 'nationalities':nationalities, 'cust':cust})
   
def salaried(request,id):

    if request.method == 'POST':
        user = request.user
        add = AdditionalDetails.objects.filter(add_det_id=id).first()
        
        loan_amt = request.POST['loan_amt']
        cibil_type = request.POST['cibil_type']
        cibil_score = request.POST['cibil_score']
        loanTaken = request.POST['loanTaken']
        repaymentHistory = request.POST['repaymentHistory']
        defaultYear = request.POST['defaultYear']
        details_bout_default = request.POST['details_bout_default']
        gender = request.POST['gender']
        dob = request.POST['dob']
        age = request.POST['age']
        retire_age = request.POST['retire_age']
        maritalStatus = request.POST['maritalStatus']
        qualification = request.POST['qualification']
        # degree_others = request.POST['degree_others']
        profession = request.POST['profession']
        # degree = request.POST['degree']
        # lawyerType = request.POST['lawyerType']
        nationality = request.POST['nationality']
        # country = request.POST['country']
        enduse = request.POST['enduse']

        if loan_amt != "":

            sal_personal_det = PersonalDetails(loan_amt=loan_amt, cibil_type=cibil_type, cibil_score=cibil_score,
                                                loanTaken= loanTaken, repaymentHistory=repaymentHistory, defaultYear=defaultYear, 
                                                details_bout_default=details_bout_default, gender=gender, dob=dob, age=age, 
                                                retire_age=retire_age, maritalStatus=maritalStatus, qualification=qualification, 
                                                profession=profession, nationality=nationality, enduse=enduse, addi_details_id=add)

            sal_personal_det.save()

        salary_type = request.POST['salary_type']
        bank_name = request.POST['bank_name']
        gross_sal = request.POST['gross_sal']
        net_sal = request.POST['net_sal']
        bonusType = request.POST['bonusType']
        bonus_amt = request.POST['bonus_amt']
        incentivesType = request.POST['incentivesType']
        incentive_amt = request.POST['incentive_amt']

        if bank_name != "":
            sal_inc_det = SalIncomeDetails(salaryType=salary_type, bank_name=bank_name, gross_sal=gross_sal, net_sal=net_sal,
                                        bonusType=bonusType, bonus_amt=bonus_amt, incentivesType=incentivesType, 
                                        incentive_amt=incentive_amt, addi_details_id_inc=add )
            sal_inc_det.save()

        rent_inc = request.POST.getlist('rent_inc')
        Lessee_type = request.POST.getlist('Lessee_type')
        Lessee_name = request.POST.getlist('Lessee_name')
        rent_amt = request.POST.getlist('rent_amt')
        ten_of_agmnt = request.POST.getlist('ten_of_agmnt')
        ten_pending = request.POST.getlist('ten_pending')
        validRentAgreement = request.POST.getlist('validRentAgreement')
        make_agreement = request.POST.getlist('make_agreement')
        old_agreement = request.POST.getlist('old_agreement')
        agreementType = request.POST.getlist('agreementType')
        reflectionInAccount = request.POST.getlist('reflectionInAccount')
        reflectionInItr = request.POST.getlist('reflectionInItr')
        ext_exp_in_years = request.POST.getlist('ext_exp_in_years')

        if rent_inc != "":
            for (a,b,c,d,e,f,g,h,i,j,k,l,m) in zip(rent_inc,Lessee_type,Lessee_name,rent_amt,ten_of_agmnt,ten_pending,validRentAgreement,
            make_agreement,old_agreement,agreementType,reflectionInAccount,reflectionInItr,ext_exp_in_years):
                
                sal_other_inc = SalOtherIncomes(rental_income=a, Lessee_Type=b, Lessee_Name=c,
                rent_amount=d, tenure_of_arguement=e, tenure_pending=f,
                valid_rent_agreement=g, Will_u_make_agreement=h, How_old_is_agreement=i,
                agreement_Type=j, reflection_in_bank_acc=k, reflection_in_ITR_acc=l,
                extension_expected_in_years=m, addi_details_id_other_inc=add)

                sal_other_inc.save()

            other_income = request.POST.getlist('other_income')
            income_amount = request.POST.getlist('income_amount')

        if other_income != "":
            for (a,b) in zip (other_income, income_amount):
                sal_additional_inc = SalAdditonalOtherIncome(other_income = a, income_amount = b, add_det_id=add)
                sal_additional_inc.save()

        comp_type = request.POST['comp_type']
        comp_name = request.POST['comp_name']
        location = request.POST['location']
        paid_up_cap = request.POST['paid_up_cap']
        comp_age = request.POST['comp_age']
        nature_business = request.POST['nature_business']
        designation = request.POST['designation']
        des_type = request.POST['des_type']
        curr_exp = request.POST['curr_exp']
        total_exp = request.POST['total_exp']
        emp_type = request.POST['emp_type']
        form16 = request.POST['form16']
        office_phone = request.POST['office_phone']
        office_email = request.POST['office_email']    

        if comp_name != "":
            comp_det = SalCompanyDetails(
            comp_type = comp_type,comp_name = comp_name,location = location,paid_up_cap = paid_up_cap,comp_age = comp_age,
            nature_business = nature_business,designation = designation,des_type = des_type,curr_exp = curr_exp,
            total_exp = total_exp,emp_type = emp_type,form16 = form16,office_phone = office_phone,office_email = office_email, 
            add_det_id=add)    

            comp_det.save()

        bank_name = request.POST.getlist('bank_name')
        products = request.POST.getlist('products')
        loan_amt = request.POST.getlist('loan_amt')
        emi = request.POST.getlist('emi')
        rate_of_int = request.POST.getlist('rate_of_int')
        tenure = request.POST.getlist('tenure')
        emi_start_date = request.POST.getlist('emi_start_date')
        emi_end_date = request.POST.getlist('emi_end_date')
        outstanding = request.POST.getlist('outstanding')
        out_amt = request.POST.getlist('out_amt')
        bounces = request.POST.getlist('bounces')
        mor_taken = request.POST.getlist('mor_taken')
        app_type = request.POST.getlist('app_type')

        if bank_name != []:
            for(a,b,c,d,e,f,g,h,i,j,k,l,m) in zip(bank_name, products, loan_amt, emi, rate_of_int, tenure, emi_start_date, emi_end_date,
                outstanding, out_amt, bounces, mor_taken, app_type):

                sal_exist_loan_det = SalExistingLoanDetails(bank_name=a, products=b, loan_amount=c, emi=d, rate_of_interest=e,
                tenure=f, emi_start_date=g, emi_end_date=h, outstan_paid_by_customer=i, outstanding_amount=j, any_bounces=k,
                moratorium_taken=l, application_type=m, add_det_id=add)  

                sal_exist_loan_det.save()

    
        card_bank_name = request.POST.getlist('card_bank_name')
        credit_limit = request.POST.getlist('credit_limit')
        limit_utilized = request.POST.getlist('limit_utilized')
        min_due = request.POST.getlist('min_due')
        credit_card_age = request.POST.getlist('credit_card_age')
        payment_delay = request.POST.getlist('payment_delay')
        payment_delay_year = request.POST.getlist('payment_delay_year')
        mor_taken = request.POST.getlist('mor_taken')

        if card_bank_name != []:
            for(a,b,c,d,e,f,g,h) in zip(card_bank_name, credit_limit, limit_utilized, min_due, 
            credit_card_age, payment_delay, payment_delay_year, mor_taken):
                
                sal_exist_card_det = SalExistingCardDetails(card_bank_name=a, credit_limit=b, limit_utilized=c, 
                min_due=d, credit_card_age=e, payment_delay=f, payment_delay_year=g, mor_taken=h, add_det_id=add)

                sal_exist_card_det.save()

        inw_cheque_return = request.POST['inw_cheque_return']
        loanInquiry = request.POST['loanInquiry']
        loan_enq_det = request.POST['loan_enq_det']

        if inw_cheque_return != "":
            sal_additional_det = SalAdditionalDetails(inw_cheque_return=inw_cheque_return, loan_enq_disburse=loanInquiry, loan_enq_det=loan_enq_det, add_det_id=add)
            sal_additional_det.save()


        investments_u_have = request.POST['investments_u_have']

        if investments_u_have != "":
            sal_inv_u_have = Investments(investments_u_have=investments_u_have,add_det_id=add)
            sal_inv_u_have.save()


        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')

        if 'next' in request.POST:
            # cust_type = nxt.cust_type.lower()
            # return redirect(f"/account/{cust_type}/{nxt.add_det_id}")
            if add.applicant_type == "Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "1st Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "1st Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "2nd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "2nd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "3rd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "3rd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "4th Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            else:
                return redirect(f"/account/property_details/{add.lead_id.lead_id}")



    cust = AdditionalDetails.objects.filter(add_det_id=id).first()
    genders = Gender.objects.all()
    qualifications = Qualification.objects.all()
    degrees = Degree.objects.all()
    professions = Profession.objects.all()
    nationalities = Nationality.objects.all()
    maritalstatues = MaritalStatus.objects.all()
    salarytypes = SalaryType.objects.all()
    agreementtypes = AgreementType.objects.all()
    companytypes = CompanyType.objects.all()
    designationtypes = DesignationType.objects.all()
    products = Product.objects.all()
    context = {
        'genders': genders,
        'qualifications': qualifications,
        'degrees': degrees,
        'professions': professions,
        'nationalities': nationalities,
        'maritalstatues': maritalstatues,
        'salarytypes': salarytypes,
        'agreementtypes': agreementtypes,
        'companytypes': companytypes,
        'designationtypes': designationtypes,
        'products': products,
        
        'cust':cust
    }

    return render(request, 'account/Salaried.html', context=context)

def selfemployed(request):
    genders = Gender.objects.all()
    maritalstatues = MaritalStatus.objects.all()
    qualifications = Qualification.objects.all()
    degrees = Degree.objects.all()
    professions = Profession.objects.all()
    nationalities = Nationality.objects.all()
    residenceTypes = ResidenceType.objects.all()
    companytypes = CompanyType.objects.all()
    agreementtypes = AgreementType.objects.all()
    products = Product.objects.all()
    
    context = {
        'genders': genders,
        'maritalstatues': maritalstatues,
        'qualifications': qualifications,
        'degrees': degrees,
        'professions': professions,
        'nationalities': nationalities,
        'residenceTypes': residenceTypes,
        'companytypes': companytypes,
        'agreementtypes': agreementtypes,
        'products': products
    }
    return render(request, 'account/Self Employed.html', context=context)

def student(request,id):

    if request.method == 'POST':
        user = request.user
        add = AdditionalDetails.objects.filter(add_det_id=id).first()


        dob = request.POST['dob']
        age = request.POST['age']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        email = request.POST['email']
        gender = request.POST['gender']
        location = request.POST['location']
        state = request.POST['state']
        pincode = request.POST['pincode']
        nationality = request.POST['nationality']
        country = request.POST['country']
        end_use = request.POST['end_use']
        stud_det = StudentDetails(dob=dob, age=age, phone=phone, alt_phone=alt_phone, email=email, gender=gender, location=location,
                                  state=state, pincode=pincode, nationality=nationality, country=country, end_use=end_use, add_det_id=add)
        stud_det.save()


        bank_name = request.POST.getlist('bank_name')
        product = request.POST.getlist('product')
        loan_amt = request.POST.getlist('loan_amt')
        emi = request.POST.getlist('emi')
        roi = request.POST.getlist('roi')
        tenure = request.POST.getlist('tenure')
        emi_start_date = request.POST.getlist('emi_start_date')
        emi_end_date = request.POST.getlist('emi_end_date')
        outstanding_paid = request.POST.getlist('outstanding_paid')
        outstanding_amt = request.POST.getlist('outstanding_amt')
        any_bounce = request.POST.getlist('any_bounce')
        moratorium_taken = request.POST.getlist('moratorium_taken')
        applicant_type = request.POST.getlist('applicant_type')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h,i,j,k,l,m) in zip(bank_name, product, loan_amt, emi, roi, tenure, emi_start_date, emi_end_date, 
                                                  outstanding_paid, outstanding_amt, any_bounce, moratorium_taken, applicant_type):
                
                loan_det = StudentExistingLoanDetails(bank_name=a, product=b, loan_amt=c, emi=d, roi=e, tenure=f, emi_start_date=g,
                                                      emi_end_date=h, outstanding_paid=i, outstanding_amt=j, any_bounce=k, 
                                                      moratorium_taken=l, applicant_type=m, add_det_id=add)

                loan_det.save()


        bank_name = request.POST.getlist('bank_name')
        credit_limit = request.POST.getlist('credit_limit')
        limit_utilized = request.POST.getlist('limit_utilized')
        min_due = request.POST.getlist('min_due')
        card_age = request.POST.getlist('card_age')
        pay_delay = request.POST.getlist('pay_delay')
        pay_delay_year = request.POST.getlist('pay_delay_year')
        moratorium_taken = request.POST.getlist('moratorium_taken')

        if(bank_name != []):
            for(a,b,c,d,e,f,g,h) in zip(bank_name, credit_limit, limit_utilized, min_due, 
            card_age, pay_delay, pay_delay_year, moratorium_taken):
                
                card_det = StudentExistingCardDetails(bank_name=a, credit_limit=b, limit_utilized=c, 
                min_due=d, card_age=e, pay_delay=f, pay_delay_year=g, moratorium_taken=h, add_det_id=add)

                card_det.save()


        if 'save' in request.POST:
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')

        if 'next' in request.POST:
            # cust_type = nxt.cust_type.lower()
            # return redirect(f"/account/{cust_type}/{nxt.add_det_id}")
            if add.applicant_type == "Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "1st Co-Applicant").first()
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "1st Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "2nd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "2nd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "3rd Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            elif add.applicant_type == "3rd Co-Applicant":
                add1 = AdditionalDetails.objects.filter(lead_id=add.lead_id, applicant_type = "4th Co-Applicant").first()
                
                if add1 == None:
                    return redirect(f"/account/property_details/{add.lead_id.lead_id}")
                else:
                    cust_type = add1.cust_type.lower()
                    return redirect(f"/account/{cust_type}/{add1.add_det_id}")

            else:
                return redirect(f"/account/property_details/{add.lead_id.lead_id}")


    cust = AdditionalDetails.objects.filter(add_det_id=id).first()
    genders = Gender.objects.all()
    nationalities = Nationality.objects.all()
    products = Product.objects.all()
    return render(request, 'account/Student.html', {'nationalities':nationalities, 'products':products, 'genders': genders, 'cust': cust})


