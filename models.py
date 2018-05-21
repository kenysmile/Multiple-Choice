@app.route('/teacher')
def teacher():
    user = session.get('user')
    cols = ['id', 'ten', 'tuoi', 'diachi', 'userid']
    # data = Teacher.query.all()
    data = Teacher.query.filter_by(ten = user)
    result = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(result=result)