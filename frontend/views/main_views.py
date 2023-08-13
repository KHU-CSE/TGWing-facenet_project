from flask import Blueprint, render_template, request
import numpy as np
import json
import sys
import keras
sys.path.append('../../')
from src import embeddings
bp = Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def main():
    return render_template('main/main.html',client_img=False,faculty=False)

@bp.route('/',methods=('POST',))
def create():

    file = request.files['file']
    path = "./frontend/static/client_img/"+(file.filename)
    path_ = "./static/client_img/"+(file.filename)
    file.save(path)
    keras.backend.clear_session()
    model = keras.models.load_model('./model/facenet_keras.h5')
    emb = embeddings.get_embedding_from_one_pic(model, path)
    faculty_json = open('./model/faculty_emb.json',encoding='utf-8')
    faculty_dict = json.load(faculty_json)
    min_dist = 100
    name = ""
    for key in faculty_dict:
        dist = np.linalg.norm(faculty_dict[key]-emb)
        if min_dist>dist:
            min_dist=dist
            name = key
    print(name, min_dist)
    department = name.split('_')[0]
    name_ = name.split('_')[1]
    faculty_path = "./static/faculty_img/"+name+".jpg"

    return render_template('main/main.html', client_img=path_, faculty=faculty_path, department=department, name=name_)
