from flask import Flask, render_template, request, jsonify
from planner import Planner
import json

app = Flask(__name__)
planner = Planner()

# Create a new planning problem
planner.definePlanningProblem()

@app.route("/")
def index(exp=0):
    p = planner.getOrderedObservations()
    return render_template('index.html', canAskForExplanations=exp, plan=p)

'''
Function that obtains plan from the UI request and
returns a JSON format.
    @Input
        Example 'plan' : [
                {"name":"Add Course - Embedded Operating Systems Internal (systems)",
                        "x":0,"y":0,"width":12,"height":1},
                {"name":"Add Chair - Subbarao Kambhampati (applications)",
                        "x":0,"y":3,"width":12,"height":1}
            ]
'''
def ui_plan_to_pddl_style(request):
    seq = {}
    print(request)
    plan = json.loads(dict(request.form)['plan'][0])
    print(plan)
    for act in plan:
        # We assume that only one action occurs at a time
        # TODO: Update code if we want to allow options for
        # two simultaneous actions (choices)
        seq[ act["y"] ] = act["name"]
    #print "\n======\n{}\n======\n".format(seq)
    print(seq)
    return seq

@app.route("/validate", methods=['GET', 'POST'])
def validate():
    planner.savePlan() 
    planner.getValidatedPlan(ui_plan_to_pddl_style(request))
    return index()
    
@app.route("/fix", methods=['GET', 'POST'])
def fix():
    planner.savePlan()
    planner.getSuggestedPlan(ui_plan_to_pddl_style(request), True)
    return index()
    
@app.route("/suggest", methods=['GET', 'POST'])
def suggest():
    planner.savePlan()
    planner.getSuggestedPlan(ui_plan_to_pddl_style(request))
    return index(1)
    
@app.route("/undo", methods=['GET', 'POST'])
def undo():
    planner.loadPlan()
    return index()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
