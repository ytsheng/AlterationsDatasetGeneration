from selenium import webdriver
import time
import random
import math
import json

# Utility Methods
def random_number(mmin, mmax, step):
    delta = mmax - mmin + step
    rrange = delta / step
    rand = random.random()
    rand *= rrange
    rand = math.floor(rand)
    rand *= step
    rand += mmin
    return float("{:.2f}".format(rand))

def get_params_circlepacking(pid, name_val):
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {
        "seed": seed,
        "nc": random_number(1, 5, 1),
        "pid": pid,
        "name": name_val,
    }

    return params


def get_params_carpet(nl, name_val):
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {
        "seed": seed,
        "ng": random_number(5, 60, 1),
        "sce": random_number(0, 1, 1),
        "sw": random_number(2, 7, 1),
        "pid": random_number(0, 4, 1),
        "nl": nl,
        "name": name_val,
    }

    return params


### Tiles & Cushions
def get_params_tnc(c, name_val):
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {
        "seed": seed,
        "ng": random_number(1, 60, 1),
        "rth": random_number(0, 1, 0.1),
        "sw": random_number(1, 7, 1),
        "pid": random_number(0, 4, 1),
        "dl": random_number(0, 1, 1),
        "curvy": c,
        "name": name_val,
    }

    return params


### Spractal Code
def get_params_spractal(ol, name_val):
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {
        "seed": seed,
        "rc": random_number(0, 1, 0.1),
        "droptiny": random_number(0, 1, 0.1),
        "droplarge": random_number(0, 1, 0.1),
        "droprest": random_number(0, 1, 0.1),
        "nu": random_number(0, 0.1, 0.01),
        "fci": random_number(0, 11, 1),
        "eci": random_number(0, 2, 1),
        "ew": random_number(1, 10, 1),
        "overlap": ol,
        "name": name_val,
    }

    chance = params["rc"]
    return params


## Stroke Code
def get_params_strokes(sw, name_val):
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {
        "seed": seed,
        "numTrials": random_number(0, 10, 1),
        "strokeWidth": sw,
        "pid": random_number(0, 4, 1),
        "cid": random_number(0, 1, 0.1),
        "p0": random_number(0, 1, 0.1),
        "p1": random_number(0, 1, 0.1),
        "name": name_val,
    }
    return params

## Leaves Code
def get_params_leaves(vc, name_val):
    dynamic = dynamic_params_leaves()
    seed = random.randint(0, 10000000)
    random.seed(seed)
    params = {"seed": seed}

    for name, val in dynamic.items():
        mmin = dynamic[name][0]
        mmax = dynamic[name][1]
        step = dynamic[name][2]
        rand = random_number(mmin, mmax, step)
        params[name] = rand

    params["verticalSize"] = vc
    params["name"] = name_val
    return params

def dynamic_params_leaves():
    return {
        # take the form of alteration_name: [min, max, optional_step]
        "palette": [0, 12, 1],
        "numColumns": [1, 50, 1],
        "numRows": [1, 50, 1],
        "gridNoise": [0, 1, 0.05],
        "offsetLeft": [-1, 1, 0.05],
        "offsetRight": [-1, 1, 0.05],
        "drop": [0, 0.95, 0.05],
        "edgeColor": [0, 4, 1],
        "strokeWidth": [0, 6, 0.2],
        "cid": [0, 1, 0.1]
    }


def run_generation(script_name, fn, variable_name, val1, val2, num_rounds=10):
    params = {}
    driver.execute_script(f"switch_imports('{script_name}')")
    for i in range(num_rounds):
        params = fn(val1, "_A")
        params_str = json.dumps(params)
        driver.execute_script(f"start({params_str})")
        time.sleep(4)
        driver.refresh()
        time.sleep(2)
        driver.execute_script(f"switch_imports('{script_name}')")
        time.sleep(4)

        params[variable_name] = val2
        params["name"] = "_B"
        params_str = json.dumps(params)
        driver.execute_script(f"start({params_str})")
        time.sleep(4)
        driver.refresh()
        time.sleep(2)
        driver.execute_script(f"switch_imports('{script_name}')")
        time.sleep(4)
        print(f"Done {script_name} round {i} of {num_rounds}")


driver = webdriver.Chrome("/Users/sash/local/chromedriver")
driver.get("localhost:8000/generation.html")
time.sleep(10)
num_rounds = 2000

# leaves
run_generation("leaves", get_params_leaves, "verticalSize", 0.25, 0.35, num_rounds)
run_generation("strokes", get_params_strokes, "strokeWidth", 5, 10, num_rounds)
run_generation("spractal", get_params_spractal, "overlap", 0.8, 1, num_rounds)
run_generation("tiles_cushions", get_params_tnc, "curvy", 1, 0, num_rounds)
run_generation("carpet", get_params_carpet, "nl", 3, 4, num_rounds)
run_generation("circle_packing", get_params_circlepacking, "pid", 1, 4, num_rounds)
