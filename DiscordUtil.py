import discord
from discord.ui import View, Button


class PageView(View):
    def __init__(self, pages, message):
        super().__init__(timeout=None)
        self.pages = pages
        self.message = message
        self.page = 0
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.page == 0
        self.children[1].disabled = self.page == len(self.pages) - 1

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(self, button: Button, interaction: discord.Interaction):
        if self.page > 0:
            self.page -= 1
            await self.message.edit(embed=self.pages[self.page])
            self.update_buttons()
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, button: Button, interaction: discord.Interaction):
        if self.page < len(self.pages) - 1:
            self.page += 1
            await self.message.edit(embed=self.pages[self.page])
            self.update_buttons()
            await interaction.response.edit_message(view=self)