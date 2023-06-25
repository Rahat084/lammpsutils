#! /user/bin/env python
''' Read and analyze lammps log file'''
from os.path import exists
import matplotlib.pyplot as plt
import numpy as np


class LogReader():
    """
    Class object to read and analyze the lammps log files
    """

    def __init__(self,filename = "log.lammps"):
        self._filename = filename
        # Read Thermodynamic data from the log file
        if exists(filename):
            with open(filename,'r') as r:
                lines = r.readlines()
                for line in lines:
                    if 'Step' in line:
                        start = lines.index(line)
                    if 'Loop' in line:
                        stop = lines.index(line)
                try:
                    start
                except NameError:
                    print("No thermo data to read")
                    return
                self._headline = lines[start]
                self._data = [lines[i] for i in range(start+1,stop)]
        else:
            print(f"No logfile named {filename} found\nInsert the logfile name")


    def _filename_check(func):
        def wrapper(self, *args, **kwargs):
            if exists(self._filename):
                return func(self, *args, **kwargs)
            else:
                print(f"No logfile named {self._filename} found\nInsert the logfile name")
        return wrapper


    def __call__(self,filename):
        self.__init__(filename=filename)


    @_filename_check
    def write_txt(self,filename):
        # Write therodynamic data to a text file
        with open(filename,'w') as wrt:
            wrt.write(self._headline)
            wrt.write(self._data)


    @_filename_check
    def view_data(self):
        print(self._headline)
        print("".join(self._data))


    @_filename_check
    def get_data(self):
        return np.loadtxt(self._data)


    @_filename_check
    def plot(self, xlabel, ylabel, fontsize = 20):
        data= self.get_data()
        heading = self._headline.split(" ")
        xlbl = heading.index(xlabel)
        ylbl = heading.index(ylabel)
        plt.plot(data[:,xlbl], data[:,ylbl])
        plt.xlabel(xlabel, fontsize = fontsize)
        plt.ylabel(ylabel, fontsize = fontsize)


if __name__=="__main__":
    reader = LogReader()
    reader.view_data()
