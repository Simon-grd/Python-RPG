# map.py
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from animation import scroll_text, screen_transition
from enemy import start_combat, Enemy
from item import feuille_dor, epee_mcd_attack, potion_invisibilite, potion_invincibilite, wamp_cave_plan

class GameMap:
    def __init__(self):
        self.console = Console()

    def show_game_map(self, ascii_art):
        self.console.clear()
        ascii_map = r"""
  _________________________________________________________
 /                                                         \
|  [bold]1. La Montagne de l'Enfer[/bold]                    [bold]2. Le Vaisseau Amiral[/bold]  |
|   ___   ___   ___                      /\  /\  /\        |
|  /   \ /   \ /   \                   /  \/  \/  \       |
| |     Cavernes     |                /             \      |
|  \___/ \___/ \___/                  \/\        /\/      |
|      |                  ______________  \      /         |
|      |                 /              \ \    /           |
| [bold]2. Jardins Étincelants[/bold]  | [bold]5. Marais des Secrets[/bold] | |
|   o  o  o  o  o      |  ~~  ~~  ~~  ~~ |    | ~~  ~~    |
|  < Fleurs Magiques >  |  Marécages     |    |           |
|   o  o  o  o  o       \_______________/     |  Serpents |
|      |                          |            \_/  \_/    |
| [bold]3. Forêt des Fées[/bold]       /   \                      |
|   /\  /\  /\              ____/     \____                |
|  /  \/  \/  \           /               \               |
| |  Arbres     |         |  [bold]Campement[/bold]   |              |
|  \  Ancestraux/          \_______________/               |
 \_________________________________________________________/
        """
        print(Panel.fit(f"[cyan]{ascii_map}[/cyan]", 
              title="[bold gold1]Carte du Royaume d'Eldoria[/bold gold1]", 
              border_style="green",
              padding=(1, 2)))
        input("\nAppuyez sur Entrée pour retourner au menu...")

    def la_montagne_de_lenfer(self, player):
        scroll_text("Vous tombez sur une feuille d'or au sol...", style="#FFA500")
        print("1. Vous ramassez la feuille\n2. Vous mangez la feuille \n")
        feuille = input("Que souhaitez vous faire ? ")
        if feuille == "1":
            print("Trop cool une feuille !")
            player.add_item(feuille_dor)
            print("Vous rencontrez Gandalf 'Bonjour jeune fourbe, que faites vous ici ?' :")
            print("1. Bonjour, je suis perdu, aide moi par pitié !\n2. Bonjour Monsieur, qui êtes vous ? Je suis à la recherche du One Piece \n")
            rep_gand = input("Quoi répondre a Gandalf ?")
            if rep_gand == "1":
                print("'Tiens pomme' -1500HP")
                player.health -= 1500
                if player.check_if_dead():
                    return 
            elif rep_gand == "2":
                print("'Je suis Gandalf, le seul habitant de cette dimension. Prends cette carte, elle t'y mènera'")
                print("Vous arrivez devant le OnePiece et donc devant le boss de la montagne")
                print("Le boss MODELIO se dresse sur le chemin (BOSS : NAME : Modelio 1350HP ATTACK : 500 DEFENSE : 300)")
                print("1. Vous donnez la feuille au boss\n2. Vous attaquez le boss \n")
                modelio = input("Pris de panique vous devez prendre une décision crutiale : ")
                if modelio == "1":
                    print("Vous avez vaincu le cruel boss modelio !")
                    player.gain_xp(300)
                elif modelio == "2":
                    boss_modelio = Enemy("MODELIO", 1350, 300, 150, 500)
                    start_combat(player, boss_modelio)
        elif feuille == "2":
            print("Miam c'est vraiment trop bon !")
            player.gain_xp(100)

    def le_vaisseau_amiral(self, player):
        print("Vous êtes à l'entrée du vaisseau et rencontrez l'alien ' Salut, que fais tu ici ?'")
        print("1. Si on fait une partie d'échecs et que je gagne, tu me laisse passer ?")
        print("2. Bonjour, je cherche le commandant du vaisseau")
        choice = input("Quoi lui répondre ? : ")
        if choice == "1":
            print("'T'es pas très fort pour le goat des échecs dis donc !'")
            print("Tu te fais ratio salement avec un mat du berger -50HP")
            player.health -= 50
            print(player.show_healthbar())
            player.gain_xp(50)
        elif choice == "2":
            print("'Suivez moi, je vais vous y mener'")
            print("Vous ouvrez la porte du centre de commandement")
            print("'Que faites vous ici !?'")
            print("1. Votre vaisseau m'appartient dès à présent !\n2. Ah non rien, je visite\n")
            prise_vaisseau = input("Que souhaitez vous faire ? : ")
            if prise_vaisseau == "1":
                print("Votre vaisseau m'appartient dès à présent ! + 50 DEF")
                player.defense += 50
                player.gain_xp(50)
                print("Le commandant du vaisseau veut vous combattre")
                print("1. Vous décidez d'utiliser le pion d'échecs comme totem d'immortalité")
                print("2. Vous essayez de vaincre le commandant du vaisseau")
                commandant = input("Que souhaitez vous faire ? : ")
                if commandant == "1":
                    print("Le boss finit par mourir car vous êtes immortel")
                elif commandant == "2":
                    boss_vaisseau = Enemy("Commandant du vaisseau", 500, 200, 100, 200)
                    start_combat(player, boss_vaisseau)
            elif prise_vaisseau == "2":
                print("Vous vous faites expulser du vaisseau par l'alien")

    def le_parc_mcd(self, player):
        scroll_text("Vous vous retrouvez devant un parc d'attraction à l'abandon et rencontrez l'armée de Looping :", style="#FFA500")
        print("1. Je tente de les contourner en escaladant la structure de l'attraction devant moi.")
        print("2. Je vais directement dans la direction de l'armée en espérant qu'ils me laissent passer.")
        parc = input("Que souhaitez vous faire ? : ")
        if parc == "1":
            print("Vous êtes sur une plateforme au dessus de l'armée :")
            print("1. Vous décidez de vous faufiler sur la plateforme jusqu'au boss Looping en espérant ne pas vous faire repérer.")
            print("2. Vous tentez de descendre de la plateforme juste derrière les gardes.")
            plateforme = input("Que souhaitez vous faire ? : ")
            if plateforme == "1":
                print("L'armée de Looping vous attaque et vous perdez car vous vous prenez pour Francis Ngannou")
                player.health -= 100
                print(player.show_healthbar())
            elif plateforme == "2":
                print("Un garde vous repère 'Revenez !'")
                garde = input("Voulez vous retourner vers le garde ? \n1. Oui\n2. Non")
                if garde == "1":
                    print("Le garde vous donne son épée de fou malade")
                    player.add_item(epee_mcd_attack)
                elif garde == "2":
                    print("Vous continuez a courrir vers le boss")
                    print("Vous vous trouvez maintenant devant le boss Looping(HP 1500  ATTACK : 750 DEFENSE : 250 )")
                    loopi = input("1. Vous utilisez l'épée MCD du garde\n2. Vous Activez votre totem d'immortalité")
                    if loopi == "1":
                        print("Vous vous faites ratio par les clés étrangères")
                        player.health -= 100
                        print(player.show_healthbar())
                    elif loopi == "2":
                        print("Vous gagnez")
                        print("EZ")
                        player.gain_xp(200)
        elif parc == "2":
            print("L'armée de Looping vous attaque et vous perdez car vous vous prenez pour Francis Ngannou")
            player.health -= 100
            print(player.show_healthbar())

    def la_foret_maria_db(self, player):
        scroll_text("Vous apparaissez dans une forêt assez sombre, avec autour de vous une clés étrangère :", style="#FFA500")
        key = input("1. Vous ramassez la clé\n2. Vous laissez la clé par terre\n")
        if key == "1":
            print("Une super clé inutile retour lobby...")
            player.health += 300
        elif key == "2":
            print("Soudain vous vous retrouvez face à une table de téléportation en plein milieu du chemin :")
            print("1 : Vous choisissez de vous téléporter à l'entrée de la forêt")
            print("2 : Vous choisissez de vous téléporter dans le royaume UTF8")
            print("3 : Vous choisissez de vous téléporter en tant qu'administrateur dans le royaume UTF8")
            tp = input("Que voulez vous faire ? : ")
            if tp == "1":
                print("BOUM")
            elif tp == "2":
                print("T mor")
                exit()
            elif tp == "3":
                print("Face à vous se trouve le Boss du royaume ( BOSS : NAME : UTF8MB4 HP : 1750 ATTACK : 600 DEFENSE : 400) vous possédez plusieurs droits admin :")
                print("1 : Vous utilisez /kill UTF8MB4")
                print("2 : Vous utilisez /ipconfig UTF8MB4")
                print("3 : Vous utilisez /lobby")
                adm = input("Quelle commande allez vous éxecuter ? : ")
                if adm == "1":
                    print("Vous avez vaincu le boss UTF8MB4 QUEL BOSS BRAVO")
                    player.gain_xp(500)
                elif adm == "2":
                    print("Dommage si pres du but t mor")
                    exit()
                elif adm == "3":
                    print("T'es perdu là")

    def le_chateau_de_wamp(self, player):
        scroll_text("Vous apparaissez face à un Enderman'brrrrr hrrr'")
        print("1. Vous vous imposez face à l'Enderman ")
        print("2. Vous passez devant lui sans le regarder")
        chateau = input("Que souhaitez vous faire? : ")
        if chateau == "1":
            print("L'Enderman vous téléporte dans le vide")
            player.health -= 100
            print(player.show_healthbar())
        elif chateau == "2":
            print("Vous accédez au château de Wamp")
            print("Arrivé à l'intérieur, plusieurs choix s'offrent à vous :")
            print("1. Vous empruntez le grand escalier face à vous")
            print("2. Vous apercevez une bibliothèque suspecte à votre gauche et décidez de passer derrière elle.")
            print("3.  Une tenue de garde Wamp est vêtue sur un mannequin à l'entrée et vous décidez de vous habiller avec.")
            into_chateau = input("Que souhaitez vous faire ? :")
            if into_chateau == "1":
                print("L'escalier ne mène à rien et vous retournez à l'entrée")
            elif into_chateau == "2":
                print("vous mourrez en vous faisant écraser par la bibliothèque")
                player.health -= 100
                print(player.show_healthbar())
            elif into_chateau == "3":
                print("Vous continuez à parcourir les couloirs du château")
                print("Un garde Wamp vient vous aborder 'Qui es-tu ? Je ne t'ai jamais vu ici.'")
                print("1. 'Salut, je suis nouveau. Saurais-tu où se trouve le Wamp'")
                print("2. 'Je fais partie des nouvelles recrues de Wamp. Sais-tu où se trouve le grand mâge du château ?'")
                garde_wamp = input("Que souhaitez vous faire? : ")
                if garde_wamp == "1":
                    print("'Nous n'avons pas le droit de rencontrer Mr Wamp, retournez faire votre garde !'")
                elif garde_wamp == "2":
                    print("'Oui bien sûr, suis moi !'")
                    print("Vous accédez à la chambre du Mâge")
                    print("Le Mâge 'De quoi as-tu besoin ?'")
                    print("1. 'Donne moi une potion d'invisibilité'")
                    print("2. 'Donne moi une potion d'invincibilité'")
                    mage = input("Que souhaitez vous faire ?")
                    if mage == "1":
                        print("Vous possédez maintenant une potion d'invisibilité")
                        player.add_item(potion_invisibilite)
                    elif mage == "2":
                        print("Vous possédez maintenant une potion d'invincibilité")
                        player.add_item(potion_invincibilite)
                        print("Le Mâge 'Avez-vous besoin d'autre chose ?")
                        print("1. 'Il me faudrait le code d'accès à la Wamp Cave'")
                        print("2. 'Où se trouve la Wamp Cave ?'")
                        mage2 = input("Que souhaitez vous faire ?")
                        if mage2 == "1":
                            print("'Je n'ai pas le droit, retourne faire ta garde'")
                        elif mage2 == "2":
                            print("'Prends ce plan, il t'y mènera'")
                            player.add_item(wamp_cave_plan)
                            print("Après avoir suivi les indications du plan, vous vous retrouvez devant la porte de la Wamp Cave")
                            print("1. Vous frappez à la porte")
                            print("2. Vous ingurgitez la potion que vous a donné le grand mâge précédemment")
                            wamp_cave = input("Que souhaitez vous faire ?")
                            if wamp_cave == "1":
                                print("Vous mourrez d'électrocution en touchant la porte")
                                player.health -= 100
                                print(player.show_healthbar())
                            elif wamp_cave == "2":
                                print("Vous utilisez la potion que vous a donné le grand mâge")
                                print("Vous apercevez une évacuation d'air provenant de la Wamp Cave")
                                print("1. Vous décidez d'enlever la grille et d'accéder au conduit de ventilation")
                                print("2. Vous cherchez un autre endroit afin d'accéder à la Wamp Cave")
                                wamp_cave2 = input("Que souhaitez vous faire ? : ")
                                if wamp_cave2 == "1":
                                    print("Vous voilà dans le plafond de la Wamp Cave")
                                elif wamp_cave2 == "2":
                                    print("Vous finissez par vous faire repérer par Wamp dans un endroit interdit et vous a renvoyé à l'entrée du château")
                                    print("Vous voulez attaquer Wamp, mais vous ne savez pas comment vous y prendre")
                                    print("1. Vous essayez de vaincre Wamp discrètement en lui infligeant un coup par derrière")
                                    print("2. Vous proposez directement un combat à Wamp")
                                    wamp_combat = input("Que souhaitez vous faire :")
                                    if wamp_combat == "1":
                                        print("Vous avez perdu votre chance de vaincre Wamp")
                                    elif wamp_combat == "2":
                                        wamp_enemy = Enemy("Wamp", 1000, 150, 75, 300)
                                        start_combat(player, wamp_enemy)

# Création d'une instance de GameMap et alias pour compatibilité avec le reste du projet
_game_map = GameMap()
show_game_map = _game_map.show_game_map
la_montagne_de_lenfer = _game_map.la_montagne_de_lenfer
le_vaisseau_amiral = _game_map.le_vaisseau_amiral
le_parc_mcd = _game_map.le_parc_mcd
la_foret_maria_db = _game_map.la_foret_maria_db
le_chateau_de_wamp = _game_map.le_chateau_de_wamp
