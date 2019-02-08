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
                aws = pd.concat([aws, pd.read_csv(f, header=0, encoding='utf-8', skiprows=[0,2,3])])

        print(aws)



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

