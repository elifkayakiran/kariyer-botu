import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# JSON veri tabanını yükle
with open("meslekler.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} olarak giriş yapıldı!")

# Kategorileri belirle (mesleklerin "alanlar" kısmına göre)
KATEGORILER = [
    ("Teknoloji", "teknoloji"),
    ("Sanat", "sanat"),
    ("Yaratıcılık", "yaratıcılık"),
    ("İş Dünyası", "iş"),
    ("Mühendislik", "mühendislik"),
    ("Sağlık", "sağlık"),
    ("İnsan", "insan"),
    ("Hukuk", "hukuk"),
    ("Eğitim", "eğitim"),
    ("Toplum", "toplum"),
    ("Ekonomi", "ekonomi"),
    ("Dil", "dil"),
    ("Ulaşım", "ulaşım")
]

@bot.command()
async def kariyer(ctx):
    """
    Kullanıcıya ilgi alanı seçtiren butonlar
    """
    view = View()

    for label, custom_id in KATEGORILER:
        button = Button(label=label, style=discord.ButtonStyle.primary, custom_id=custom_id)

        async def button_callback(interaction: discord.Interaction, secim=custom_id):
            meslekler = [m for m in veri["meslekler"] if secim in m["alanlar"]]

            if meslekler:
                m = random.choice(meslekler)

                embed = discord.Embed(
                    title=f"💼 Meslek: {m['isim']}",
                    description=m["açıklama"],
                    color=0x00ff99
                )
                embed.add_field(name="🎯 Gerekli Beceriler", value=", ".join(m["beceriler"]), inline=False)
                embed.add_field(name="🎓 Eğitim", value=", ".join(m["egitim"]), inline=False)
                embed.add_field(name="⭐ Hedefler", value=", ".join(m["hedefler"]), inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Üzgünüm, bu alanda önerim yok 😔", ephemeral=True)

        button.callback = button_callback
        view.add_item(button)

    await ctx.send("📌 Hangi alana daha çok ilgi duyuyorsun?", view=view)

@bot.command()
async def oner(ctx, alan="teknoloji"):
    """
    Komutla meslek önerisi
    """
    meslekler = [m for m in veri["meslekler"] if alan in m["alanlar"]]
    if meslekler:
        m = random.choice(meslekler)

        embed = discord.Embed(title=f"💼 Meslek: {m['isim']}", description=m["açıklama"], color=0x00ff99)
        embed.add_field(name="🎯 Gerekli Beceriler", value=", ".join(m["beceriler"]), inline=False)
        embed.add_field(name="🎓 Eğitim", value=", ".join(m["egitim"]), inline=False)
        embed.add_field(name="⭐ Hedefler", value=", ".join(m["hedefler"]), inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Üzgünüm, bu alanda önerim yok 😔")

@bot.command()
async def yardım(ctx):
    """
    Botun yardım komutu
    """
    embed = discord.Embed(
        title="📖 Kariyer Botu Yardım",
        description="Bu bot sana yeni kariyer yolları önermeye yardımcı olur!",
        color=0x3498db
    )
    embed.add_field(
        name="!kariyer",
        value="📌 İlgi alanı seçmek için butonları gösterir. (Teknoloji, Sanat, Sağlık vb.)",
        inline=False
    )
    embed.add_field(
        name="!oner <alan>",
        value="🔍 Belirli bir alandan rastgele bir meslek önerir.\nÖrnek: `!oner teknoloji`",
        inline=False
    )
    embed.add_field(
        name="!yardım",
        value="📖 Bu mesajı gösterir.",
        inline=False
    )
    embed.set_footer(text="💡 İlgi alanına göre kariyerini keşfetmeye başla!")

    await ctx.send(embed=embed)




# Botu başlat
bot.run("")