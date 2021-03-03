FROM jupyter/base-notebook

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /tmp/

RUN jupyter nbextension install --py jupyter_tabnine --user
RUN jupyter nbextension enable --py jupyter_tabnine --user
RUN jupyter serverextension enable --py jupyter_tabnine --user