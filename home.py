from nicegui import ui
from login import login
from signin import signup

# Routing
ui.page('/sign-in')(signup)
ui.page('/login')(login)

# Run the NiceGUI app
ui.run(port=8002)


