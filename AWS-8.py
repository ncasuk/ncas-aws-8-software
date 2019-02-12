#!/usr/bin/env python3
import csv
import os

import pandas as pd
from datetime import datetime

from amfutils.instrument import AMFInstrument
from netCDF4 import Dataset

class AWS8 (AMFInstrument):
    """
    Class to convert arbitrary Campbell AWS `.dat` files into well-formed
    netCDF files conforming to AMF conventions
    """

    progname = __file__
    amf_variables_file = 'surface-met.xlsx - Variables - Specific.csv' 

    def get_data(self, infiles):
        """
        Example top few lines of DAT file

        ::
            
            "TOA5","CR1000","CR1000","2923","CR1000.Std.26","CPU:YORK3.CR1","15302","Table1"
            "TIMESTAMP","RECORD","WS_ms_S_WVT","WindDir_D1_WVT","BP_mbar_Avg","AirTC_Avg","RH","Slr_W_Avg","Slr_kJ_Tot"
            "TS","RN","meters/second","Deg","mbar","Deg C","%","W/m²","kJ/m²"
            "","","WVc","WVc","Avg","Avg","Smp","Avg","Tot"
            "2017-09-14 17:23:00",0,4.785,33.57,1014,26.73,77.77,440.5,77.09
            "2017-09-14 17:24:00",1,5.062,37.94,1014,26.81,78.12,441.3,132.4
            "2017-09-14 17:25:00",2,4.412,43.33,1014,26.92,78.26,437.7,131.3

        :param infiles: list(-like) of data filenames
        :return: a Pandas DataFrame of the AWS data
        """

        aws = pd.DataFrame()
        for infile in infiles:
            with open(infile,'rb') as f:
                aws = pd.concat([aws, pd.read_csv(f, 
                    parse_dates=True, 
                    index_col=0, 
                    header=0, 
                    encoding='utf-8', 
                    skiprows=[0,2,3],
                    na_values=['NAN'],
                    dtype={"TIMESTAMP":str,"RECORD": int,"WS_ms_S_WVT":float,"WindDir_D1_WVT":float,"BP_mbar_Avg":float,"AirTC_Avg":float,"RH":float,"Slr_W_Avg":float,"Slr_kJ_Tot":float}
                    )])

        aws.sort_index(inplace=True)
        aws.drop_duplicates(inplace=True)

        #set start and end times
        self.time_coverage_start = aws.index[0].strftime(self.timeformat)
        self.time_coverage_end = aws.index[-1].strftime(self.timeformat)

        self.rawdata = aws
        return aws

    def netcdf(self, output_dir):
        """
        Takes a dataframe (self.rawdata) with Campbell AWS data and outputs a 
        well-formed NetCDF using appropriate conventions.

        :param output_dir: string containing path to output directory
        """
        self.setup_dataset('surface-met',1)

        #lat/long
        self.land_coordinates()

        tempvar = {}
        #create and populate variable fields
        for each in ['air_pressure', 'air_temperature', 'relative_humidity','wind_speed', 'wind_from_direction','downwelling_shortwave_flux_in_air']:
            tempvar[each] = self.amf_var_to_netcdf_var(each)
        tempvar['air_pressure'] = self.rawdata.BP_mbar_Avg # mbar==hPa
        tempvar['air_temperature'] = self.rawdata.AirTC_Avg + 273.15 #convert to K
        tempvar['relative_humidity'] = self.rawdata.RH 
        tempvar['wind_speed'][:] = self.rawdata.WS_ms_S_WVT.values
        tempvar['wind_from_direction'][:] = self.rawdata.WindDir_D1_WVT.values
        tempvar['downwelling_shortwave_flux_in_air'][:] = self.rawdata.Slr_W_Avg.values
    
        #add all remaining attribs
        self.dataset.setncatts(self.raw_metadata)
    
        self.dataset.close()

if __name__ == '__main__':
    args = AWS8.arguments().parse_args()
    aws = AWS8(args.metadata) 

    try:
        os.makedirs(args.outdir,mode=0o755)
    except OSError:
         #Dir already exists, probably
         pass
    else:
        print ("Successfully create directory %s" % args.outdir)
    aws.get_data(args.infiles)
    aws.netcdf(output_dir=args.outdir)

