import os
import io
import subprocess
import time
import platform
import pprint
import datetime

ecal_bin         = ''
ecal_samples_bin = ''
res_dir          = ''
runs             = ''
zc               = ''

if platform.system() == "Windows":
  ecal_bin         = os.path.join(os.environ['ECAL_HOME'], 'bin')
  ecal_samples_bin = os.path.join(os.environ['ECAL_HOME'], 'samples', 'bin')
  res_dir          = 'd:\\'

ecal_stop_prc    = os.path.join(ecal_bin,         'ecal_stop')
ecal_lat_snd_prc = os.path.join(ecal_samples_bin, 'ecal_sample_latency_snd')
ecal_lat_rec_prc = os.path.join(ecal_samples_bin, 'ecal_sample_latency_rec_cb')

def getSystemInfo():
  info={}
  info['platform']=platform.system()
  info['platform-release']=platform.release()
  info['platform-version']=platform.version()
  info['architecture']=platform.machine()
  info['processor']=platform.processor()
  r = ''
  for k,v in info.items():
    r += f'{k}: {v}\n'
  return r

def run_checks():
  res = ''
  for s in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
    p1 = subprocess.Popen([ecal_lat_rec_prc], stdout=subprocess.PIPE)
    time.sleep(1)
    p2 = subprocess.Popen([ecal_lat_snd_prc, f"{zc}", f"-r {runs}", f"-s {s}"])
    p2.wait()
    os.system(ecal_stop_prc)
    r = io.TextIOWrapper(p1.stdout, encoding="utf-8").read()
    print(r)
    res += r
    time.sleep(5)
  return res

ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

f = open(os.path.join(res_dir, f"ecal-latency-{ts}.txt"), 'w')
f.write('Mode: ZERO COPY OFF\n\n')
f.write(getSystemInfo())
f.write('\n')
runs = '10000'
zc   = ''
f.write(run_checks())
f.close()

f = open(os.path.join(res_dir, f"ecal-latency-{ts}-zero-copy.txt"), 'w')
f.write('Mode: ZERO COPY ON\n\n')
f.write(getSystemInfo())
f.write('\n')
runs = '10000'
zc   = '-z'
f.write(run_checks())
f.close()
