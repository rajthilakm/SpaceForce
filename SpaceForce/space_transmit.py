import datetime
import pandas as pd 
import json
import numpy as np
from influxdb import DataFrameClient
from influxdb import InfluxDBClient

def process_data(raw_data,units):
    '''
    Function to process raw data 
    parameters : raw_data , units 
    returns Pandas Dataframe with cleaned and resampled data 
    '''
    df=pd.DataFrame.from_records(raw_data)
    df['datetime']=pd.to_datetime(pd.DatetimeIndex(df.datetime))
    df.value=pd.to_numeric(df.value,errors='coerce').astype('float')
    interval=round(pd.Series(df.datetime.unique()).diff().dropna().mean()/np.timedelta64(1, 'm'))
    df=df.set_index('datetime')
    if interval==60.0 and (units=='kW' or units=='kWh'):
    	df= disaggregate(df)
    elif interval== 5.0 and units=='kW':
        df=df*(5/60)
        df=df.resample('15T').sum()
    elif interval == 5.0 and units =='kWh':
        df=df.resample('15T').sum()
    elif interval ==15.0 and units=='kW':
        df=df/4
    elif interval==15.0 and units=='kWh':
        df=df
    else:
        return(Exception)
    return df

def disaggregate(df):
    '''
    Function to disggregate hourly values
    parameters : df
    returns Pandas Dataframe with disaggregated data 
    '''
    df=df/4
    df=df.resample('15T').mean().interpolate(method='pad',axis=1,limit=3,limit_direction='forward')
    ds=pd.date_range(start=df.index[-1]+datetime.timedelta(minutes=15),periods=3,freq='15T')
    ve=[df.iloc[-1].value]*3
    new_df=pd.DataFrame({'datetime':ds,'value':ve})
    new_df=new_df.set_index('datetime')
    df=df.append(new_df)
    return df

def write_db(df,s_id):
    '''
    Function to write data to influx db 
    parameters : df , s_id 
    returns boolean value of operation
    '''
    dfclient=DataFrameClient(host='127.0.0.1',port=8086,database='space')
    x=dfclient.write_points(df,measurement='power',
        	tags={'site_id':s_id,'units':'kWh'},
        	field_columns={'value':df[['value']]},
        	database='space')
    return x

def query_db(s_id,start_date,end_date):
    '''
    Function to query data from influx db 
    parameters :  s_id , start date , end data 
    returns dictionary of the query 
    '''
    client=InfluxDBClient(host='127.0.0.1',port=8086,database='space_app')
    sd=format_date(start_date)
    ed=format_date(end_date)
    q="SELECT * FROM autogen.power where (site_id='{}' AND time >='{}' AND time <='{}')".format(s_id,sd,ed)
    x=client.query(q,database='space')
    x_dict=x.raw
    x_df=pd.DataFrame.from_records(x_dict.get('series')[0].get('values'),columns=x_dict.get('series')[0].get('columns'))
    x_df=x_df.rename(columns={'time':'datetime'})
    data=x_df[['datetime','value']].to_json(orient='records')
    frame={"spaceship_id":x_df.site_id.iloc[0],"units":x_df.units.iloc[0],"data":json.loads(data)}
    return frame

def format_date(sd):
    '''
    Helper funtion to format date given in get command
    parameters : sd 
    return string with formatted date 
    '''
    return sd.replace('-',':').replace(':','-',2)