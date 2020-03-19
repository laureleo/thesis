# Setup
* python -m venv .thesis 
* source .thesis/bin/activate
* (.thesis) $ pip install ipykernel
* (.thesis) $ ipython kernel install --user --name=.thesis
* (.thesis) $ pip install --upgrade pip
* (.thesis) $ pip install -r requirements.txt

* make sure you use the .thesis kernel when opening jupyter lab

# For progress bars
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# Dealing with GPU OOM
Simplest workaround seems to be closing down the notebook, then restarting it. You can check the held GPU with nvidia-smi
