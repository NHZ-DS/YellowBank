import os, re

files = [
    'streamlit_app/Home.py',
    'streamlit_app/pages/1_Questionnaire.py',
    'streamlit_app/pages/2_Situation.py',
    'streamlit_app/pages/3_Parcours.py'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        
        c = re.sub(r'page_icon=":material/[a-z_]+:"', 'page_icon="⭐"', c)
        c = re.sub(r':material/[a-z_]+:', '', c)
        
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(c)
        print(f"Cleaned {f}")
    except Exception as e:
        print(f"Error {f}: {e}")
