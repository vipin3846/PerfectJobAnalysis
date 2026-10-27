from flask import Flask , render_template , request , Response
import pandas as pd 
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)



def data(args):
    cmpy_data = pd.read_csv("static/company_data2.csv")
    cmpy_name = args.get('cmpy')
    industry = args.get('industry')  # Dropdown menu
    location = args.get('location')  # Dropdown menu
    cmpy_type = args.get('company_type')  # Dropdown menu
    emp_size = args.get('employee_size')  # Dropdown menu
            
    min_rating = args.get('min_rating')
    max_rating = args.get('max_rating')
    min_age = args.get('min_age')
    max_age = args.get('max_age')
    
    
        #conn  = get_connection()
        #cur = conn.cursor(pymysql.cursors.DictCursor)
        #cur.execute("select * from company_data limit 10")
        #company_data = cur.fetchall()
    
    
    if cmpy_name:
        cmpy_data = cmpy_data[cmpy_data['company_name'].str.contains(cmpy_name, case=False)]
    if industry and industry != "All industries":
        cmpy_data = cmpy_data[cmpy_data['industry'].str.lower() == industry.lower()]
    if location and location != "All locations":
        cmpy_data = cmpy_data[cmpy_data['location'].str.lower() == location.lower()]
    if cmpy_type and cmpy_type != "All company types":
        cmpy_data = cmpy_data[cmpy_data['type'].str.lower() == cmpy_type.lower()]
    if emp_size and emp_size != "All sizes":
        cmpy_data = cmpy_data[cmpy_data['employes'].str.lower() == emp_size.lower()]
    if min_rating:
        cmpy_data = cmpy_data[cmpy_data['company_rating'] >= float(min_rating)]
    if max_rating:
        cmpy_data = cmpy_data[cmpy_data['company_rating'] <= float(max_rating)]
    if min_age:
        cmpy_data = cmpy_data[cmpy_data['age'] >= float(min_age)]
    if max_age:
        cmpy_data = cmpy_data[cmpy_data['age'] <= float(max_age)]


    return cmpy_data




@app.route("/")
def home():
    data = pd.read_csv("static/company_data2.csv")
    city = len(data['location'].unique())
    avg = round(data['company_rating'].mean(),1)
    return render_template('index.html',lanth = len(data),city=city,avg=avg)

@app.route("/dashboard")
def dashboard():
    cmpy_data = data(request.args)



    cmpy_record = cmpy_data['company_name'].count()
    cmpy_unique = cmpy_data['company_name'].nunique()
    cmpy_rating = round(cmpy_data['company_rating'].mean(),1)
    cmpy_rating_avlable = round((cmpy_data["company_rating"].notna().sum() / len(cmpy_data)) *100,1)
    plt.figure(figsize=(9,3))
    sns.barplot(x=cmpy_data['type'],y=cmpy_data['company_rating'],palette="viridis")
    plt.title("company type wise rating")
    plt.xlabel('company type')
    plt.ylabel('rating')
    plt.xticks(rotation=45, ha='right',fontsize=10)

    buf1 = BytesIO()
    plt.savefig(buf1,format="png",bbox_inches = 'tight')
    plt.close()
    buf1.seek(0)

    plot_url1 = base64.b64encode(buf1.getvalue()).decode('utf-8')


    cmpy_data['rating_group'] = pd.cut(cmpy_data['company_rating'], bins=4, labels=['Poor', 'Average', 'Good', 'Excellent'])
    plt.figure(figsize=(4,3))
    sns.countplot(cmpy_data['rating_group'])

    buf2 = BytesIO()
    plt.savefig(buf2,format="png",bbox_inches = 'tight')
    plt.close()
    buf2.seek(0)

    plot_url2 = base64.b64encode(buf2.getvalue()).decode('utf-8')


    
    top_industries = cmpy_data["industry"].value_counts().head(10).sort_values()
    plt.figure(figsize=(4,3))
    sns.barplot(
    x=top_industries.index,
    y=top_industries.values,
    color="steelblue"
    )
    plt.title("Top 10 Industries by Number of Companies")
    plt.ylabel("Number of Companies")
    plt.xlabel("Industry")
    plt.xticks(rotation=45, ha='right',fontsize=8)
    plt.tight_layout()
    
    buf3 = BytesIO()
    plt.savefig(buf3,format="png",bbox_inches = 'tight')
    plt.close()
    buf3.seek(0)
    
    plot_url3 = base64.b64encode(buf3.getvalue()).decode('utf-8')


    employee_counts = cmpy_data["employes"].value_counts()
    employee_order = [
    "1-10", "11-50", "51-200", "201-500",
    "501-1k", "1k-5k", "5k-10k",
    "10k-50k", "50k-1 Lakh", "1 Lakh+"
    ]

    employee_order = [
    size for size in employee_order
    if size in employee_counts.index
    ]

    ordered_counts = employee_counts.reindex(employee_order)
    plt.figure(figsize=(4,3))
    sns.barplot(
    x=ordered_counts.index,
    y=ordered_counts.values,
    color="steelblue"
    )
    plt.title("Company Distribution by Employee Size")
    plt.xlabel("Employee Size")
    plt.ylabel("Number of Companies")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buf4 = BytesIO()
    plt.savefig(buf4,format="png",bbox_inches = 'tight')
    plt.close()
    buf4.seek(0)
        
    plot_url4 = base64.b64encode(buf4.getvalue()).decode('utf-8')




    top_locations = cmpy_data["location"].value_counts().head(10).sort_values()
    plt.figure(figsize=(4,3))
    sns.barplot(
    x=top_locations.index,
    y=top_locations.values,
    color="steelblue"
    )
    plt.title("Top 10 Locations by Number of Companies")
    plt.ylabel("Number of Companies")
    plt.xlabel("Location")
    plt.xticks(rotation=45, ha='right',fontsize=8)
    plt.tight_layout()

    buf5 = BytesIO()
    plt.savefig(buf5,format="png",bbox_inches = 'tight')
    plt.close()
    buf5.seek(0)
            
    plot_url5 = base64.b64encode(buf5.getvalue()).decode('utf-8')


    return render_template('dashboard.html',cmpy_unique=cmpy_unique,cmpy_record=cmpy_record,cmpy_rating=cmpy_rating,cmpy_rating_avlable=cmpy_rating_avlable,plot_url1=plot_url1,plot_url2=plot_url2,plot_url3=plot_url3,plot_url4=plot_url4,plot_url5=plot_url5)





per_page = 11
@app.route("/table",methods=['GET', 'POST'])
def table():
    cmpy_data = data(request.args)

    if request.args.get('action')=="export":
        return Response(
        cmpy_data.to_csv(index=False),
        headers={"Content-Disposition": "attachment; filename=companies.csv"}
        )



    page = request.args.get('page',1,type=int)
    total_pages = max(1,-(-len(cmpy_data)//per_page))
    page = max(1,min(page,total_pages))

    start = (page-1)*per_page
    records = cmpy_data.iloc[start:start+per_page].to_dict(orient='records')

    args = {k: v for k, v in request.args.items() if k not in ('page','action') and v}

    #cmpy_data=cmpy_data.head(10)
    #records = cmpy_data.to_dict(orient='records')
    return render_template("table.html",cmpy_data = records,page=page,total_pages=total_pages,total=len(cmpy_data),args=args)

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)