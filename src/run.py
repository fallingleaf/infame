from aura import Aura
import config


app = Aura().create_app(config)
app.run('localhost', 5000)
