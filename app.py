from flask import Flask, render_template, request, jsonify
from planner import Planner
from interface import Interface
import json
import sys

app = Flask(__name__)
planner = Planner()
translator = Interface()

# Create a new planning problem
planner.definePlanningProblem()

''' Helper actions '''
def pddl_to_ui_actions():
    # Get the plan to be showed in the planning panel
    action_seq = planner.get_action_sequence_list()
    return translator.actionsToUI(action_seq)

def ui_to_pddl_actions(request, is_get_request=False):
    if is_get_request:
        plan = json.loads( request.args.get('plan') )
    else:
        plan = json.loads( dict(request.form)['plan'][0] )
    return translator.uiToActions(plan)

@app.route("/")
def index(was_plan_found=False):

    p = pddl_to_ui_actions()
    # Should we show the explanation button
    can_ask_for_explanations = 0
    if was_plan_found:
        can_ask_for_explanations = 1
    
    return render_template('index.html', canAskForExplanations=can_ask_for_explanations, plan=p)

@app.route("/validate", methods=['GET', 'POST'])
def validate():
    print('[DEBUG] Starting Validation Process ...')
    planner.save_plan()
    planner.get_validated_plan(ui_to_pddl_actions(request, is_get_request=True))
    return jsonify(pddl_to_ui_actions())
    
@app.route("/suggest", methods=['GET', 'POST'])
def suggest():
    print('[DEBUG] Starting Suggestion Process ...')
    planner.save_plan()
    
    # plan_was_found = 1 if plan is found, 0 otherwise
    was_plan_found = planner.get_suggested_plan(ui_to_pddl_actions(request))
    if not was_plan_found:
        planner.load_plan()
    
    return index(was_plan_found)

def main(host='127.0.0.1'):
    app.run(host=host,
            port=5000,
            debug=True)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(host=sys.argv[1])
    else:
        main()
