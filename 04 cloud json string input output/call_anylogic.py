#%% call_anylogic.py

from anylogiccloudclient.client.cloud_client import CloudClient
import json

AL_KEY = "eaa866c1-5de4-47aa-900e-214abb621887"
MODEL_NAME = "Demo: cloud json string"


# Create client, get latest version of the model, get inputs object
client = CloudClient(AL_KEY)
model = client.get_latest_model_version(MODEL_NAME)
inputs = client.create_inputs_from_experiment(model, "Experiment")


# read inputs string
with open("./custom_input.txt", "r") as infile:
    INPUT_STRING = json.load(infile)

# Set inputs
inputs.set_input(name="Raw JSON string", value=INPUT_STRING)


# create modelrun object and run model
modelrun = client.create_simulation(inputs)
outputs = modelrun.get_outputs_and_run_if_absent()


#%% Post call actions

# receive results
result_JSON = json.loads(outputs.get_raw_outputs()[0].value)

# print output
print(json.dumps(result_JSON, indent=4))


#%% REST version
import requests


class SessionBaseURL(requests.Session)

    def __init__(self, base_url: str, *args, **kwargs) -> None:
        self.base_url = base_url
        super().__init__(*args, **kwargs)

    def get(specific_endpoint: str, *args, **kwargs):
        
        url = self.base_url + '/' + specific_endpoint
        
        r = super().get(url, *args, **kwargs)
        return r

BASE_URL = "https://cloud.anylogic.com/api/open/8.5.0"




session = requests.Session()


session.get("https://cloud.anylogic.com/api/open/8.5.0")

