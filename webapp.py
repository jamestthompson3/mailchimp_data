from flask import Flask, render_template, request
from email.mime.text import MIMEText
import smtplib
import pandas as pd

app=Flask(__name__)
def send_email(file):
	df=pd.read_csv(file)
	emailz=[]
	for item in df["Email"]:
		emailz.append(item)
	from_email="sendmeemail951@gmail.com"
	from_password="sendtheemail"

	subject="Hello."
	message="This was sent by one of your friends. You are doing a great job and someone cares about you! I hope you have a wonderful day!"

	for item in emailz:
		msg=MIMEText(message,'html')
		msg['Subject']=subject
		msg['To']=item
		msg['From']=from_email
		gmail=smtplib.SMTP('smtp.gmail.com',587)
		gmail.ehlo()
		gmail.starttls()
		gmail.login(from_email,from_password)
		gmail.send_message(msg)

@app.route('/')
def home():
	return render_template("home.html")
@app.route('/newsletter/')
def newsletter():
	import pandas as pd
	import datetime
	from bokeh.plotting import output_file, show, figure
	from bokeh.models import HoverTool, ColumnDataSource
	from bokeh.embed import components
	from bokeh.resources import CDN


	df=pd.read_csv("domino_newsletter.csv", parse_dates=["Send_Date"])

	cds=ColumnDataSource(df)

	hover=HoverTool(tooltips=[("Title","@Title"),("Open Rate","@Open_Rate"),("Successful Deliveries", "@Successful_Deliveries"),("Opens","@Unique_Opens"),("Click Rate","@Click_Rate"),("Total Clicks","@Total_Clicks"),("Unsubs","@Unsubscribes"),("Bounces","@Total_Bounces")])

	p=figure(plot_width=700,plot_height=400,x_axis_type="datetime",responsive=True)
	p.add_tools(hover)
	
	p.title.text="Newsletter Open Rates (hover for more details)"
	p.title.text_font_size='20pt'
	p.xaxis.axis_label="Send Date"
	p.xaxis.axis_label_text_font_size="15pt"
	p.yaxis.axis_label="Open Rate (%) "
	p.yaxis.axis_label_text_font_size="15pt"
	
	p.circle(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,size=7)
	r=df[["Send_Date", "Successful_Deliveries","Soft_Bounces","Hard_Bounces","Total_Bounces",
	"Unique_Opens","Unique_Clicks","Unsubscribes"]].groupby([pd.Grouper(freq='1W',key='Send_Date')]).sum()
	html_table=r.to_html(bold_rows=True, border=None, justify='left',index=True)
	
	script1,div1=components(p)
	cdn_js=CDN.js_files[0]
	cdn_css=CDN.css_files[0]
	return render_template("newsletter.html",
    script1=script1,
    div1=div1,
    html_table=html_table,
    cdn_css=cdn_css,
    cdn_js=cdn_js )

@app.route('/marketing/')
def marketing():
	import pandas as pd
	from bokeh.plotting import output_file, show, figure
	from bokeh.models import HoverTool, ColumnDataSource
	from bokeh.embed import components
	from bokeh.resources import CDN
	df=pd.read_csv("mailchimp_campaigns.csv", parse_dates=["Send_Date"])


	cds=ColumnDataSource(df)
	
	p=figure(plot_width=700,plot_height=400,x_axis_type="datetime",responsive=True)
	hover=HoverTool(tooltips=[("Group","@Title"),("Open Rate","@Open_Rate"),("Subject","@Subject"),("Successful Deliveries", "@Successful_Deliveries"),("Opens","@Unique_Opens"),("Click Rate","@Click_Rate"),
		("Total Clicks","@Total_Clicks"),("Unsubs","@Unsubscribes"),("Bounces","@Total_Bounces")])
	
	p.add_tools(hover)
	p.title="Email Campaign Open Rates (hover for more details)"
	p.title.text_font_size='20pt'
	p.xaxis.axis_label="Send Date"
	p.xaxis.axis_label_text_font_size="15pt"
	p.yaxis.axis_label="Open Rate (%) "
	p.yaxis.axis_label_text_font_size="15pt"
	
	p.circle(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,size=11)
	p.line(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,line_width=3)
	r=df[["Send_Date", "Successful_Deliveries","Soft_Bounces","Hard_Bounces","Total_Bounces",
	"Unique_Opens","Unique_Clicks","Unsubscribes"]].groupby([pd.Grouper(freq='1W',key='Send_Date')]).sum()
	html_table=r.to_html(bold_rows=True, border=None, justify='left',index=True)
	
	script1,div1=components(p)
	cdn_js=CDN.js_files[0]
	cdn_css=CDN.css_files[0]
	return render_template("marketing.html",
    script1=script1,
    div1=div1,
    html_table=html_table,
    cdn_css=cdn_css,
    cdn_js=cdn_js )

@app.route('/email_validation/', methods=['GET','POST'])
def email_validation():
	if request.method=='POST':
		file=request.files['upload']
		send_email(file)
		return render_template("success.html")
	return render_template("email_validation.html")

@app.route('/email_validation/success/',methods=['GET','POST'])
def upload_success():
	return render_template("success.html")

if __name__=="__main__":
	app.run(debug=True)
