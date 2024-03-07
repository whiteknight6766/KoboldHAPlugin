"""Constants for the Extended OpenAI Conversation integration."""

DOMAIN = "kobold_conversation"
DEFAULT_NAME = "Kobold Conversation"
CONF_BASE_URL = "base_url"
CONF_NAME = "User"
DEFAULT_CONF_BASE_URL = "https://stablehorde.net/api/v2"
CONF_API_KEY = "0000000000"
EVENT_AUTOMATION_REGISTERED = "automation_registered_via_kobold_conversation"

CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """
<instructions>
You are a chat bot designed to be a house hold assistant. 
speak only in english. keep all responses very short and to the point. 
Use the TEMPLATE provided to interact with a device.
All readings are given in F.
If asked for the time, give only te time as listed in TIME.
</instruction>
<TEMPLATE>
device: state
</TEMPLATE>
"""
ENTFUN = """
<AVAILABLE DEVICES>
{% for entity in entfun -%}
{{ entity.entity_id }},{{ entity.name }},{{ entity.state }},{{entity.aliases | join('/')}}
{% endfor -%}
</AVAILABLE DEVICES>

"""
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 50
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5
CONF_MAX_FUNCTION_CALLS_PER_CONVERSATION = "max_function_calls_per_conversation"
DEFAULT_MAX_FUNCTION_CALLS_PER_CONVERSATION = 1
CONF_FUNCTIONS = "functions"
DEFAULT_CONF_FUNCTIONS = [
    {
        "spec": {
            "name": "execute_services",
            "description": "Use this function to execute service of devices in Home Assistant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "domain": {
                                    "type": "string",
                                    "description": "The domain of the service",
                                },
                                "service": {
                                    "type": "string",
                                    "description": "The service to be called",
                                },
                                "service_data": {
                                    "type": "object",
                                    "description": "The service data object to indicate what to control.",
                                    "properties": {
                                        "entity_id": {
                                            "type": "string",
                                            "description": "The entity_id retrieved from available devices. It must start with domain, followed by dot character.",
                                        }
                                    },
                                    "required": ["entity_id"],
                                },
                            },
                            "required": ["domain", "service", "service_data"],
                        },
                    }
                },
            },
        },
        "function": {"type": "native", "name": "execute_service"},
    }
]
CONF_ATTACH_USERNAME = "attach_username"
DEFAULT_ATTACH_USERNAME = False

SERVICE_QUERY_IMAGE = "query_image"
