import asyncio
import requests
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import conversation
from homeassistant.const import MATCH_ALL, ATTR_NAME
from typing import Literal
from homeassistant.util import ulid
from homeassistant.components.homeassistant.exposed_entities import async_should_expose
from homeassistant.core import HomeAssistant, State
import logging
import time
from time import ctime
from datetime import datetime, timezone
from homeassistant.const import (
    EVENT_CALL_SERVICE
    )

from .const import (
    CONF_MAX_TOKENS,
    CONF_PROMPT,
    CONF_TEMPERATURE,
    CONF_TOP_P,
    CONF_MAX_FUNCTION_CALLS_PER_CONVERSATION,
    CONF_FUNCTIONS,
    CONF_BASE_URL,
    DEFAULT_ATTACH_USERNAME,
    DEFAULT_MAX_TOKENS,
    DEFAULT_PROMPT,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    DEFAULT_MAX_FUNCTION_CALLS_PER_CONVERSATION,
    DEFAULT_CONF_FUNCTIONS,
    DOMAIN,
    CONF_ATTACH_USERNAME,
    CONF_API_KEY,
    ENTFUN
)

from homeassistant.helpers import (
    config_validation as cv,
    intent,
    template,
    entity_registry as er
)

from .helpers import (
    validate_authentication,
    get_function_executor
)


#from homeassistant.helpers.event import async_track_state_change_async
DATA_AGENT = "agent"
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kobold Conversation from a config entry."""

    agent = KoboldAgent(hass, entry)

    data = hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {})
    data[CONF_API_KEY] = entry.data[CONF_API_KEY]
    data[DATA_AGENT] = agent

    conversation.async_set_agent(hass, entry, agent)
    return True


class KoboldAgent(conversation.AbstractConversationAgent):
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.history: dict[str, list[dict]] = {}
        base_url = entry.data.get(CONF_BASE_URL)
        api_key = entry.data[CONF_API_KEY]
        #setting up call? 
        
        
        #if is_azure(base_url):
        #    self.client = AsyncAzureOpenAI(
        #        api_key=entry.data[CONF_API_KEY],
        #        azure_endpoint=base_url,
        #        api_version=entry.data.get(CONF_API_VERSION),
        #    )
        #else:
        #    self.client = AsyncOpenAI(
        #        api_key=entry.data[CONF_API_KEY], base_url=base_url
        #    )
            
        #self.client = self.HordeClient(entry)
        
        #modelNames = await self.hass.async_add_executor_job(self.getModelNames)
        #modelNames = self.getModelNames()
        #event_data = entry
        #hass.bus.async_fire("kobold_event", modelNames)

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return a list of supported languages."""
        return MATCH_ALL

    async def HordeClient(self,
            messages,
            max_tokens,
            top_p,
            temperature,
            user
            ):
        #send comms? 
        api_key = self.entry.data[CONF_API_KEY]
        modelNames = await self.hass.async_add_executor_job(self.getModelNames)
        self.hass.bus.async_fire("kobold_event", {"Model Names": modelNames, "API Key": api_key})
        #sendPrompt = self._async_generate_prompt(self.entry.data[ENTFUN], entfun)
        sendPrompt = ""
        for eamsg in messages:
            sendPrompt = sendPrompt + "\n" + eamsg["role"] + ": " + eamsg["content"] + "\n"
        #sendPrompt = sendPrompt + "\nAssistant: "
        #    else:
        #        sendPrompt = sendPrompt + "\nAssistant: "

        headers = {
            "accept": "application/json",
            "apikey": api_key,
            "Client-Agent": "unknown:0:unknown",
            "Content-Type": "application/json"
        }
        json_data = {
            'prompt': sendPrompt+"\nsystem: ",
            'params': {
                'n': 1,
                'frmtadsnsp': True,
                'frmtrmblln': True,
                'frmtrmspch': True,
                'frmttriminc': True,
                'max_context_length': 1024,
                'max_length': max_tokens,
                'rep_pen': 3,
                'rep_pen_range': 4096,
                'rep_pen_slope': 10,
                'singleline': True,
                'temperature': temperature,
                'tfs': 1,
                'top_a': 1,
                'top_k': 100,
                'top_p': top_p,
                'typical': 1,
                'use_default_badwordsids': True,
                'min_p': 0,
                'dynatemp_range': 0,
                'dynatemp_exponent': 1,
                "stop_sequence": [
                ],
            },
            'trusted_workers': False,
            'slow_workers': False,
            'worker_blacklist': False,
            "models": modelNames,
            'dry_run': False,
            'disable_batching': False,
        }

        addy = "https://stablehorde.net/api/v2/generate/text/async"
        #args = {"address":addy, "headers":headers, "json":json_data}
        self.hass.bus.async_fire("kobold_event", json_data)
        message = await self.hass.async_add_executor_job(self.execute_internet_call, "post", addy, headers, json_data)

        self.hass.bus.async_fire("kobold_event", {"data": message})
        if "message" in message.keys():
            self.hass.bus.async_fire("kobold_event", {"data": message["message"]})
            return({"message": message["message"]})
        else:
            
            notYet = True
            time.sleep(5)
            msgid = message["id"]

            while notYet == True:

                addy = "https://stablehorde.net/api/v2/generate/text/status/"+msgid
                #args = {"address":addy, "headers":headers, "json":""}
                response = await self.hass.async_add_executor_job(self.execute_internet_call, "get", addy, headers, json_data)
                self.hass.bus.async_fire("kobold_event", {"data": response})


                # We should get the below as a response.
                #response = {
                #    "generations": [
                #        {
                #        "text": "AI Generated text here!",
                #        "seed": 0,
                #        "gen_metadata": [],
                #        "worker_id": "5544bbaf-8cf1-4146-8ed5-54145b7f690f",
                #        "worker_name": "discount-O2",
                #        "model": "koboldcpp/Silicon-Maid-7B",
                #        "state": "ok"
                #        }
                #    ],
                #    "finished": 1,
                #    "processing": 0,
                #    "restarted": 0,
                #    "waiting": 0,
                #    "done": True,
                #    "faulted": False,
                #    "wait_time": 0,
                #    "queue_position": 0,
                #    "kudos": 5,
                #    "is_possible": True
                #

                if response["finished"] == 1:
                    notYet = False
                    self.hass.bus.async_fire("kobold_event", {"data": response["generations"][0]["text"]})
                    return({"message":response["generations"][0]["text"]})
                else:
                    time.sleep(1+response["wait_time"]/2) # this is the polling rate

        return({"message":"It's a trap, you slipped out of the self.client's response decision tree. Redo that dumbass."})

    async def async_process(self, user_input: conversation.ConversationInput) -> conversation.ConversationResult:
        raw_prompt = self.entry.options.get(CONF_PROMPT, DEFAULT_PROMPT)

        if user_input.conversation_id in self.history:
            conversation_id = user_input.conversation_id
            messages = self.history[conversation_id]
        else:
            conversation_id = ulid.ulid()
            user_input.conversation_id = conversation_id
            prompt = self._async_generate_prompt(raw_prompt)

            dynPrompt = "<time> " + str(time.strftime("%A, %d %B %Y %R %P", time.localtime())) + " </time>\n<chat>"
            
            messages = [{"role": "system", "content": prompt+dynPrompt}]
        user_message = {"role": "user", "content": user_input.text}
        if self.entry.options.get(CONF_ATTACH_USERNAME, DEFAULT_ATTACH_USERNAME):
            user = await self.hass.auth.async_get_user(user_input.context.user_id)
            if user is not None and user.name is not None:
                user_message[ATTR_NAME] = user.name

        messages.append(user_message)
        response = await self.query(user_input, messages, 0)
        intent_response = intent.IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response)
        
        messages.append({"role": "system", "content": response})
        self.history[conversation_id] = messages
        return conversation.ConversationResult(
            response=intent_response, conversation_id=conversation_id
        )








    
    def _async_generate_prompt(self, raw_prompt: str) -> str:
        """Generate a prompt for the user."""
        return template.Template(raw_prompt, self.hass).async_render(
            {
                "ha_name": self.hass.config.location_name
            },
            parse_result=False,
        )

    async def query(
        self,
        user_input: conversation.ConversationInput,
        messages,
        n_requests,
    ):


        
        max_tokens = self.entry.options.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
        top_p = self.entry.options.get(CONF_TOP_P, DEFAULT_TOP_P)
        temperature = self.entry.options.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
        #functions = list(map(lambda s: s["spec"], self.get_functions()))
        #self.hass.bus.async_fire("kobold_event", {"data": functions})

        #Right CHA! hook in response to find a working function


        #if n_requests == self.entry.options.get(
        #    CONF_MAX_FUNCTION_CALLS_PER_CONVERSATION,
        #    DEFAULT_MAX_FUNCTION_CALLS_PER_CONVERSATION,
        #):
        #    function_call = "none"
        #if len(functions) == 0:
        #    functions = None
        #    function_call = None
        #_LOGGER.info("Prompt for %s: %s", messages)
        
        #if entity_id is not None:  s.split(':')[0]
        #    service_data = {"entity_id": entity_id, "rgb_color": rgb_color, "brightness": 255}
        #    hass.services.call("light", "turn_on", service_data, False)

        response: ChatCompletion = await self.HordeClient(
            messages=messages,
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature,
            user=user_input.conversation_id,
        )

        # HERE is the ID switch to get the messages

        choice: Choice = response["message"]
        message = choice

        # response looks like :Sure thing; turning living-room lights ON now...
        #self.hass.bus.async_fire("kobold_event", {"data": exposed_entities})
        #for ent_id in exposed_entities:
        return message
    

    
    def execute_internet_call(self, method, addy, headers, json_data):
        #'https://stablehorde.net/api/v2/generate/text/async', headers=headers, json=json_data
        #self.hass.bus.async_fire("kobold_event", {"address": addy})
        #self.hass.bus.async_fire("kobold_event", {"headers": headers})
        #self.hass.bus.async_fire("kobold_event", {"json": json_data})
        if method == "post":
            r = requests.post(addy, headers=headers, json=json_data)
        if method == "get":
            r = requests.get(addy, headers=headers, json=json_data)
        return(r.json())
        


    def getModelNames(self):
        headers = {
            'accept': 'application/json',
            'Client-Agent': 'unknown:0:unknown',
        }
        params = {
            'type': 'text',
        }
        response = requests.get('https://stablehorde.net/api/v2/status/models', params=params, headers=headers)
        r = response.json()
        modelNames = []
        for each in r:
            # Use this for all models
            #modelNames.append(each["name"])

            # use something like this to filter models you don't like. 
            if "koboldcpp" in each["name"].lower():
                modelNames.append(each["name"])

            # Or sort individual models like this
            #if "silicon" in each["name"].lower():
            #    modelNames.append(each["name"])

        return(modelNames)


