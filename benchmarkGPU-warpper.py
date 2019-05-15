#!/usr/bin/python
"""
Benchmark GPU Tool
Output: csv table with the benchmark results

"""
import subprocess
import os
import sys
import datetime
import time
import pygit2
import logging
import functools
import re
import shutil
import pandas as pd

#global params
images = ["pytorch","caffe2","cntk"]
version=17.12
internet_available=True
repo_path = '/tmp/benachmark-gpu'
log_path = "/tmp/Benchmark-gpu.log"
repo_url = 'https://github.com/u39kun/deep-learning-benchmark.git'
date = datetime.datetime.now().isoformat()

#logger constructor
def create_logger():
    """
    Creates a logging object and return s logger 
    """
    logger = logging.getLogger("GPU Benchmark Logger")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(log_path)
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

#Decorator logger
def log(func):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_str = func.__name__
        if type(args) != type(str):
                args_str = "Not str format argument"
        else:
                args_str = ', '.join(args)
        start_time = time.time()
        if func_str == "mainRunBenchmark":
                logger.info("Starting Run Benchmark GPU with the function {func_str} ".format(func_str=func_str))
        else:
                logger.info("Running func {func_str} with arguments: {args_str}".format(func_str=func_str,args_str=args_str))
        try:
                results = func(*args, **kwargs)
                end_time = time.time()
                diff = round(end_time - start_time,2)

                logger.info("End func {func_str} with results:{results} - the function takes {diff}Secounds".format(func_str=func_str,results=results,diff=diff))
                return results
                
        except:
                logger.error("Problem in func {func_str}".format(func_str=func_str))
                return "Error"

    return wrapper


@log
def cloneGit(repo_url,repo_path):
    try:
        # Clone a repository
        if os.path.exists(repo_url):
              shutil.rmtree(repo_path)  
        results=pygit2.clone_repository(repo_url, repo_path, bare=False, repository=None, remote=None, checkout_branch=None, callbacks=None)
        return "Pass"
    except:
            logger.error("Error with git clone")
            logger.error("Try to check def get_git")
            return "Failed"
    
@log
def getImages(images):
    subprocess.Popen("sudo mkdir /opt/docker_images",shell=True,stdout=subprocess.PIPE)
    command=subprocess.Popen("sudo docker login nvcr.io/nvidia",shell=True,stdout=subprocess.PIPE)
    command.wait()
    for image in images:
        command=subprocess.Popen("sudo docker pull nvcr.io/nvidia/{image}:{version}".format(image=image,version=version),shell=True,stdout=subprocess.PIPE)
        command.wait()
        print(command.communicate()[0])
        command=subprocess.Popen("sudo docker save nvcr.io/nvidia/{image}:{version} >> /opt/docker_images/{image}-{version}.tgz".format(image=image,version=version),shell=True,stdout=subprocess.PIPE)
        command.wait()
        print(command.communicate()[0])
    return "Pass"

@log
def ensurePreTestRequirements():
        #install pips
        modules = ["tensorflow", "torch", "caffe2" ,"torchvision"]
        try:
            for module in modules:
                subprocess.call(['pip3', 'install', module])
            return "Pass"
        except:
            return "Failed"

@log
def parseBenchOutput(output):
        """
        This function aims to parse the output from the benchmark script
        this function return DataFrame to work with.
        """
        counter1 = 0
        parse_array = []
        data = []
        while counter1 < len(output):
                if "running benchmark for frameworks" in output[counter1]  :
                        break
                counter1 += 1
        for i in range(counter1+3,len(output)):
                parse_array.clear()
                
                parse_array = output[i].split(' ')
                parse_array[0] = parse_array[0][:-2]
                parse_array.pop(3)
                parse_array[3] = parse_array[3][:-1]
                parse_array.pop(5)
                parse_string = " ".join(parse_array)
                parse_string = date + " " + parse_string
                data.append(parse_string)
        df = pd.DataFrame(data=[row.split() for row in data],columns=['Timestamp','Framework','Algoritem','Bench','Precision','Result'])
        return df
        

@log
def runBench():
        """
        The Function Consolidate the Benchmark process,
        this func calls to the whole others function.
        """
       # result = ensurePreTestRequirements()
        result = "Pass"
        if result == "Pass":
                        
                process = subprocess.getoutput('sudo python3 /tmp/benachmark-gpu/benchmark.py') # Also gets you the stdout
                output = process.split('\n')                
                df = parseBenchOutput(output)
                if os.path.exists('/tmp/benchGPUResult.csv'):
                    os.remove('/tmp/benchGPUResult.csv')  
                df.to_csv('~/benchGPUResult.csv')
                logger.info("Benchmark end")
        else:
                logger.error("Failed prerequirements check")
                return "ERROR"
        return True


@log
def mainRunBenchmark():
  """
  Main Function to manage the benchmark process
  """
  #result = cloneGit(repo_url,repo_path)
  #result = getImages(images)
  result = runBench()
  return result

#main
if __name__ == "__main__":
    logger = create_logger()
    result=mainRunBenchmark()
    print(result)
