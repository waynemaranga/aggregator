```sh
uv pip freeze > requirements.txt
pip install --requirement requirements.txt --target dependencies/ --upgrade
pip install -r requirements.txt -t dependencies --upgrade
zip -r dependencies.zip dependencies
```