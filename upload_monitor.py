import functools
import json
import os
import pandas
import glob


import monitor_api

import monitor_logger

from flask import Flask, request, render_template, jsonify, \
    send_from_directory

from flask_restful import Api

from monitor_resource import monitor_resource

from flask import Flask, jsonify
from flask_cors import cross_origin
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost'], supports_credentials=True)

logger = monitor_logger.get_logger(__name__)

# app.config['UPLOAD_PATH'] = os.getcwd()+'/static/video/'
app.config['UPLOAD_PATH'] ='/DanceWorkbench/test_videos_store/front'

app.config['UPLOADS_DEFAULT_DEST'] = app.config['UPLOAD_PATH']
app.config['ALLOWED_EXTENSIONS'] = set(['gif','mp4','m4a','avi'])

api = Api(app)
api.add_resource(monitor_api.MonitorApi, '/api/<id>')

app.register_blueprint(monitor_resource)
last_score = []


def log(*text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            logger.debug('执行方法：%s，请求参数：%s():' % (func.__name__, text))
            return func(*args, **kw)

        return wrapper

    return decorator


@log
def is_safe_url(next_url):
    logger.debug("next url is %s:" % next_url)
    return True


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')




# 文件下载
@app.route('/download/<path:filename>')
def send_html(filename):
    logger.debug("download file, path is %s" % filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)


# http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
@app.route('/upload', methods=['POST','GET'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            logger.debug('No selected file')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    logger.debug('filename is %s' % origin_file_name)
                    # filename = secure_filename(file.filename)
                    filename = origin_file_name

                    if os.path.exists(app.config['UPLOAD_PATH']):
                        logger.debug('%s path exist' % app.config['UPLOAD_PATH'])
                        pass
                    else:
                        logger.debug('%s path not exist, do make dir' % app.config['UPLOAD_PATH'])
                        os.makedirs(app.config['UPLOAD_PATH'])

                    if check_video(app.config['UPLOAD_PATH']):  #该路径下已经存在这个视频，删除这些视频
                        for infile in glob.glob(os.path.join(app.config['UPLOAD_PATH'], '*.gif')):
                            os.remove(infile)
                        for infile in glob.glob(os.path.join(app.config['UPLOAD_PATH'], '*.mp4')):
                            os.remove(infile)
                        for infile in glob.glob(os.path.join(app.config['UPLOAD_PATH'], '*.m4a')):
                            os.remove(infile)
                        for infile in glob.glob(os.path.join(app.config['UPLOAD_PATH'], '*.avi')):
                            os.remove(infile)

                    file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                    logger.debug('%s save successfully' % filename)
                    return jsonify({'code': 0, 'filename': origin_file_name, 'msg': ''})
                else:
                    logger.debug('%s not allowed' % file.filename)
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                logger.debug('upload file exception: %s' % e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})

def check_video(filepath):
    Files=os.listdir(filepath)
    for k in range(len(Files)):
        # 提取文件夹内所有文件的后缀
        Files[k]=os.path.splitext(Files[k])[1]
    
    Str2=['.wav','.mp3','.mp4']
    if len(list(set(Str2).intersection(set(Files))))>0:  #假设该路径下有视频
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/delete', methods=['GET'])
def delete_file():
    if request.method == 'GET':
        filename = request.args.get('filename')
        timestamp = request.args.get('timestamp')
        logger.debug('delete file : %s, timestamp is %s' % (filename, timestamp))
        try:
            fullfile = os.path.join(app.config['UPLOAD_PATH'], filename)

            if os.path.exists(fullfile):
                os.remove(fullfile)
                logger.debug("%s removed successfully" % fullfile)
                return jsonify({'code': 0, 'msg': ''})
            else:
                return jsonify({'code': -1, 'msg': 'File not exist'})

        except Exception as e:
            logger.debug("delete file error %s" % e)
            return jsonify({'code': -1, 'msg': 'File deleted error'})

    else:
        return jsonify({'code': -1, 'msg': 'Method not allowed'})




@app.route('/getScore',methods=['POST'])
def getscore():
    data = json.loads(request.form.get('data'))
    filename = data['filename']  #测试视频
    standard = data['standard']  #标准视频，作为调用main函数的参数
    output_path = '../DanceWorkbench/output'
    command = 'ls'
    d = os.system(command)
    print(d)
    # filename = './scores/'+filename+'.csv'
    data = pandas.read_csv('output_score.csv', header=0)
    motion_score = data.iloc[0,1:].tolist()
    rhythm_score = data.iloc[1,1:].tolist()
    result = []
    id = 0
    for row1_item,row2_item in zip(motion_score,rhythm_score):
        content = {'id': id, 'motion_score': str(row1_item),'rhythm_score':str(row2_item)}
        result.append(content)
        id = id+1
        content = {}
    return jsonify(result)  #一共有16列，最后一列是总分
    #stocklist = list(data.values.flatten())
    #return jsonify(last_score)


app.secret_key = 'aHR0cDovL3d3dy53YW5kYS5jbi8='

if __name__ == '__main__':
    # print(type(flask_db.get_user('admin')))
    # print(flask_db.get_user('admin'))
    
    CORS(app, supports_credentials=True)  # 设置跨域
    app.run(host='0.0.0.0',#任何ip都可以访问
    debug=True)
    # CORS(app, supports_credentials=True)  # 设置跨域
    # app.run(debug=True)