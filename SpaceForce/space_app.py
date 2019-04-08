from flask import Flask, jsonify, request,abort
from space_transmit import * 

app= Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/',methods=['GET'])
def test():
    return jsonify({'message':'Welcome!'})

@app.route('/data',methods=['POST'])
def post_data():
    if not request.json:
        abort(400,'This endpoint requires a JSON request body')
    raw_data=request.json['data']
    s_id=request.json['spaceship_id']
    units=request.json['units']
    try:
        df=process_data(raw_data,units)
        write_db(df,s_id)
        return jsonify({'message':'Post Sucessful'})
    except:
        return abort(400)

@app.route('/data',methods=['GET'])
def get_data():
    s_id=request.args.get('spaceship_id')
    start=request.args.get('start')
    end=request.args.get('end')
    try:
        result=query_db(s_id,start,end)
        return jsonify(result)
    except:
        return abort(400)
 
if __name__=='__main__':
    app.run(debug=True, port=5001)