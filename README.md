//// Sur les deux (MAC M1 et WINDOWS)
conda env create -f environment.yml
conda activate poc-setfit

//// Sur WINDOWS (à la racine):
    pip uninstall torch -y
    pip install torch --index-url https://download.pytorch.org/whl/cu121

/// Tester le streamlit (à la racine)
.\.venv\Scripts\Activate.ps1
(Si ça ne marche pas, essayer ça avant :
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
)

    /// INSTALLER LES DEPENDANCES
    python -m pip install streamlit
    Ou
    python -m pip install -r requirements.txt

python -m streamlit run Dashboard/app.py

