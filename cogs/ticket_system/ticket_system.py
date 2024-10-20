import nextcord
from nextcord import slash_command, SlashOption, Interaction
from nextcord.ext import commands


class BasicTicketSystem(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.ticket_creation_channel = nextcord.ui.ChannelSelect(placeholder="Select a channel", min_values=1, max_values=1, channel_type=nextcord.ChannelType.text)
        self.ticket_creation_category = nextcord.ui.Select(placeholder="Select a category", min_values=1, max_values=1, channel_type=nextcord.ChannelType.category)

        self.ticket_creation_category.callback = self.__ticket_creation_category_callback
        self.ticket_creation_channel.callback = self.__ticket_creation_channel_callback
        
        self.add_item(self.ticket_creation_channel)
        self.add_item(self.ticket_creation_category)
        
    async def __ticket_creation_category_callback(self, interaction: Interaction):
        self.selected_value = int(interaction.data['values'][0])
        self.selected_category = interaction.guild.get_channel(self.selected_value)

        # Save the selected category id && message id in the database

        await self.selected_category.send("Ticket creation category has been set!")
        await interaction.response.send_message(f"Ticket creation category has been set to {self.selected_category.mention}!", ephemeral=True)

    async def __ticket_creation_channel_callback(self, interaction: Interaction):
        self.selected_value = int(interaction.data['values'][0])
        self.selected_channel = interaction.guild.get_channel(self.selected_value)

        # Save the selected channel id && message id in the database

        await self.selected_channel.send("Ticket creation channel has been set!")
        await interaction.response.send_message(f"Ticket creation channel has been set to {self.selected_channel.mention}!", ephemeral=True)



class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configure_types = ["Basic", "Advanced", "Advanced+", "Premium"]

    @slash_command(name="tickets", description="Create a ticket")
    async def tickets(self, interaction: Interaction):
        return

    @tickets.subcommand(name="info", description="All the information about the ticket system")
    async def info(self, interaction: Interaction):
        await interaction.send("This is a ticket info command!")    
    
    @tickets.subcommand(name="configure", description="Configure the ticket system")
    async def configure(self, interaction: Interaction, type : str = SlashOption(name="type", description="Type of Ticket System")):

        if type not in self.configure_types:
            await interaction.response.send_message("Invalid type of ticket system. Please select from the options.", ephemeral=True)
            return
        
        match type:
            case "Basic":

                embed = nextcord.Embed(title="Ticket System Configuration", color=0x00FF00)
                embed.add_field(name="Type", value="Basic", inline=False)
                embed.add_field(name="Description", value="This is a basic ticket system configuration.", inline=False)

                await interaction.channel.send(embed=embed, view=BasicTicketSystem())

                await interaction.response.send_message(f"Configuring the ticket system for {type} type.", ephemeral=True)
            case "Advanced":
                await interaction.response.send_message(f"Configuring the ticket system for {type} type.", ephemeral=True)
            case "Advanced+":
                await interaction.response.send_message(f"Configuring the ticket system for {type} type.", ephemeral=True)
            case "Premium":
                await interaction.response.send_message(f"Configuring the ticket system for {type} type.", ephemeral=True)


    @configure.on_autocomplete("type")
    async def tickets_type(self, interaction: Interaction, type: str):
        await interaction.response.send_autocomplete(self.configure_types)

def setup(bot):
    bot.add_cog(TicketSystem(bot))