import discord
from discord.ext import commands
from discord.ui import Button, View

import requests
import os
from datetime import datetime
from dotenv import load_dotenv



load_dotenv()
token = os.getenv("TOKEN");

intents = discord.Intents.default()
# para que interactue
intents.message_content = True 
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)


# para leer comandos o usar
@bot.command()
# si el ususario escribe !info se mostrará este print
async def info(ctx):
    embed = discord.Embed(
        title="Información del Bot",
        description="Este bot fue desarrollado para ayudarte a gestionar el servidor de forma interactiva.",
        color=0x7289DA  # Color azul para el embed
    )
    embed.set_author(name="Tu Bot", icon_url="https://link-a-tu-imagen.com/avatar.png")
    embed.set_thumbnail(url="https://link-a-tu-imagen.com/logo.png")
    embed.add_field(name="Comando !rol", value="Asigna un rol al usuario.", inline=False)
    embed.add_field(name="Comando !ayuda", value="Muestra todos los comandos disponibles.", inline=False)
    embed.set_footer(text="Creado por ✨[MARILYN]✨")

    await ctx.send(embed=embed)

@bot.command()
async def limpiar(ctx, cantidad: int = 10):
    # Intenta borrar la cantidad de mensajes especificada
    try:
        await ctx.channel.purge(limit=cantidad)
        await ctx.send(f"{cantidad} mensajes eliminados", delete_after=5)
    except discord.Forbidden:
        await ctx.send("No tengo permisos para eliminar mensajes.")
    except Exception as e:
        await ctx.send(f"Ocurrió un error: {e}")
@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        resultado = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)

        if resultado.status_code == 404:
            await ctx.send("Pokemon no encontrado")
        else:
            img_url = resultado.json()["sprites"]["front_default"] 
            await ctx.send(img_url)   
    except Exception as ex:
            print("Error", ex)

@poke.error
async def error_type(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("tienes que pasarme un pokemon")



# respuesta a evento
@bot.event
async def on_ready():
    print("Bot en linea")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "hola" in message.content.lower():
        await message.channel.send(f"Hola {message.author.name}!")
    await bot.process_commands(message)     

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1301572398159761440)  # Asegúrate de que este ID sea correcto
    if channel is not None:  # Verifica que el canal existe
        embed = discord.Embed(
            description=f"Bienvenido✨✨ {member.mention} ✨✨ al servidor de prueba",
            color=0xff55ff,
            timestamp=datetime.now()
        )

        role = discord.utils.get(member.guild.roles, name="miembro")
        if role is not None:  # Verifica que se encontró el rol
            await member.add_roles(role)
            await channel.send(embed=embed)
        else:
            await channel.send(f"No se encontró el rol 'miembro'. Asegúrate de que existe.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Diccionario de palabras clave y sus respuestas con emojis
    palabras_clave = {
        "hola": "👋",         # Responder con emoji de saludo
        "gracias": "😊",      # Responder con emoji de agradecimiento
        "adiós": "👋",        # Responder con emoji de despedida
        "feliz": "😄",        # Responder con emoji de felicidad
        "tonta": "👍", 
        "ño":"😣",              # Responder con emoji de pulgar arriba
    }

    # Revisa cada palabra clave en el diccionario
    for palabra, emoji in palabras_clave.items():
        if palabra in message.content.lower():
            await message.add_reaction(emoji)

    # Procesa otros comandos además de las reacciones
    await bot.process_commands(message)
@bot.command()
async def rol(ctx, *, role_name: str):
    # Verifica si el rol existe en el servidor
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"El rol '{role_name}' no existe. Verifica el nombre y vuelve a intentarlo.")
        return

    if role in ctx.author.roles:
        await ctx.send(f"Ya tienes el rol '{role_name}'.")
        return

    try:
        await ctx.author.add_roles(role)
        await ctx.send(f"El rol '{role_name}' ha sido asignado a {ctx.author.mention}.")
    except discord.Forbidden:
        await ctx.send("No tengo permisos suficientes para asignar ese rol.")
    except Exception as e:
        await ctx.send(f"Ocurrió un error al asignar el rol: {e}")

# Comando para remover roles
@bot.command()
async def remover_rol(ctx, *, role_name: str):
    # Verifica si el rol existe en el servidor
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role is None:
        await ctx.send(f"El rol '{role_name}' no existe. Verifica el nombre y vuelve a intentarlo.")
        return

    if role not in ctx.author.roles:
        await ctx.send(f"No tienes el rol '{role_name}' asignado.")
        return

    try:
        await ctx.author.remove_roles(role)
        await ctx.send(f"El rol '{role_name}' ha sido removido de {ctx.author.mention}.")
    except discord.Forbidden:
        await ctx.send("No tengo permisos suficientes para remover ese rol.")
    except Exception as e:
        await ctx.send(f"Ocurrió un error al remover el rol: {e}")





# Definimos los roles disponibles
roles = {
    "Deportista": 1301723151302131742,
    "Artista": 1301729913346457610,
    "Novio":1301726538181382144

}


        # Clase personalizada para los botones de rol
class RoleButton(Button):
    def __init__(self, label, role_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"El rol {role.name} ha sido removido.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"El rol {role.name} ha sido asignado.", ephemeral=True)

# Comando para enviar los botones de selección de roles
@bot.command()
async def seleccionar_roles(ctx):
    view = View()
    for role_name, role_id in roles.items():
        view.add_item(RoleButton(label=role_name, role_id=int(role_id)))
    
    await ctx.send("Selecciona un rol haciendo clic en los botones:", view=view)



class InfoButton(Button):
    def __init__(self, label, url=None):
        super().__init__(label=label, style=discord.ButtonStyle.link if url else discord.ButtonStyle.primary, url=url)

    async def callback(self, interaction):
        await interaction.response.send_message("Gracias por hacer clic en el botón!", ephemeral=True)

@bot.command()
async def opciones(ctx):
    view = View()
    # Botón de acción
    view.add_item(InfoButton(label="¡Haga clic aquí!", url="https://tu-link.com"))
    # Botón de rol personalizado
    view.add_item(InfoButton(label="Información adicional"))

    embed = discord.Embed(
        title="Elige una opción",
        description="Puedes hacer clic en uno de los botones de abajo para explorar más.",
        color=0x57F287
    )

    await ctx.send(embed=embed, view=view)
@bot.command()
async def bienvenida(ctx):
    embed = discord.Embed(
        title="🎉 Bienvenido al Servidor! 🎉",
        description="Estamos emocionados de que estés aquí. Por favor, explora los canales y selecciona tus roles.",
        color=0xFF5733
    )
    embed.add_field(name="📢 Anuncios", value="Consulta los últimos anuncios aquí.", inline=False)
    embed.add_field(name="🔗 Recursos", value="Encuentra recursos útiles para comenzar.", inline=False)
    
    view = View()
    view.add_item(Button(label="Ver reglas", style=discord.ButtonStyle.success, url="https://link-a-reglas.com"))

    await ctx.send(embed=embed, view=view)

bot.run(variableEntorno.TOKEN)
