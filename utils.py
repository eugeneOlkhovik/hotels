import pandas as pd
import numpy as np
import missingno as msno
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt


colors=px.colors.sequential.RdBu

def get_pie_plot(df,col_name, title):
    fig = px.pie(df,names=col_name, width=600, height=400, title = title, color_discrete_sequence=colors)
    fig.show()

def get_histogram_plot(df,col_name, title,nbins=15):
    fig = px.histogram(df,x=col_name, width=800, height=600, title = title, color_discrete_sequence=colors, nbins=nbins)
    fig.show()

def get_histogram_target_plot(df,col_name, title, nbins=15, is_percent=True):
    p = 'percent' if is_percent else None
    fig = px.histogram(df,x=col_name, width=800, height=600, barmode='group', 
                       title = title,color='is_canceled', color_discrete_sequence=colors, nbins=nbins, histnorm=p)
    fig.show()

def get_plot_price_monthly(df):
    months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
    price_monthly = df[df['is_canceled'] == 'not_canceled'][["hotel", "arrival_date_month", "adr_per_person"]].sort_values("arrival_date_month")
    price_monthly['arrival_date_month'] = pd.Categorical(price_monthly['arrival_date_month'], categories=months, ordered=True)
    sns.set_palette("rocket")
    plt.figure(figsize=(15,8))
    sns.lineplot(x = "arrival_date_month", y="adr_per_person", hue="hotel", data=price_monthly, 
                hue_order = ["City Hotel", "Resort Hotel"], size="hotel", sizes=(2.5, 2.5))
    plt.title("Room price per night and person over the year", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.xticks(rotation=45)
    plt.ylabel("Price", fontsize=12)
    plt.show()

def get_hist_subplot(df,col_names, plot_title, subplot_titles):
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)
    fig.add_trace(
    go.Histogram(x=df[col_names[0]], 
                 marker = {'color' : colors[0]},
                 ), 
    row=1,col=1)
    fig.add_trace(
    go.Histogram(x=df[col_names[1]],
                 marker = {'color' : colors[0]},
                 ), 
    row=1,col=2)

    fig.update_layout(height=600, width=1200, title_text=plot_title, showlegend=False)
    fig.show()
   
def get_subplots_with_cancelation(df,col_names,plot_title, subplot_titles):
    fig = make_subplots(rows=1, cols=2, subplot_titles=subplot_titles)
    fig.add_trace(
        go.Histogram(x=df[df['is_canceled']=='not_canceled'][col_names[0]], name="Not canceled",
                     marker = {'color' : colors[0]}, nbinsx=20
                     ), 
        row=1,col=1
    )
    fig.add_trace(
        go.Histogram(x=df[df['is_canceled']=='canceled'][col_names[0]], name="Canceled",
                     marker = {'color' : colors[1]}, nbinsx=20
                     ), 
        row=1,col=1
    )
    fig.add_trace(
        go.Histogram(x=df[df['is_canceled']=='not_canceled'][col_names[1]], name="Not canceled",
        showlegend=False,
                     marker = {'color' : colors[0]}
                     ), 
        row=1,col=2,
    )
    fig.add_trace(
        go.Histogram(x=df[df['is_canceled']=='canceled'][col_names[1]], name="Canceled",
        showlegend=False,
                     marker = {'color' : colors[1]}
                     ), 
        row=1,col=2
    )

    fig.update_layout(height=600, width=1200, title_text=plot_title, showlegend=True)
    fig.show()
    
def get_box_plot(df,col_name,plot_title):
    fig = go.Figure()
    fig.add_trace(go.Box(x=df[df['is_canceled']=='not_canceled'][col_name], name="Not canceled",
            showlegend=True,
                         marker = {'color' : colors[0]}
                         )
    )
    fig.add_trace(go.Box(x=df[df['is_canceled']=='canceled'][col_name], name="canceled",
            showlegend=True,
                         marker = {'color' : colors[1]}
                         )
    )
    fig.update_layout(height=600, width=1200, title_text=plot_title, showlegend=True)
    fig.show()
    
def find_outliers_IQR(df):
    q1=df.quantile(0.25)
    q3=df.quantile(0.75)
    IQR=q3-q1
    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
    print(f'number of outliers: {len(outliers)}')
    print(f'max outlier value: {str(outliers.max())}')
    print(f'min outlier value: {str(outliers.min())}')

def get_target_encoding(df, column):
    categories = df[column].unique()
    targets = df['is_canceled'].unique()
    cat_list = []
    for cat in categories:
        aux_dict = {'category': cat}
        aux_df = df[df[column] == cat]
        counts = aux_df['is_canceled'].value_counts()
        aux_dict['count'] = sum(counts)
        for t in targets:
            aux_dict[f'target_{str(t)}'] = counts[t]
        cat_list.append(aux_dict)
    cat_list = pd.DataFrame(cat_list)
    cat_list[column] = cat_list['target_1'] / cat_list['count']
    dict(zip(cat_list.category.values, cat_list[column].values))
    df[column].replace(dict(zip(cat_list.category.values, cat_list[column].values)), inplace=True)