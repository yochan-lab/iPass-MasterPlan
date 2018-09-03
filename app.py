from flask import Flask, render_template, request, jsonify
from planner import Planner
from interface import Interface
import json

app = Flask(__name__)
planner = Planner()
translator = Interface()

# Create a new planning problem
planner.definePlanningProblem()

@app.route("/")
def index(was_plan_found=False):

    # Get the plan to be showed in the planning panel
    action_seq = planner.get_action_sequence_list()
    p = translator.actionsToUI(action_seq)
    
    # Should we show the explanation button
    can_ask_for_explanations = 0
    if was_plan_found:
        can_ask_for_explanations = 1
    
    return render_template('index.html', canAskForExplanations=can_ask_for_explanations, plan=p)

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
    plan = json.loads(dict(request.form)['plan'][0])
    print(plan)
    return translator.uiToActions(plan)

@app.route("/validate", methods=['GET', 'POST'])
def validate():
    planner.save_plan() 
    planner.get_validated_plan(ui_plan_to_pddl_style(request))
    return index()
    
@app.route("/suggest", methods=['GET', 'POST'])
def suggest():
    planner.save_plan()
    
    # plan_was_found = 1 if plan is found, 0 otherwise
    was_plan_found = planner.get_suggested_plan(ui_plan_to_pddl_style(request))
    if not was_plan_found:
        planner.load_plan()
    
    return index(was_plan_found)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
