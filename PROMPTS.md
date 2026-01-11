Please create a Python project that I can deploy to Cloudflare workers platform. The project is a simple Flask project that offers the following handlers:
/chat [GET, POST]

The purpose of this application is to accept a user string e.g. "what is the weather in riga" and then converts it using the Cloudflare Workers AI LLM into a JSON structure that can be used to query the weather from weather.com

Secrets (e.g. the weather.com API key) are stored in the environment variables section of the project.

Flow:
The user will visit a /chat handler and see a web page (hosted by cloudflare pages) that will allow him to input free-form text input. The user pressing enter will POST the input to the /chat handler.

Upon receiving the POST request, the application will convert the user input from a string into a JSON using a Workers AI model call. The Workers AI model call needs to format this JSON into a structure suitable to make a call to weather.com's API to get the weather. An example of this structure would be:
{ "intent": "get_weather", "q": string, "units": "metric"|"imperial", "timeframe": "now"|"today"|"tomorrow"|"7d" }
Provide additional instructions to the AI model to default to metric & now unless the user's input specifies otherwise. Also instruct the model to output strictly a JSON.
Test the output of the model to see whether it is valid JSON.

If not valid JSON, return a "Did not work!" to the front-end page.
If valid JSON, return the weather to the page and show it to the user.

Create a "cloudflare instructions.md" file that will walk me through all the steps I need to impement to make this work.

move the html to a separate html file and update any instructions files to reflect this new html file

Please update the application so that the workers AI also generates a little limerick about the target city and it's weather, for display to the user on the /chat webpage 

change the service provider to weatherapi.com
Update all instructions, request bodies, etc

when the weather comes back for multiple days, the response from the weather API looks like the sample in @sample1.json 
Update the front-end webpage to handle this correctly

Also, when a new query is made, clear out the results of the previous queries from the frontend UI

update the UI to make the background like the cloudflare theme and remove emojis in the limerick