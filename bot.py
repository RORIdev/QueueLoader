from __future__ import print_function

from QueueMessage import queue_message_from_dict
from ChatMessage import chat_message_from_dict
import os
import sys
import json
from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import input

def main():
    args = sys.argv[1:]
    if(len(args) != 1):
        print("Uso : bot.py queue\nEx: bot.py towny")
        sys.exit()
    else:
        EMAIL = ""
        PASSWORD = ""
        MULTIMC_INSTANCE = ""

        auth = authentication.AuthenticationToken()
        try:
            auth.authenticate(EMAIL,PASSWORD)
        except YggdrasilError as e:
            print(e)
            sys.exit()
        print("Logado como %s" % auth.username)
        connection = Connection("dc-f626de6d73b7.earthmc.net",25577, auth_token=auth, allowed_versions=[477])

        def entra_server(join_game_packet):
            print("Conectado no servidor")
            packet = serverbound.play.ChatPacket()
            packet.message = ("/joinqueue %s" %(args[0]))
            connection.write_packet(packet)
        connection.register_packet_listener(entra_server, clientbound.play.JoinGamePacket)

        def mensagem(chat_packet):
            if(chat_packet.field_string('position') == "SYSTEM" and chat_packet.json_data.startswith('{"extra":[{"color":"yellow","text":"You are currently in position ')):

                result = queue_message_from_dict(json.loads(chat_packet.json_data ))
                print("Pos : (%s) %s [%s]" %(result.extra[1].text[:-1], result.extra[3].text,args[0]))
                if(int(result.extra[1].text[:-1].replace(" ",""),10) <= 5):
                    connection.disconnect()
                    os.system('multimc -l "%s"'%(MULTIMC_INSTANCE))
            elif(chat_packet.field_string('position') == "CHAT"):

                result = chat_message_from_dict(json.loads(chat_packet.json_data))
                print("[%s] %s > %s" %(result.extra[0].hover_event.value[0].extra[1].text[:-1],result.extra[0].extra[0].text[:-2],result.extra[1].extra[0].text))
            elif(chat_packet.field_string('position') != "SYSTEM"):
                print("UNHANDLED %s MESSAGE : \n(%s)" %(chat_packet.field_string('position'),chat_packet.json_data))

        
            
        connection.register_packet_listener(mensagem, clientbound.play.ChatMessagePacket)
        connection.connect()

        while True:
            try:
                text = input()
                if text == "/respawn":
                    print("Respawnando ...")
                    packet = serverbound.play.ClientStatusPacket()
                    packet.action_id = serverbound.play.ClientStatusPacket.RESPAWN
                    connection.write_packet(packet)
                else:
                    packet = serverbound.play.ChatPacket()
                    packet.message = text
                    connection.write_packet(packet)
            except KeyboardInterrupt:
                print("Tchau!")
                sys.exit()

if __name__ == "__main__":
    main()
