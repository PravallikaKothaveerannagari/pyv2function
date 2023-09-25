import azure.functions as func
import os
import datetime
import logging
import sys
import importlib.util

# Azure function timer. To alter timer cadence see function.json file
app = func.FunctionApp()

@app.function_name(name="monitoring_weekly")
@app.schedule(schedule="0 */1 * * * *", 
              arg_name="mytimer",
              run_on_startup=False,
              use_monitor=True) 

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if mytimer.past_due:
        logging.info('The timer is past due!')
        
    logging.info('Python timer trigger function ran at %s', utc_timestamp)


def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), f'{script_name}')

    s = importlib.util.spec_from_file_location(script_name, script_path)
    m = importlib.util.module_from_spec(s)
    sys.modules[s.name] = m
    s.loader.exec_module(m)

    
def batch_execution(file_list):

    exceptions = [] #store errors

    for file in file_list:
        try:
            run_script(file)
        except Exception as e:
            exceptions.append(e)
        else: 
            print('Success')

    return exceptions

#list of scripts running in function, if adding new script add to list.
file_list = ['python_file1.py',
        'python_file2.py',
        'python_file3.py',
        'python_file4.py',
        'python_file5.py']

batch_execution(file_list)