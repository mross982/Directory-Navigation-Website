from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
# from werkzeug import secure_filename
from app import app, db
from app.forms import LoginForm, CategorySetupForm, LinkSetupForm
from app.models import User, Category, Link
import sys
import csv
from datetime import datetime as dt


def object_troubleshoot(obj):

    for attr in dir(obj):
        try:
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
        except:
            pass


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')



@app.route('/user/<name>', methods=['GET', 'POST'])
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    containter_form = ContainerSetupForm()
    category_form = CategorySetupForm()
    link_form = LinkSetupForm()
    if request.method == 'POST':
        if category_form.submit.data == True: #create new container
            category = Category(name=category_form.name.data)
            category.user_id.append(current_user.id)
            db.session.add(category)
            db.session.commit()
            category_form.name.data = ''
            category_form.submit.data = False
            
            return render_template('user.html', name=current_user.name, containers=user.containers, container_form=container_form, category_form=category_form, link_form=link_form)
    	
    	elif category_form.submit.data == True: # create new category
    		pass

    	elif link_form.submit.data == True: # create new link
    		pass

        

    return render_template('user.html', name=current_user.name, containers=user.containers, container_form=container_form, category_form=category_form, link_form=link_form)


# @app.route('/measure_setup/<program_id>', methods=['GET', 'POST'])
# @login_required
# def measure_setup(program_id):
#     measure_form = MeasureSetupForm()
#     benchmark_form = BenchmarksForm()
#     if benchmark_form.validate_on_submit():
#         measure = Measure(name=measure_form.name.data, program_id=program_id, unit=measure_form.unit.data, start_date=measure_form.start_date.data,
#             end_date=measure_form.end_date.data, direction=measure_form.direction.data)
#         db.session.add(measure)
#         db.session.commit()
#         measure = Measure.query.filter_by(name=measure_form.name.data).first_or_404()
#         for entry in benchmark_form.benchmarks.entries:
#             if entry.data['benchmark'] == None:
#                 break
#             else:
#                 n_bm = Benchmark(measure_id=measure.id, benchmark=entry.data['benchmark'], value=entry.data['value'])
#                 db.session.add(n_bm)
#         db.session.commit()
        
#         return redirect(url_for('data', measure_id=measure.id))
#     print(measure_form.errors)
#     print(benchmark_form.errors)

#     return render_template('measure_setup.html', title='Set up a Measure', measure_form=measure_form, benchmark_form=benchmark_form)


# @app.route('/data/<measure_id>', methods=['GET', 'POST'])
# @login_required
# def data(measure_id):
    
#     data_form = DataForm()
#     if request.method == 'POST':

#         if data_form.file.name not in request.files: # check if the post request has the file part
#             flash('No file part')
#             return redirect(url_for('data', measure_id=measure_id, data_form=data_form))

#         file = request.files[data_form.file.name] # Create variable for uploaded file
#         # if user does not select file, browser may submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(url_for('data', measure_id=measure_id, data_form=data_form))
       
#         filename = secure_filename(file.filename) # prevent any funny buisiness
#         #####################################################
#         # TEMPORARY SCAFFOLDING
#         file_fields = {'Date': 'date', 'Numerator': 'numerator', 'Patient ID':'data_id'}
#         #####################################################

#         with open(filename, newline='', encoding='utf-8-sig') as csvfile: # w/o encoding, got ï»¿ in A1
#             spamreader = csv.DictReader(csvfile)
#             try:
#                 for rdr in spamreader:
#                     for k, v in rdr.items():
#                         if k in file_fields.keys():
#                             rdr[file_fields[k]] = rdr.pop(k) # convert field names based on file_fields mapping
#                         else:
#                             print('some field didnt match the defined file_fields', str(k))
#                             pass
#                         if k == 'Date': # convert to datetime object
#                             dateformat = '%m/%d/%Y'
#                             dt_obj = dt.strptime(rdr['date'], dateformat)
#                             rdr['date'] = dt_obj

#                     data = Data(measure_id=measure_id, date=rdr['date'], data_id=rdr['data_id'], numerator=rdr['numerator'])
                    
#                     db.session.add(data)
#                     db.session.commit()
#             except:
#                 print('something broke')
#                 db.session.rollback()
        
#         return redirect(url_for('user', name=current_user.name))
    
#     return render_template('data.html', data_form=data_form)


# @app.route('/modify_measure/<measure_id>', methods=['GET', 'POST'])
# @login_required
# def modify_measure(measure_id):
#     measure = Measure.query.filter_by(id=measure_id).first_or_404()
#     benchmarks = Benchmark.query.filter_by(measure_id=measure_id).all()
#     measure_form = MeasureSetupForm(obj=measure)
#     benchmark_form = BenchmarksForm.populate_form(measure_id)
#     if request.method == 'POST':
#         measure.name=measure_form.name.data
#         measure.unit=measure_form.unit.data
#         measure.start_date=measure_form.start_date.data
#         measure.end_date=measure_form.end_date.data
#         measure.direction=measure_form.direction.data
#         ######### TO DO ###################
#         # FIX THE BENCHMARKS TO UPDATE AS WELL
#         #######################################

#         db.session.commit()
#         return redirect(url_for('user', name=current_user.name))
    
#     return render_template('measure_setup.html', title='Modify your Measure', measure_form=measure_form, benchmark_form=benchmark_form)


# @app.route('/warning/<measure_id>', methods=['GET' ,'POST'])
# @login_required
# def warning(measure_id):
#     form = WarningForm()
#     if request.method == 'POST':
#         if form.delete.data:
#             benchmarks = Benchmark.query.filter_by(measure_id=measure_id).all()
#             db.session.delete(measure)
#             for b_mark in benchmarks:
#                 db.session.delete(b_mark)
#             db.session.commit()
#             flash("Measure Deleted")
#             return redirect(url_for('user', name=current_user.name ))
#         else:
#             return redirect(url_for('user', name=current_user.name))
#     return render_template('warning.html', form=form)


# @app.route('/share/<program_id>', methods=['GET', 'POST'])
# @login_required
# def share(program_id):
#     form = UserShareForm()
#     if request.method == 'POST':
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             program = Program.query.filter_by(id=program_id).first()
#             program.users.append(user)
#             db.session.add(program)
#             db.session.commit()
#             return redirect(url_for('user', name=current_user.name))

#         else:
#             flash("User email not found. Try again!")
#             return redirect(url_for('share', program_id=program_id))

#     return render_template('share.html', form=form)
