from random import choice
from typing import Dict, Annotated


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
        reflected: bool = False,
        player_short: bool = False,
        enemy_short: bool = False,
        last_hit: bool = False) -> dict:
    """ Возвращает {"player": str, "enemy": str} """

    if last_hit:
        if player_short:
            player_text = f'Вы разрубаете {enemy_name} на две части'
        else:
            player_text = f'Молниеносным ударом вашего клинка, вы разрубаете {enemy_name} на две части'
        if enemy_short:
            enemy_text = 'Вас разрубили на две части'
        else:
            enemy_text = f'{player_name} разрубает своим клинком вас, куски вашего тела падают в разные стороны'

        return {
            'player': player_text,
            'enemy': enemy_text
        }

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

    player_reflected_texts = {
        "classic": [
            'Быстрым движением вы достаете кинжал, но атака не увенчалась успехом...',
            f'Вы достали нож и пытаетесь ударить соперника, но у вас ничего не вышло...'
        ],
        "short": [
            'Вы пытались ударить врага кинжалом, но ничего не вышло...',
            f'*{enemy_name}* оказался сильнее примитивных атак...'
        ]
    }

    enemy_reflected_texts = {
        "classic": [
            'Ваш соперник достал кинжал, но вы были к этому готовы еще с рождения...',
            f'В голове у вас промелькнуло "*{player_name}*, сегодня не твой день" перед тем как отразить его атаку'
        ],
        "short": [
            'Ваш враг облажался, атака не удалась...',
            f'*{player_name}* совершил ошибку напав на вас...'
        ]
    }

    result = dict()

    if not reflected:
        result['player'] = choice(player_texts['short']) if player_short else choice(player_texts['classic'])
        result['enemy'] = choice(enemy_texts['short']) if enemy_short else choice(enemy_texts['classic'])
    else:
        result['player'] = choice(player_reflected_texts['short']) if player_short else choice(player_reflected_texts['classic'])
        result['enemy'] = choice(enemy_reflected_texts['short']) if enemy_short else choice(enemy_reflected_texts['classic'])

    return result



