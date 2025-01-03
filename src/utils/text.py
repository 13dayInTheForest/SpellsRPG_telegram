from random import choice


def dont_know_this_spell() -> str:
    texts = [
        'Вы еще не знаете такого заклинания',
        'Я не понял что вы сказали, сделаем вид что этого не было',
        'Давайте перестанем гадать, и просто выберем что-нибудь из вариантов снизу, ОК?',
        'Так, дайте проверю... Хм, нет, такого приема у вас нет',
        'Вы не можете этого сделать, по крайней мере в этой игре',
    ]
    return choice(texts)


def blade_strike_skill(
        player_name: str,
        enemy_name: str,
        done: bool,
        player_short: bool = False,
        enemy_short: bool = False) -> dict:

    player_texts = {
        "classic": [
            'Вы бросаетесь в сторону противника, кинжал в ваших руках нацелен прямо на его шею.',
            f'Вы достали кинжал, и побежали в сторону *{enemy_name}*, в надежде возить холодный кусок метала прямо в его сердце'
        ],
        "short": [
            'Вы бросаетесь в сторону противника с кинжалом',
            f'Вы достали кинжал, и побежали в сторону *{enemy_name}*'
        ]
    }

    enemy_texts = {
        "classic": [
            'Ваш враг достал кинжал, и рванул в вашу сторону сломя голову, в надежде убить вас.',
            f'*{player_name}* внезапно начал сокращать дистанцию между вами, вы увидели в его руке длинный кинжал.'
        ],
        "short": [
            'Ваш враг бежал на вас с кинжалом',
            f'*{player_texts}* хочет ударить ваш кинжалом'
        ]
    }

    result = dict()
    result['player'] = choice(player_texts['short']) if player_short else choice(player_texts['classic'])
    result['enemy'] = choice(enemy_texts['short']) if enemy_short else choice(enemy_texts['classic'])

    return result



