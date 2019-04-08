import sys
sys.path.append('../')
from test_utils import * 
import space_transmit
import datetime
import pandas as pd 
from pandas.util.testing import assert_frame_equal
import unittest

class TestApp(unittest.TestCase):
    '''
    Test the functions used by space app 
    '''
    def test_format_date(self):
        """ Method to test format date function"""
        dt='2018-02-03T00-01-00'
        eq_('2018-02-03T00:01:00',space_transmit.format_date(dt))

    def test_disaggregate(self):
        """ Method to disaggregate function. This test only works
    for cases where the data is available in 1 HR intervals 
        """
        processed_df = pd.read_pickle('./processed_df.pickle')
        raw_df=pd.read_pickle('./raw_df.pickle')
        test_processed_df=space_transmit.disaggregate(raw_df)
        assert_frame_equal(processed_df,test_processed_df)

    def test_process_data_15_Min(self):
        """ 
    Method to test process data function. 
    This test only works for cases where the data is available 
    in 15 Min intervals 
        """
        raw_data=pd.read_pickle('./raw_data_15M.pickle')
        processed_df=pd.read_pickle('./processed_df_15_Min.pickle')
        units='kWh'
        test_processed_df_15_M=space_transmit.process_data(raw_data,units)
        assert_frame_equal(processed_df,test_processed_df_15_M)

    def test_process_data_1_H(self):
        """ 
    Method to test process data function. 
    This test only works for cases where the data is available 
    in 60 Min intervals 
        """
        raw_data=pd.read_pickle('./raw_data_1H.pickle')
        processed_df=pd.read_pickle('./processed_df_1H.pickle')
        units='kWh'
        test_processed_df_1H=space_transmit.process_data(raw_data,units)
        assert_frame_equal(processed_df,test_processed_df_1H)

    def test_process_data_5_M(self):
        """ 
    Method to test process data function. 
    This test only works for cases where the data is available 
    in 5 Min intervals 
        """
        raw_data=pd.read_pickle('./raw_data_5M.pickle')
        processed_df=pd.read_pickle('./processed_df_5M.pickle')
        units='kW'
        test_processed_df_1H=space_transmit.process_data(raw_data,units)
        assert_frame_equal(processed_df,test_processed_df_1H)

    def test_query_db(self):
        """ 
    Method to test query function. 
        """
        s_id='11'
        start='2018-08-24T00-00-00Z'
        end='2018-08-24T03-00-00Z'
        result= space_transmit.query_db(s_id,start,end)
        test_query_result=pd.read_pickle('./query_db_result.pickle')
        eq_(result,test_query_result)

if __name__ == '__main__':
    unittest.main()