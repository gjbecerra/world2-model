from flask import Flask, request
from flask import render_template
from datetime import time
from world2_runsim import world2_run

app = Flask(__name__)

@app.route("/")
def chart():
    return render_template('index.html')


@app.route("/world2_model", methods=['GET','POST'])
def world2_model():
    errors = ""
    if request.method == "POST":
        BRN1 = None
        NRUN1 = None
        DRN1 = None
        FC1 = None
        POLN1 = None
        try:
            BRN1 = float(request.form["birthRate"])
        except:
            errors += "Birth Rate {!r} is not a number.\n".format(request.form["naturalResourceUsage"])
        try:
            NRUN1 = float(request.form["naturalResourceUsage"])
        except:
            errors += "Natural Resource Usage {!r} is not a number.\n".format(request.form["naturalResourceUsage"])
        try:
            DRN1 = float(request.form["deathRate"])
        except:
            errors += "Death Rate {!r} is not a number.\n".format(request.form["naturalResourceUsage"])
        try:
            FC1 = float(request.form["foodCoefficient"])
        except:
            errors += "Food Coefficient {!r} is not a number.\n".format(request.form["naturalResourceUsage"])
        try:
            POLN1 = float(request.form["pollution"])
        except:
            errors += "Pollution {!r} is not a number.\n".format(request.form["naturalResourceUsage"])

        TIME, P, POLR, CI, QL, NR = world2_run(BRN1, NRUN1, DRN1, FC1, POLN1)
        return render_template('world2_model.html', population=P, pollution=POLR,\
            capitalInv=CI, qualityOfLife=QL, naturalResources=NR, labels=TIME,\
            errors=errors)
    if request.method == "GET":
        BRN1 = 0.04
        NRUN1 = 1
        DRN1 = 0.028
        FC1 = 1
        POLN1 = 1
        TIME, P, POLR, CI, QL, NR = world2_run(BRN1, NRUN1, DRN1, FC1, POLN1)
        return render_template('world2_model.html', population=P, pollution=POLR,\
            capitalInv=CI, qualityOfLife=QL, naturalResources=NR, labels=TIME)

if __name__ == "__main__":
    app.run(debug=True)
