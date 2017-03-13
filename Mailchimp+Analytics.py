
# coding: utf-8

# In[30]:

import pandas as pd
import datetime
from bokeh.plotting import output_file, show, figure
from bokeh.models import HoverTool, ColumnDataSource


# In[39]:

df=pd.read_csv("mailchimp_campaigns.csv", parse_dates=["Send_Date"])


# In[38]:

output_file("mailchimp.html")
cds=ColumnDataSource(df)
hover=HoverTool(tooltips=[("Group","@Title"),("Successful Deliveries", "@Successful_Deliveries"),("Total Opens","@Total_Opens"),("Click Rate","@Click_Rate"),("Total Clicks","@Total_Clicks"),("Unsubs","@Unsubscribes")])
p=figure(plot_width=700,plot_height=400,x_axis_type="datetime")
p.add_tools(hover)
p.title="Email Campaign Open Rates"
p.xaxis.axis_label="Send Date"
p.yaxis.axis_label="Open Rate"
p.circle(df["Send_Date"],df["Open_Rate"],color="#44D5FE",source=cds,size=7)
show(p)


# In[ ]:



