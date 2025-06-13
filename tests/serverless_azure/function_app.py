# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
os.environ["PYTHONPATH"] = f"{os.environ['PYTHONPATH']}/:{os.environ['PACKAGES_DIR']}"

import newrelic.agent
import azure.functions as func  

newrelic.agent.initialize()  # Initialize the New Relic agent
os.environ["NEW_RELIC_APP_NAME"] = app_name = "Python Agent Test (serverless_azure)"
application = newrelic.agent.register_application(app_name, timeout=20.0)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
print(f"PYTHONPATH IN FUNCTION_APP: {os.environ['PYTHONPATH']}")

@app.function_name(name="HttpTriggerBasic")
@app.route(route="basic")
def basic_page(req):
    # Works when running locally but not on Github Actions.
    assert newrelic.agent.current_transaction(), "No active transaction."

    user = req.params.get("user")
    response = func.HttpResponse(f"Hello, {user}!", status_code=200, headers={"Content-Type": "text/plain"})
    return response
