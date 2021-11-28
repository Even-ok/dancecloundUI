from flask import Flask
from flask import request
app = Flask(import_name=__name__)

@app.route('test', methods=['GET', 'POST'])
def test():
	f = request.files.get("file")	#获取前端传来的文件
	f.save('./{}'.format(f.filename))	# 将文件保存下来
	return {'flag': True}

if __name__ == '__main__':
    # print(type(flask_db.get_user('admin')))
    # print(flask_db.get_user('admin'))
    app.run()