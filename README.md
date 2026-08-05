//// Sur les deux (MAC M1 et WINDOWS)
conda env create -f environment.yml
conda activate poc-setfit

//// Sur WINDOWS (à la racine):
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cu121
