from utils import init_app
from llm.prompt import STANDARD_PROMPT

class style:
    BOLD = '\033[1m'
    END = '\033[0m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    RED = '\033[31m'

llm, router = init_app()

# Assigning the issues that can be supported
issues = ['Password Reset', 'Account Unlock']
STANDARD_PROMPT = STANDARD_PROMPT.format(issues=issues)

# Adding the routes and examples to the router
router.add_route('Password Reset', ['I need to reset my password', 'I forgot my password', 'I need to change my password', 'password reset'])
router.add_route('Account Unlock', ['My account is locked', 'I need to unlock my account', 'My account is disabled', 'account locked', 'account disabled', 'account unlock'])

# Starting the conversation
print(f"{style.BOLD}Respond with 'bye' to end the conversation{style.END}")
introduction = print(f"{style.BLUE}SUPPORT BOT: What do you require help with?{style.END}")

while True:
    query = input(f"{style.GREEN}USER: {style.END}")
    
    # End conversation if user says 'bye'
    if 'bye' in query.lower():
        break

    # Identify the route the query matches
    route = router.identify_route(query)

    # Handling queries through routing
    match route:
        case 'Password Reset':
            # Handle logic for supporting password reset
            response = llm.query(STANDARD_PROMPT, query)
            print(f"{style.BLUE}SUPPORT BOT: {response}{style.END}")
        case 'Account Unlock':
            # Handle logic for supporting account unlock
            response = llm.query(STANDARD_PROMPT, query)
            print(f"{style.BLUE}SUPPORT BOT: {response}{style.END}")
        case other:
            # Block out of scope issues
            print(f"{style.RED}Currently the support bot is only able to help with the following issues: {issues}{style.END}")
