import db
import vkapi
import copy
import json

keyboards = {}
keyboards['-1'] = ""
keyboards['0'] = {"one_time": True,
                 "buttons": [
                                [{"action": {"type": "text", "payload": "1",
                                             "label": "1. Проголосовать на выборах"}, "color": "primary"}],
                                [{"action": {"type": "text", "payload": "2",
                                             "label": "2. Отправить сообщение Студсовету"}, "color": "primary"}]
                            ]
                }

keyb_templ =   {"one_time": True,
                 "buttons": []
                }

keyboards['0.1'] = keyboards['1.1'] =   {"one_time": True,
                                         "buttons": [[{"action": {"type": "text", "payload": "1",
                                                                     "label": "0. Вернуться в главное меню"}, "color": "default"}]]
                                        }

keyboards['1.1.1'] =   {"one_time": True,
                         "buttons": [
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "1. ФИО введены верно"}, "color": "negative"}],
                                        [{"action": {"type": "text", "payload": "2",
                                                     "label": "0. Вернуться в главное меню"}, "color": "default"}]
                                    ]
                        }

keyboards['2'] =  {"one_time": True,
                         "buttons": [
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "1. Вернуться к выбору ФИО"}, "color": "default"}],
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "0. Вернуться в главное меню"}, "color": "default"}]
                                    ]
                      }
keyboards['2.1'] =  {"one_time": True,
                         "buttons": [   [{"action": {"type": "text", "payload": "1",
                                                     "label": "1. Номер студбилета введён верно"},
                                          "color": "negative"}
                                        ],
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "2. Вернуться к выбору ФИО"},
                                          "color": "default"}
                                        ],
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "0. Вернуться в главное меню"},
                                          "color": "default"}
                                        ]
                                    ]
                      }

keyboards['3'] =  {"one_time": True,
                         "buttons": [
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "1. Да"},
                                          "color": "positive"},
                                         {"action": {"type": "text", "payload": "1",
                                                     "label": "2. Нет"},
                                          "color": "negative"}]
                                    ]
                      }

keyboards['4.2'] =  {"one_time": True,
                         "buttons": [
                                        [{"action": {"type": "text", "payload": "1",
                                                     "label": "0. Вернуться к выбору кандидатов"},
                                          "color": "positive"}]
                                    ]
                      }

keyboards['invitation'] =  {"one_time": True,
                             "buttons": [
                                            [{"action": {"type": "text", "payload": "1",
                                                         "label": "Проголосовать"},
                                              "color": "positive"}]
                                        ]
                          }

def gen_blue_button(text):
    but = {"action": {"type": "text", "payload": "1", "label": "1"}, "color": "primary"}
    but['action']['label'] = text
    return but

def gen_red_button(text):
    but = {"action": {"type": "text", "payload": "1", "label": "1"}, "color": "negative"}
    but['action']['label'] = text
    return but

def gen_green_button(text):
    but = {"action": {"type": "text", "payload": "1", "label": "1"}, "color": "positive"}
    but['action']['label'] = text
    return but

def gen_white_button(text):
    but = {"action": {"type": "text", "payload": "1", "label": "1"}, "color": "default"}
    but['action']['label'] = text
    return but

def get_board(state, vk_id):
    if state in keyboards.keys():
        keyb = keyboards[state]
        if keyb == "":
            return keyb
        else:
            return json.dumps(keyb, ensure_ascii=False)

    if state == '1':
        prof = vkapi.get_profile(vk_id)
        name = prof["first_name"]
        surname = prof["last_name"]
        vari = db.get_simular_voter(name, surname, vk_id)
        keyb = copy.deepcopy(keyb_templ)
        for num, keys in enumerate(vari):
            label = str(num + 1) + '. ' + keys[0]
            if len(label) > 40:
                label = label[:37] + "..."
            keyb["buttons"].append([gen_blue_button(label)])

        keyb["buttons"].append([gen_red_button(str(len(vari) + 1) + '. Меня нет в списке')])
        keyb["buttons"].append([gen_white_button('0. Вернуться в главное меню')])
        return json.dumps(keyb, ensure_ascii=False)

    if state == '4':
        candidates = db.get_candidates(vk_id)

        keyb = copy.deepcopy(keyb_templ)
        for num, cand in enumerate(candidates):
            fullname = cand[0] + ' ' + cand[1] + ' ' + cand[2]
            fullname = fullname.strip()

            keyb["buttons"].append([gen_blue_button(str(num + 1) + '. ' + fullname)])
        keyb["buttons"].append([gen_white_button('0. Против всех')])
        return json.dumps(keyb, ensure_ascii=False)

    if state == '4.1':
        candidates = db.get_candidates(vk_id)

        keyb = copy.deepcopy(keyb_templ)
        for num, cand in enumerate(candidates):
            fullname = cand[0] + ' ' + cand[1] + ' ' + cand[2]
            fullname = fullname.strip()

            if cand[8]:
                keyb["buttons"].append([gen_green_button(str(num + 1) + '. ' + fullname)])
            else:
                keyb["buttons"].append([gen_blue_button(str(num + 1) + '. ' + fullname)])

        keyb["buttons"].append([gen_white_button('0. Завершить голосование')])
        return json.dumps(keyb, ensure_ascii=False)

    if state == '4.1.1':
        keyb = copy.deepcopy(keyb_templ)

        candidates = db.get_candidates(vk_id)

        for num, cand in enumerate(candidates):
            fullname = cand[0] + ' ' + cand[1] + ' ' + cand[2]
            fullname = fullname.strip()

            if cand[8]:
                keyb["buttons"].append([gen_white_button(str(num + 1) + '. ' + fullname)])

        keyb["buttons"].append([gen_green_button('0. Подтвердить')])
        return json.dumps(keyb, ensure_ascii=False)

    return ""