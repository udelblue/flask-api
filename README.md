## Virtual environment

### Windows venv activation


```bash
# In cmd.exe
venv\Scripts\activate.bat

or 

.venv\Scripts\activate

# In PowerShell
venv\Scripts\Activate.ps1

```

### Linux and MacOS venv activation

```bash
$ source myvenv/bin/activate
```



## Run 

```bash
set FLASK_APP=.app.py
flask run



flask --app ./app.py run
```



## API Document

go to http://127.0.0.1:5000/openapi