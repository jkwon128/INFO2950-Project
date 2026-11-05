import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/info2950-mpl')
os.environ.setdefault('IPYTHONDIR','/tmp/info2950-ipython')
os.environ.setdefault('JUPYTER_RUNTIME_DIR','/tmp/info2950-jupyter')
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
p=Path(sys.argv[1]).resolve()
n=nbformat.read(p,as_version=4)
km=KernelManager(kernel_name='python3')
km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
NotebookClient(n,km=km,timeout=240,resources={'metadata':{'path':str(p.parent)}}).execute()
nbformat.write(n,p)
print('Executed:',p.name)
for c in n.cells:
    for o in c.get('outputs',[]):
        if o.output_type=='stream':print(o.text.strip())
