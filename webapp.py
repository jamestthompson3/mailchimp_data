from flask import Flask, render_template



# In[39]:


app=Flask(__name__)

@app.route('/')
def home():
	return render_template("home.html")
@app.route('/plot/')
def plot():
	import pandas as pd
	from bokeh.plotting import output_file, show, figure
	from bokeh.models import HoverTool, ColumnDataSource
	from bokeh.embed import components
	from bokeh.resources import CDN
	df=pd.read_csv("mailchimp_campaigns.csv", parse_dates=["Send_Date"])

	cds=ColumnDataSource(df)
	hover=HoverTool(tooltips=[("Group","@Title"),("Open Rate","@Open_Rate"),("Successful Deliveries", "@Successful_Deliveries"),("Total Opens","@Total_Opens"),("Click Rate","@Click_Rate"),("Total Clicks","@Total_Clicks"),("Unsubs","@Unsubscribes")])
	p=figure(plot_width=700,plot_height=400,x_axis_type="datetime",responsive=True)
	p.add_tools(hover)
	p.title="Email Campaign Open Rates (hover over dots for details)"
	p.xaxis.axis_label="Send Date"
	p.yaxis.axis_label="Open Rate"
	p.circle(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,size=9)
	p.line(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,line_width=3)

	#p.line(df["Send_Date"],df["Open_Rate"].mean(),color="#FE7A7A",source=cds,line_width=2)
	
	script1,div1=components(p)
	cdn_js=CDN.js_files[0]
	cdn_css=CDN.css_files[0]
	return render_template("plot.html",
    script1=script1,
    div1=div1,
    cdn_css=cdn_css,
    cdn_js=cdn_js )

if __name__=="__main__":
	app.run(debug=True)
